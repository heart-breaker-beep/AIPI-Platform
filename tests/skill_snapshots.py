"""
技能输出快照的读写工具。

用途：第 4 阶段要合并几个技能之间的重复代码，
属于「行为不变」的纯重构。
快照的作用是把每个技能的**完整返回值**钉住 ——
只断言几个字段的话，重构中悄悄改掉的
其它字段（章节顺序、reason 文案、report 路径）不会被发现。

首次运行某个快照时把结果写进 tests/fixtures/skill_output/，
之后都做比较。要重新生成就删掉对应文件再跑。
"""

import json
from pathlib import Path


SNAPSHOT_DIR = (
    Path(__file__).parent
    / "fixtures"
    / "skill_output"
)


def _serialize(value) -> str:
    """稳定序列化：排序键、保留中文、非 JSON 类型转字符串。"""

    return json.dumps(
        value,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
        default=str,
    )


def assert_snapshot(
    name: str,
    result,
) -> None:
    """
    断言 result 与已存的快照一致。

    快照缺失时创建它并说明原因 ——
    这样新加技能时不需要手工抄一份输出进来。
    """

    SNAPSHOT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    path = SNAPSHOT_DIR / f"{name}.json"

    actual = _serialize(result)

    if not path.is_file():

        path.write_text(
            actual + "\n",
            encoding="utf-8",
        )

        raise AssertionError(
            f"快照不存在，已生成 {path}；"
            f"确认内容后重新运行即可。"
        )

    expected = path.read_text(
        encoding="utf-8"
    ).rstrip("\n")

    if expected != actual:

        raise AssertionError(
            f"技能输出与快照不一致：{name}\n"
            f"快照：{path}\n"
            "若确认这是预期的行为变化，删除该文件后重跑。"
        )

