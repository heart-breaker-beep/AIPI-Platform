"""
ModuleDeepDiveSkill 测试。

深挖是「默认报告只看要点，细节按需展开」的
那一半能力，覆盖：

1. 模块名校验
2. 只挑该模块相关文件，且配额远大于默认报告
3. 明细带签名 / 调用链 / 常量 / 源码片段
4. 图节点能解析到真实定义
5. LLM 不可用 / 返回非法 JSON 时降级，
   仍然保留实现明细
6. 如实交代采集范围（读了哪些、哪些失败）

全程使用假 Tool，不联网。
"""

import json

import pytest

from app.core.exceptions import ToolError
from app.skills.module_deep_dive_skill import (
    ModuleDeepDiveSkill,
)

TREE = (
    "src/app/services/workflow_service.py",
    "src/app/services/other_service.py",
    "src/app/models/agent_run.py",
    "src/app/rag/retriever.py",
    "src/app/main.py",
    "tests/test_workflow.py",
)


WORKFLOW_SOURCE = (
    "from langgraph.graph import StateGraph\n"
    "\n"
    "\n"
    "class WorkflowService:\n"
    "    def build(self):\n"
    "        builder = StateGraph(AgentState)\n"
    "        builder.add_node('duplicate_check',\n"
    "                          self._node_duplicate_check)\n"
    "        return builder.compile()\n"
    "\n"
    "    def _node_duplicate_check(self, state) -> dict:\n"
    "        found = find_similar(state['vendor'])\n"
    "        if found.score >= 0.85:\n"
    "            state['status'] = 'suspected'\n"
    "        return state\n"
)


SOURCES = {
    "src/app/services/workflow_service.py": WORKFLOW_SOURCE,
    "src/app/services/other_service.py": (
        "def helper():\n    pass\n"
    ),
    "src/app/models/agent_run.py": (
        "class AgentRun(Base):\n    pass\n"
    ),
    "src/app/rag/retriever.py": (
        "from qdrant_client import QdrantClient\n"
        "\n"
        "def retrieve_documents(query):\n"
        "    return query\n"
    ),
    "src/app/main.py": (
        "from fastapi import FastAPI\n\napp = FastAPI()\n"
    ),
}


VALID_REPLY = json.dumps(
    {
        "responsibility": ["负责把录入流程编排成状态图。"],
        "key_implementations": [
            "duplicate_check 节点用 0.85 阈值判定重复"
        ],
        "data_structures": ["state 字典承载 vendor"],
        "call_flow": ["build() 注册节点后交给图执行"],
        "boundaries": ["数据不足：未见重试逻辑"],
        "risks": ["0.85 是硬编码常量"],
        "open_questions": ["human_review 未在本次范围内"],
    },
    ensure_ascii=False,
)


class FakeRepositoryTool:

    async def get_tree(self, **kwargs):
        return [
            {"path": path, "type": "blob"}
            for path in TREE
        ]


class FakeFileReader:

    def __init__(self, missing=()):
        self.missing = set(missing)
        self.read = []

    async def execute(
        self,
        owner,
        name,
        file_path,
        branch,
    ):
        self.read.append(file_path)

        if file_path in self.missing:
            raise ToolError("HTTP 404: Not Found")

        if file_path in SOURCES:
            return SOURCES[file_path]

        raise ToolError("HTTP 404: Not Found")


class FakeLLMTool:

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

    async def execute(
        self,
        *,
        title,
        content,
        filename,
    ):
        self.calls.append(
            {
                "title": title,
                "content": content,
                "filename": filename,
            }
        )

        return {
            "path": f"reports/{filename}",
            "format": "markdown",
        }


class FakeContext:

    def __init__(
        self,
        reader=None,
        llm=None,
        exporter=None,
    ):
        self.tools = {
            "github_repository": FakeRepositoryTool(),
            "file_reader": reader or FakeFileReader(),
        }

        if llm is not None:
            self.tools["llm_chat"] = llm

        if exporter is not None:
            self.tools["report_export"] = exporter


def run_deep_dive(
    module="workflow",
    reader=None,
    llm=None,
    exporter=None,
    **extra,
):
    import asyncio

    input_data = {
        "module": module,
        "owner": "demo",
        "repo": "demo",
        "run_id": "run-1",
    }

    input_data.update(extra)

    return asyncio.run(
        ModuleDeepDiveSkill().execute(
            FakeContext(reader, llm, exporter),
            input_data,
        )
    )


# ----------------------------------------------------------------
# 入参校验
# ----------------------------------------------------------------


def test_rejects_unknown_module():
    """不在六个模块内的名字必须直接拒绝。"""

    with pytest.raises(ValueError) as error:

        run_deep_dive(module="database")

    assert "Unsupported module" in str(
        error.value
    )

    # 提示里要列出合法值，便于调用方纠正。
    assert "workflow" in str(error.value)


def test_requires_owner_and_repo():

    import asyncio

    with pytest.raises(ValueError):

        asyncio.run(
            ModuleDeepDiveSkill().execute(
                FakeContext(),
                {"module": "workflow"},
            )
        )


def test_module_name_is_case_insensitive():
    """模块名大小写不敏感。"""

    result = run_deep_dive(
        module="WorkFlow",
        llm=FakeLLMTool(),
    )

    assert result["module"] == "workflow"


# ----------------------------------------------------------------
# 取材
# ----------------------------------------------------------------


def test_reads_module_relevant_files_first():
    """
    该模块相关的文件必须优先读。

    深挖的价值在于「比默认报告看得多」，
    因此配额要给到 40，并且优先命中该模块的文件。
    """

    result = run_deep_dive(
        module="workflow",
        llm=FakeLLMTool(),
    )

    assert (
        "src/app/services/workflow_service.py"
        in result["files_read"]
    )

    # 配额远大于默认报告的 20。
    assert ModuleDeepDiveSkill.MAX_FILES == 40


def test_unreadable_files_are_reported():
    """读取失败的文件必须如实带出来。"""

    reader = FakeFileReader(
        missing=["src/app/rag/retriever.py"]
    )

    result = run_deep_dive(
        module="workflow",
        reader=reader,
        llm=FakeLLMTool(),
    )

    assert (
        "## 本次采集范围" in result["content"]
    )

    assert "读取失败" in result["content"]

    assert (
        "src/app/rag/retriever.py"
        in result["content"]
    )


def test_fallback_skips_tests_and_migrations():
    """
    兜底补充文件时不能把配额喂给测试与迁移。

    真实案例：workflow 模块只有 workflow_service.py
    一个文件命中，其余 39 个名额全被 tests/ 和
    alembic/ 吃掉 —— 每个文件都是一次 GitHub 请求。
    """

    result = run_deep_dive(
        module="workflow",
        llm=FakeLLMTool(),
    )

    assert not any(
        "tests/" in path or "alembic/" in path
        for path in result["files_read"]
    )

    # 命中目标模块的文件仍要读到。
    assert (
        "src/app/services/workflow_service.py"
        in result["files_read"]
    )


def test_fallback_is_capped():
    """
    兜底补充文件必须封顶。

    实测：workflow 只有 1 个文件命中，
    剩余 39 个名额全用无关文件填满，
    深挖一次要 69 秒、40 次 GitHub 请求，
    而其中 39 个文件对 workflow 维度毫无贡献。
    """

    tree = (
        "src/app/services/workflow_service.py",
        *[
            f"src/app/core/mod{i}.py"
            for i in range(60)
        ],
    )


    class Repo:

        async def get_tree(self, **kwargs):
            return [
                {"path": path, "type": "blob"}
                for path in tree
            ]

    class Context:
        tools = {
            "github_repository": Repo(),
            "file_reader": FakeFileReader(),
        }

    skill = ModuleDeepDiveSkill()

    picked = skill._select_files(
        [
            {"path": path, "type": "blob"}
            for path in tree
        ],
        "workflow",
    )

    assert (
        "src/app/services/workflow_service.py"
        in picked
    )

    assert len(picked) == (
        1 + ModuleDeepDiveSkill.MAX_FALLBACK_FILES
    )

    assert len(picked) <= (
        ModuleDeepDiveSkill.MAX_FILES
    )


def test_rag_module_selects_rag_files():
    """RAG 深挖要优先挑到 rag 相关文件。"""

    result = run_deep_dive(
        module="rag",
        llm=FakeLLMTool(),
    )

    assert (
        "src/app/rag/retriever.py"
        in result["files_read"]
    )


# ----------------------------------------------------------------
# 实现明细
# ----------------------------------------------------------------


def test_details_include_source_snippet():
    """
    深挖与默认报告最大的差别：
    明细要带源码片段，而不只是签名。
    """

    result = run_deep_dive(
        module="workflow",
        llm=FakeLLMTool(),
    )

    content = result["content"]

    assert "## 实现明细" in content

    # 节点解析到真实定义。
    assert "`duplicate_check`" in content

    assert (
        "def _node_duplicate_check(self, state) -> dict"
        in content
    )

    assert "- 调用：`find_similar`" in content

    assert "`0.85`" in content

    # 源码片段真的被展开了。
    assert (
        "found = find_similar(state['vendor'])"
        in content
    )


def test_details_cap_is_larger_than_default():
    """深挖的明细上限必须大于默认报告的 6。"""

    assert ModuleDeepDiveSkill.MAX_DETAILS > 6


# ----------------------------------------------------------------
# 降级
# ----------------------------------------------------------------


def test_degrades_without_llm():
    """
    LLM 不可用时不能抛异常，
    实现明细仍要完整产出。
    """

    result = run_deep_dive(
        llm=FakeLLMTool(
            available=False,
            reason="未配置 LLM_API_KEY。",
        ),
    )

    assert (
        result["analysis"]["available"] is False
    )

    content = result["content"]

    assert "本模块的结论分析不可用" in content

    assert "未配置 LLM_API_KEY。" in content

    # 关键：确定性部分不受影响。
    assert "## 实现明细" in content

    assert (
        "def _node_duplicate_check(self, state) -> dict"
        in content
    )


def test_degrades_without_llm_tool():
    """连 llm_chat 工具都没有时同样降级。"""

    result = run_deep_dive()

    assert (
        result["analysis"]["available"] is False
    )

    assert "## 实现明细" in result["content"]


def test_degrades_on_invalid_json():

    result = run_deep_dive(
        llm=FakeLLMTool(
            content="这不是 JSON"
        ),
    )

    assert (
        result["analysis"]["available"] is False
    )

    assert "JSON" in result["analysis"]["reason"]


def test_parses_fenced_json():

    result = run_deep_dive(
        llm=FakeLLMTool(
            content=(
                "好的：\n```json\n"
                f"{VALID_REPLY}\n```"
            )
        ),
    )

    assert (
        result["analysis"]["available"] is True
    )

    assert (
        result["analysis"]["sections"][
            "responsibility"
        ][0]
        == "负责把录入流程编排成状态图。"
    )


# ----------------------------------------------------------------
# 渲染与导出
# ----------------------------------------------------------------


def test_renders_all_analysis_sections():

    content = run_deep_dive(
        llm=FakeLLMTool()
    )["content"]

    for label in (
        "职责",
        "关键实现",
        "涉及的数据结构",
        "调用流程",
        "边界与限制",
        "风险与可疑之处",
        "需要人工确认",
    ):

        assert f"### {label}" in content


def test_exports_to_module_specific_filename():
    """导出文件名要能区分 run 与模块。"""

    exporter = FakeExporter()

    result = run_deep_dive(
        llm=FakeLLMTool(),
        exporter=exporter,
    )

    assert exporter.calls[0]["filename"] == (
        "run-1_workflow_deep_dive.md"
    )

    assert result["report"]["format"] == (
        "markdown"
    )


def test_filename_falls_back_to_repo_without_run_id():

    import asyncio

    exporter = FakeExporter()

    asyncio.run(
        ModuleDeepDiveSkill().execute(
            FakeContext(exporter=exporter),
            {
                "module": "tools",
                "owner": "demo",
                "repo": "demo",
            },
        )
    )

    assert exporter.calls[0]["filename"] == (
        "demo_tools_deep_dive.md"
    )


def test_prompt_forbids_speculation():
    """深挖同样受「只归纳不推测」约束。"""

    llm = FakeLLMTool()

    run_deep_dive(llm=llm)

    system = llm.calls[0][0]["content"]

    user = llm.calls[0][1]["content"]

    assert "只能使用" in system

    assert "数据不足" in system

    # declared_by 的语义必须交代清楚。
    assert "readme" in system

    assert "<facts>" in user
