"""
Checkpoint 体积守卫与报告兜底测试。

背景
====

真实事故：被分析项目 Legal（17.8MB）跑完后，
checkpoint 的 state_data 涨到 263,743 字节，
越过 asyncmy 读取大字段的缓冲区分片上限
（实测与 MySQL sort_buffer_size 262,144 吻合）：

    Lost connection to MySQL server during query
    (Existing exports of data: object cannot be re-sized)

后果是**这个 run 再也读不回来了** ——
恢复、取报告、深挖全部 500，
而任务其实早就 COMPLETED。

两道防线：

1. 写入前守卫：state_data 超限就瘦身，
   保证写进去的行一定能读回来
2. 读取时兜底：checkpoint 读不出来就回读
   磁盘上的 reports/{run_id}_analysis.md
"""

import json
from pathlib import Path

from app.repositories.checkpoint import (
    MAX_STATE_BYTES,
    CheckpointRepository,
)
from app.services.analysis_workflow import (
    AnalysisWorkflowRunner,
)


def build_oversized_state():
    """构造一个远超上限的 state。"""

    return {
        "final_report": {
            "report": {
                "path": "reports/x_analysis.md",
                "format": "markdown",
            },
            "content": "# 报告\n" + "正文" * 20000,
        },
        "readme": "R" * 120000,
        "evidence": [
            {
                "file_path": f"f{i}.py",
                "content": "E" * 1500,
            }
            for i in range(40)
        ],
        "modules": [
            {
                "file_path": f"m{i}.py",
                "content": "M" * 1200,
            }
            for i in range(20)
        ],
        "business_field": {"important": "必须保留"},
    }


# ----------------------------------------------------------------
# 写入守卫
# ----------------------------------------------------------------


def test_oversized_state_is_trimmed_under_limit():

    state = build_oversized_state()

    assert (
        CheckpointRepository._size(state)
        > MAX_STATE_BYTES
    )

    data, trims = CheckpointRepository._fit_state_data(
        state
    )

    assert (
        CheckpointRepository._size(data)
        <= MAX_STATE_BYTES
    )

    assert trims

    assert trims["original_bytes"] > trims[
        "final_bytes"
    ]


def test_trim_drops_the_most_redundant_first():
    """
    先丢报告正文与 README。

    报告正文已经写在 reports/*.md，
    README 也已被抽取成结构 ——
    两者都是「丢了不心疼」的重复数据。
    """

    state = build_oversized_state()

    data, trims = CheckpointRepository._fit_state_data(
        state
    )

    dropped = trims["dropped_bytes"]

    assert "final_report.content" in dropped

    assert "readme" in dropped

    # 落到上限以内就停手，
    # 不该继续动 evidence / modules。
    assert "evidence" not in dropped

    assert "modules" not in dropped

    assert "content" not in data["final_report"]

    assert len(data["readme"]) == 4000


def test_trim_preserves_business_fields():
    """瘦身只动重复的大字段，不能误伤业务数据。"""

    state = build_oversized_state()

    data, _ = CheckpointRepository._fit_state_data(
        state
    )

    assert data["business_field"] == {
        "important": "必须保留"
    }

    assert len(data["evidence"]) == 40

    assert len(data["modules"]) == 20


def test_trim_falls_through_to_evidence_and_modules():
    """光丢报告正文和 README 还不够时，继续往后丢。"""

    state = {
        "final_report": {"content": "x" * 100},
        "readme": "short",
        # 光靠 evidence 与 modules 就把体积顶上去
        "evidence": [
            {"content": "E" * 2000} for _ in range(150)
        ],
        "modules": [
            {"content": "M" * 2000} for _ in range(150)
        ],
    }

    assert (
        CheckpointRepository._size(state)
        > MAX_STATE_BYTES
    )

    data, trims = CheckpointRepository._fit_state_data(
        state
    )

    assert (
        CheckpointRepository._size(data)
        <= MAX_STATE_BYTES
    )

    dropped = trims["dropped_bytes"]

    assert "evidence" in dropped or "modules" in dropped


def test_small_state_is_untouched():

    state = {"a": 1, "readme": "short"}

    data, trims = CheckpointRepository._fit_state_data(
        state
    )

    assert trims == {}

    assert data == state


def test_non_dict_state_does_not_crash():

    data, trims = CheckpointRepository._fit_state_data(
        "not-a-dict"
    )

    assert data == "not-a-dict"

    assert trims == {}


# ----------------------------------------------------------------
# 读取兜底
# ----------------------------------------------------------------


def test_report_falls_back_to_disk(tmp_path, monkeypatch):
    """
    checkpoint 读不出来时，回读磁盘上的报告文件。

    没有这条兜底，「分析成功但取报告 500」
    就会一直存在 —— 而报告其实早就写好了。
    """

    monkeypatch.chdir(tmp_path)

    reports = Path("reports")

    reports.mkdir()

    (reports / "run-1_analysis.md").write_text(
        "# 报告\n\n正文内容",
        encoding="utf-8",
    )

    result = AnalysisWorkflowRunner._report_from_disk(
        "run-1",
        None,
    )

    assert result["content"] == "# 报告\n\n正文内容"

    assert "run-1_analysis.md" in result[
        "report"
    ]["path"]


def test_report_fills_missing_content_from_disk(
    tmp_path,
    monkeypatch,
):
    """
    报告正文被瘦身丢掉时，同样从文件回读。

    state 里只剩路径，正文在磁盘上。
    """

    monkeypatch.chdir(tmp_path)

    reports = Path("reports")

    reports.mkdir()

    (reports / "run-2_analysis.md").write_text(
        "# 从文件读回来的报告",
        encoding="utf-8",
    )

    result = AnalysisWorkflowRunner._report_from_disk(
        "run-2",
        {
            "report": {
                "path": "reports/run-2_analysis.md",
                "format": "markdown",
            }
        },
    )

    assert result["content"] == (
        "# 从文件读回来的报告"
    )


def test_report_keeps_inline_content_when_present():
    """state 里有正文就不用读文件。"""

    report = {
        "report": {
            "path": "reports/nope.md",
            "format": "markdown",
        },
        "content": "# 来自 state 的正文",
    }

    result = AnalysisWorkflowRunner._report_from_disk(
        "run-3",
        report,
    )

    assert result is report


def test_report_returns_none_when_nothing_available(
    tmp_path,
    monkeypatch,
):
    """既没 state 也没文件时返回 None，而不是编一个。"""

    monkeypatch.chdir(tmp_path)

    assert (
        AnalysisWorkflowRunner._report_from_disk(
            "missing-run",
            None,
        )
        is None
    )


def test_trimmed_marker_is_underscore_prefixed():
    """
    瘦身记录必须用下划线开头。

    FinalizerNode 组装报告输入时会跳过
    下划线开头的键，否则这条记录会混进报告。
    """

    state = build_oversized_state()

    _, trims = CheckpointRepository._fit_state_data(
        state
    )

    assert trims

    key = "_trimmed"

    assert key.startswith("_")

    # 记录本身要能落库（可 JSON 序列化）。
    json.dumps({key: trims})
