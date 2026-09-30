"""
Phase 14 测试：Report Service（结构化报告 / JSON 导出）
与 Learning Path（学习路线）。

Phase 14 的两个新能力：

    14.1 Learning Path  项目 + 目标 → 学习路线
    14.2 Report Service  结构化报告数据 → Markdown / JSON

报告章节结构刻意未改（仍是 00 + 01-11），
文档 17.3 里那套 21 章会加回
已被移除的「核心源码分析」与被否掉的「项目比较」。
"""

import json

import pytest

from app.services.report_service import (
    ReportService,
)
from app.skills.learning_path_skill import (
    LearningPathSkill,
)
from app.tools.report_export_tool import (
    ReportExportTool,
)


def build_state():
    """一份接近真实的 state.data。"""

    return {
        "run_id": "run-1",
        "question": "分析项目的 agent",
        "research_plan": {
            "focus": {
                "dimensions": ["agents"],
                "notes": "关心协作",
                "source": "llm",
            }
        },
        "repository": {
            "name": "finance-agent",
            "full_name": "o/finance-agent",
            "description": "发票 Agent",
            "language": "Python",
            "topics": ["langgraph"],
            "stargazers_count": 5,
            "forks_count": 1,
            "open_issues_count": 0,
            "license": {"name": "MIT License"},
            "default_branch": "main",
            "size": 64,
            "created_at": "c",
            "pushed_at": "p",
            "html_url": "https://github.com/o/finance-agent",
        },
        "technology_stack": {
            "frameworks": ["FastAPI", "LangGraph"],
            "llm": ["OpenAI"],
            "database": ["PostgreSQL"],
            "embedding": [],
            "deployment": [],
        },
        "directory_structure": {
            "available": True,
            "total_files": 107,
            "top_level_dirs": [
                {"name": "src", "file_count": 77}
            ],
            "by_extension": {".py": 88},
            "key_files": ["pyproject.toml"],
        },
        "modules": [
            {
                "file_path": "src/app/services/workflow_service.py",
                "start_line": 37,
                "truncated": True,
                "content": "SECRET" * 300,
            },
            {
                "file_path": "src/app/main.py",
                "content": "print('x')",
            },
        ],
        "project_structure": {
            "available": True,
            "basis": "code+readme+topics",
            "dimensions": {
                "agents": {
                    "declared": True,
                    "declared_by": "code",
                    "items": ["class InvoiceAgent"],
                    "topics": [],
                    "evidence": [],
                    "code_evidence": [
                        {
                            "file_path": (
                                "src/app/agents/"
                                "invoice_agent.py"
                            ),
                            "line_start": 12,
                            "text": "class InvoiceAgent",
                        }
                    ],
                    "reason": None,
                    "details": [
                        {
                            "kind": "class",
                            "name": "InvoiceAgent",
                            "signature": "class InvoiceAgent",
                            "file_path": "a.py",
                            "line": 12,
                            "methods": ["execute"],
                            "calls": [],
                            "literals": [],
                            # 源码片段体积大且默认报告不渲染，
                            # 结构化文档里不该带上。
                            "source": "SOURCESNIPPET" * 200,
                        }
                    ],
                },
            },
        },
        "evidence": [
            {
                "file_path": "README.md",
                "line_start": 1,
                "line_end": 5,
                "content": "# hi",
                "source_type": "github",
                "source_url": "u",
                "verification_status": "UNVERIFIED",
            }
        ],
        "synthesis": {
            "available": True,
            "reason": None,
            "summary": {"one_line": "一句话。"},
            "dimensions": {"agents": "单 Agent。"},
        },
        "final_report": {
            "report": {
                "path": "reports/run-1_analysis.md",
                "format": "markdown",
            }
        },
    }


# ----------------------------------------------------------------
# Report Service
# ----------------------------------------------------------------


def test_document_has_stable_top_level_fields():
    """文档结构是消费方的契约，字段必须稳定。"""

    doc = ReportService.build_document(
        build_state()
    )

    assert doc["schema_version"] == (
        ReportService.SCHEMA_VERSION
    )

    for key in (
        "schema_version",
        "generated_at",
        "run_id",
        "title",
        "question",
        "focus",
        "project",
        "technology_stack",
        "directory",
        "modules",
        "dimensions",
        "evidence",
        "synthesis",
        "report",
    ):

        assert key in doc, key


def test_document_carries_focus():

    doc = ReportService.build_document(
        build_state()
    )

    assert doc["focus"]["dimensions"] == ["agents"]

    assert doc["focus"]["source"] == "llm"


def test_document_omits_module_content():
    """
    文档不带源码正文。

    20 个文件 × 1200 字符就是 20 多 KB，
    而 JSON 常被程序读进内存。
    要正文按 file_path 自己去取。
    """

    doc = ReportService.build_document(
        build_state()
    )

    assert doc["modules"] == [
        {
            "file_path": (
                "src/app/services/workflow_service.py"
            ),
            "start_line": 37,
            "truncated": True,
        },
        {
            "file_path": "src/app/main.py",
            "start_line": 1,
            "truncated": False,
        },
    ]

    assert "SECRET" not in json.dumps(
        doc, ensure_ascii=False
    )


def test_document_omits_detail_source():
    """明细不带 source 源码片段。"""

    doc = ReportService.build_document(
        build_state()
    )

    detail = doc["dimensions"]["agents"][
        "details"
    ][0]

    assert "source" not in detail

    assert "SOURCESNIPPET" not in json.dumps(
        doc, ensure_ascii=False
    )

    # 结构化部分要保留。
    assert detail["name"] == "InvoiceAgent"

    assert detail["methods"] == ["execute"]


def test_document_handles_empty_state():
    """没有数据时不能崩，要如实标注。"""

    doc = ReportService.build_document({})

    assert doc["project"]["available"] is False

    assert doc["directory"]["available"] is False

    assert doc["synthesis"]["available"] is False

    assert doc["modules"] == []

    assert doc["evidence"] == []


def test_document_handles_broken_state():

    doc = ReportService.build_document("x")

    assert doc["schema_version"] == 1

    assert doc["project"]["available"] is False


def test_json_output_keeps_chinese_readable():
    """
    JSON 不转义中文。

    转义成 \\uXXXX 会让文件膨胀一倍且不可读。
    """

    text = ReportService.to_json(
        ReportService.build_document(
            build_state()
        )
    )

    assert "发票 Agent" in text

    assert "\\u" not in text


def test_markdown_delegates_to_report_skill():
    """markdown 仍由 ReportGenerationSkill 渲染。"""

    content = ReportService.to_markdown(
        build_state()
    )

    assert "## 00 结论摘要" in content

    assert "## 04 Agent 架构" in content


@pytest.mark.asyncio
async def test_tool_exports_json(tmp_path):

    tool = ReportExportTool(str(tmp_path))

    result = await tool.export_json(
        {"a": "中文"},
        "r.json",
    )

    assert result["format"] == "json"

    written = json.loads(
        (tmp_path / "r.json").read_text(
            encoding="utf-8"
        )
    )

    assert written == {"a": "中文"}


@pytest.mark.asyncio
async def test_tool_export_dispatch(tmp_path):

    tool = ReportExportTool(str(tmp_path))

    md = await tool.export(
        title="T",
        content="正文",
        filename="r.md",
    )

    assert md["format"] == "markdown"

    js = await tool.export(
        title="T",
        content="",
        filename="r.json",
        document={"x": 1},
        fmt="json",
    )

    assert js["format"] == "json"


@pytest.mark.asyncio
async def test_tool_export_json_requires_document(
    tmp_path,
):

    tool = ReportExportTool(str(tmp_path))

    with pytest.raises(ValueError):

        await tool.export(
            title="T",
            content="",
            filename="r.json",
            fmt="json",
        )


# ----------------------------------------------------------------
# Learning Path
# ----------------------------------------------------------------


VALID_REPLY = json.dumps(
    {
        "learning_order": [
            "先读 workflow_service.py 的状态图装配"
        ],
        "prerequisites": [
            "LangGraph StateGraph：项目用它编排节点"
        ],
        "core_source": [
            (
                "`src/app/services/workflow_service.py`"
                " — 工作流主体"
            )
        ],
        "reading_path": ["从 main.py 入口进"],
        "improvements": ["新增节点参考 _node_* 写法"],
    },
    ensure_ascii=False,
)


class FakeLLM:

    def __init__(
        self,
        content=VALID_REPLY,
        available=True,
        reason=None,
    ):
        self.content = content
        self.available = available
        self.reason = reason
        self.calls = []

    async def execute(self, messages, **kwargs):

        self.calls.append(messages)

        if not self.available:
            return {
                "available": False,
                "reason": self.reason,
            }

        return {
            "available": True,
            "content": self.content,
        }


class FakeExporter:

    def __init__(self):
        self.calls = []

    async def execute(self, **kwargs):

        self.calls.append(kwargs)

        return {
            "path": f"reports/{kwargs['filename']}",
            "format": "markdown",
        }


class FakeContext:

    def __init__(self, llm=None, exporter=None):

        self.tools = {}

        if llm is not None:
            self.tools["llm_chat"] = llm

        self.tools["report_export"] = (
            exporter or FakeExporter()
        )


def run_path(data=None, llm=None, exporter=None):
    import asyncio

    return asyncio.run(
        LearningPathSkill().execute(
            FakeContext(llm, exporter),
            build_state() if data is None else data,
        )
    )


def test_learning_path_returns_all_sections():

    result = run_path(llm=FakeLLM())

    assert result["available"] is True

    for key in (
        "learning_order",
        "prerequisites",
        "core_source",
        "reading_path",
        "improvements",
    ):

        assert result["sections"][key], key


def test_learning_path_exports_own_file():
    """产物必须是独立文件，不覆盖分析报告。"""

    exporter = FakeExporter()

    result = run_path(
        llm=FakeLLM(),
        exporter=exporter,
    )

    assert exporter.calls[0]["filename"] == (
        "run-1_learning_path.md"
    )

    assert result["report"]["format"] == (
        "markdown"
    )


def test_learning_path_prompt_forbids_generic_advice():
    """
    prompt 必须禁止给通用学习路线。

    「先学 Python 再学 FastAPI」对任何项目都成立，
    因此毫无价值 —— 这是学习路线最容易退化的方向。
    """

    llm = FakeLLM()

    run_path(llm=llm)

    system = llm.calls[0][0]["content"]

    assert "禁止给通用学习路线" in system

    assert "数据不足" in system

    # 核心源码必须来自真实文件清单。
    assert "core_files" in system


def test_learning_path_facts_include_real_files():
    """
    事实里必须带上真实读到的文件清单 ——
    模型据此挑核心源码，不能凭空编文件名。
    """

    llm = FakeLLM()

    run_path(llm=llm)

    user = llm.calls[0][1]["content"]

    facts = json.loads(
        user[
            user.index("<facts>")
            + len("<facts>"):
            user.index("</facts>")
        ]
    )

    assert facts["core_files"] == [
        "src/app/services/workflow_service.py",
        "src/app/main.py",
    ]

    # 事实里也不该出现源码正文。
    assert "SECRET" not in user


def test_learning_path_degrades_without_llm():

    result = run_path()

    assert result["available"] is False

    assert "llm_chat" in result["reason"]


def test_learning_path_degrades_without_project_data():
    """没有分析数据时如实拒绝，不编通用路线。"""

    result = run_path(
        data={"run_id": "run-x"},
        llm=FakeLLM(),
    )

    assert result["available"] is False

    assert "没有可用于生成学习路线" in (
        result["reason"]
    )


def test_learning_path_degrades_on_invalid_json():

    result = run_path(
        llm=FakeLLM(content="不是 JSON")
    )

    assert result["available"] is False

    assert "JSON" in result["reason"]


def test_learning_path_renders_core_files():
    """渲染时列出可用于精读的真实文件。"""

    content = run_path(llm=FakeLLM())["content"]

    assert "## 学习顺序" in content

    assert "## 核心源码" in content

    assert "## 本次可用于精读的文件" in content

    assert (
        "`src/app/services/workflow_service.py`"
        in content
    )
