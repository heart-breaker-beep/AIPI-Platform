"""Phase 12：单项目完整业务闭环测试。"""

import pytest

from app.workflow.analysis_workflow import (
    build_analysis_workflow,
)
from app.workflow.checkpoint import (
    CheckpointManager,
)
from app.workflow.context import (
    WorkflowContext,
)
from app.workflow.engine import (
    WorkflowEngine,
)
from app.workflow.state import (
    WorkflowState,
    WorkflowStatus,
)


class FakeAgent:

    def __init__(
        self,
        name,
        result,
    ):
        self.name = name
        self.result = result
        self.calls = []

    async def execute(
        self,
        context,
        input_data,
    ):
        self.calls.append(
            dict(input_data)
        )

        return self.result


class FakeReportSkill:

    name = "report_generation"

    async def execute(
        self,
        context,
        input_data,
    ):
        return {
            "report": {
                "format": "markdown",
                "content": (
                    "# Project Intelligence Report"
                ),
            }
        }


def build_context():

    agents = {
        "planner_agent": FakeAgent(
            "planner_agent",
            {
                "tasks": [
                    "repository_analysis_agent",
                    "architecture_analysis_agent",
                    "technology_analysis_agent",
                    "evidence_analysis_agent",
                    "critic_agent",
                ],
                "research_plan": {
                    "plan_version": 1,
                    "tasks": [
                        "repository_analysis_agent",
                        "architecture_analysis_agent",
                        "technology_analysis_agent",
                        "evidence_analysis_agent",
                        "critic_agent",
                    ],
                },
            },
        ),

        "repository_analysis_agent": FakeAgent(
            "repository_analysis_agent",
            {
                "repository": {
                    "name": "demo",
                },
                "readme": "# Demo",
            },
        ),

        "architecture_analysis_agent": FakeAgent(
            "architecture_analysis_agent",
            {
                "architecture": {
                    "modules": [
                        {
                            "file_path":
                                "app/main.py",
                            "content":
                                "print('demo')",
                        }
                    ]
                }
            },
        ),

        "technology_analysis_agent": FakeAgent(
            "technology_analysis_agent",
            {
                "technology_stack": {
                    "frameworks": [
                        "FastAPI"
                    ]
                }
            },
        ),

        "evidence_analysis_agent": FakeAgent(
            "evidence_analysis_agent",
            {
                "evidence": [
                    {
                        "file_path":
                            "app/main.py",
                        "line_start": 1,
                        "line_end": 1,
                        "content":
                            "print('demo')",
                    }
                ]
            },
        ),

        "critic_agent": FakeAgent(
            "critic_agent",
            {
                "passed": True,
                "errors": [],
            },
        ),
    }

    return WorkflowContext(
        agents=agents,
        tools={},
        skills={
            "report_generation":
                FakeReportSkill(),
        },
        config={},
    )


@pytest.mark.asyncio
async def test_phase12_full_business_loop():

    context = build_context()

    workflow = build_analysis_workflow(
        context
    )

    checkpoint = CheckpointManager()

    engine = WorkflowEngine(
        checkpoint=checkpoint
    )

    state = WorkflowState(
        run_id="phase12-full-loop"
    )

    state.data = {
        "repository_id": 1,
        "owner": "demo",
        "repo": "demo-project",
        "repo_url":
            "https://github.com/demo/demo-project",
        "question":
            "分析 Multi-Agent Workflow",
    }

    # -------------------------------------------------
    # 1. Start -> Planner -> Design Gate
    # -------------------------------------------------

    result = await engine.run(
        workflow,
        state,
        context,
    )

    assert (
        result.status
        == WorkflowStatus.WAITING_DESIGN
    )

    assert (
        result.current_node
        == "design_gate"
    )

    assert (
        "research_plan"
        in result.data
    )

    # -------------------------------------------------
    # 2. Human Approve -> Multi-Agent
    # -------------------------------------------------

    result.approve()

    await checkpoint.save(
        result
    )

    result = await engine.resume(
        workflow,
        context,
        result.run_id,
    )

    assert (
        result.status
        == WorkflowStatus.WAITING_HUMAN
    )

    assert (
        result.current_node
        == "human_review"
    )

    assert (
        result.data[
            "executed_tasks"
        ]
        == [
            "repository_analysis_agent",
            "architecture_analysis_agent",
            "technology_analysis_agent",
            "evidence_analysis_agent",
            "critic_agent",
        ]
    )

    assert (
        result.data[
            "critic_agent"
        ]["passed"]
        is True
    )

    # -------------------------------------------------
    # 3. Human Review Approve -> Finalizer
    # -------------------------------------------------

    result.approve()

    await checkpoint.save(
        result
    )

    result = await engine.resume(
        workflow,
        context,
        result.run_id,
    )

    assert (
        result.status
        == WorkflowStatus.COMPLETED
    )

    assert (
        result.current_node
        == "end"
    )

    assert (
        "final_report"
        in result.data
    )

    assert (
        result.data[
            "final_report"
        ]["report"]["format"]
        == "markdown"
    )


@pytest.mark.asyncio
async def test_phase12_checkpoint_survives_design_gate():

    context = build_context()

    workflow = build_analysis_workflow(
        context
    )

    checkpoint = CheckpointManager()

    engine = WorkflowEngine(
        checkpoint=checkpoint
    )

    state = WorkflowState(
        run_id="phase12-checkpoint"
    )

    state.data = {
        "repository_id": 1,
        "owner": "demo",
        "repo": "demo",
        "question": "test",
    }

    result = await engine.run(
        workflow,
        state,
        context,
    )

    assert (
        result.status
        == WorkflowStatus.WAITING_DESIGN
    )

    restored = await checkpoint.load(
        "phase12-checkpoint"
    )

    assert restored is not None

    assert (
        restored.current_node
        == "design_gate"
    )

    assert (
        restored.data[
            "research_plan"
        ]["plan_version"]
        == 1
    )

# ==========================================================
# Phase 12 契约补充测试
#
# 覆盖文档 15.2 / 15.3 中此前没有实现的部分：
#   目录结构、Agent/Workflow/Skill/Tool 自述结构、
#   以及报告不得再使用硬编码内容。
# ==========================================================


class FakeTreeRepositoryTool:
    """带 get_tree 的假 GitHub Repository Tool。"""

    async def execute(self, *, owner, name):
        return {"owner": owner, "name": name}

    async def get_tree(self, *, owner, name, branch):
        return [
            {"type": "blob", "path": "README.md"},
            {"type": "blob", "path": "requirements.txt"},
            {"type": "blob", "path": "app/main.py"},
            {"type": "blob", "path": "app/agent/base.py"},
            {"type": "blob", "path": "tests/test_app.py"},
            {"type": "tree", "path": "app"},
        ]


class FakeEmptyCodeSearchTool:
    """模拟 Code Search 返回 0 条结果的真实情况。"""

    async def execute(self, *, keyword, repo):
        return []


class FakeModuleReaderTool:
    async def execute(self, *, owner, name, file_path, branch):
        return "class Demo:\n    pass\n"


def build_architecture_context():
    return WorkflowContext(
        agents={},
        tools={
            "github_repository": FakeTreeRepositoryTool(),
            "github_code_search": FakeEmptyCodeSearchTool(),
            "file_reader": FakeModuleReaderTool(),
        },
        skills={},
        config={},
    )


@pytest.mark.asyncio
async def test_directory_structure_comes_from_git_tree():
    """
    Code Search 返回 0 条结果时，
    目录结构必须来自 Git Trees API，
    而不是留空。
    """

    from app.skills.architecture_analysis_skill import (
        ArchitectureAnalysisSkill,
    )

    result = await ArchitectureAnalysisSkill().execute(
        build_architecture_context(),
        {
            "owner": "demo",
            "repo": "demo",
        },
    )

    structure = result["directory_structure"]

    assert structure["available"] is True

    assert structure["total_files"] == 5

    assert structure["by_extension"][".py"] == 3

    assert (
        structure["source"]
        == "github git trees api"
    )

    # files 也必须被文件树补全。
    assert "app/main.py" in result["files"]


@pytest.mark.asyncio
async def test_module_read_failure_does_not_break_analysis():
    """
    单个源码文件读取失败不能中断整个分析。

    旧行为：抛异常 → 整个 Workflow FAILED。
    """

    from app.core.exceptions import ToolError
    from app.skills.architecture_analysis_skill import (
        ArchitectureAnalysisSkill,
    )

    class FlakyReader:
        async def execute(self, *, owner, name, file_path, branch):
            raise ToolError(f"Read failed: {file_path}")

    context = WorkflowContext(
        agents={},
        tools={
            "github_repository": FakeTreeRepositoryTool(),
            "github_code_search": FakeEmptyCodeSearchTool(),
            "file_reader": FlakyReader(),
        },
        skills={},
        config={},
    )

    result = await ArchitectureAnalysisSkill().execute(
        context,
        {"owner": "demo", "repo": "demo"},
    )

    # 目录结构仍然可用。
    assert (
        result["directory_structure"]["available"]
        is True
    )

    # 失败被逐条记录，而不是抛出。
    assert result["modules"]

    assert all(
        module.get("error")
        for module in result["modules"]
    )


def test_report_contains_documented_sections():
    """报告必须包含文档 15.3 要求的 12 个章节。"""

    from app.skills.report_generation_skill import (
        ReportGenerationSkill,
    )

    content = ReportGenerationSkill._build_report({})

    for title in (
        "## 01 项目概览",
        "## 02 技术栈",
        "## 03 目录结构",
        "## 04 Agent 架构",
        "## 05 Workflow",
        "## 06 Skill",
        "## 07 Tool",
        "## 08 RAG",
        "## 09 Memory",
        "## 10 数据库",
        "## 11 关键源码",
        "## 12 Evidence",
    ):
        assert title in content


def test_report_has_no_hardcoded_content():
    """
    报告不得再出现硬编码内容。

    旧版本把 AIPI 自己的 Tool 列表和
    {"context_enabled": true} 写进报告，
    让报告看起来完整但内容是假的。
    """

    from app.skills.report_generation_skill import (
        ReportGenerationSkill,
    )

    content = ReportGenerationSkill._build_report({})

    assert "GitHub Repository Tool" not in content

    assert "context_enabled" not in content

    assert "memory_enabled" not in content

    # 取不到数据时必须明确说明。
    assert "真实数据不存在" in content


def test_report_uses_project_structure():
    """04/05/06/07/09 必须来自被分析项目的自述结构。"""

    from app.skills.report_generation_skill import (
        ReportGenerationSkill,
    )

    data = {
        "project_structure": {
            "available": True,
            "basis": "readme+topics",
            "dimensions": {
                "agents": {
                    "declared": True,
                    "items": ["Planner", "Critic"],
                    "topics": ["multi-agent"],
                    "evidence": [
                        {
                            "file_path": "README.md",
                            "line_start": 92,
                            "text": "- **Planner** ...",
                        }
                    ],
                },
                "tools": {
                    "declared": True,
                    "items": ["web_search"],
                    "topics": [],
                    "evidence": [],
                },
                "skills": {
                    "declared": False,
                    "items": [],
                    "topics": [],
                    "evidence": [],
                    "reason": "被分析项目未声明 skills。",
                },
            },
        }
    }

    content = ReportGenerationSkill._build_report(data)

    assert "Planner" in content

    assert "web_search" in content

    # 证据必须带可回溯的行号。
    assert "README.md" in content

    # 未声明的维度必须给出原因，
    # 而不是留空或编造内容。
    assert "被分析项目未声明 skills。" in content
