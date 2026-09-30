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


class FakeSynthesisSkill:
    """
    报告综合分析 Skill 的假实现。

    记录收到的 input_data，
    便于断言 synthesis 节点确实
    把各 Agent 的产出转发给了它。
    """

    name = "report_synthesis"

    def __init__(self):
        self.calls = []

    async def execute(
        self,
        context,
        input_data,
    ):
        self.calls.append(
            dict(input_data)
        )

        return {
            "available": True,
            "reason": None,
            "summary": {
                "one_line": "这是一个演示项目。",
                "core_design": ["显式状态机"],
                "technology_choices": [],
                "highlights": [],
                "risks": [],
                "use_cases": [],
            },
            "dimensions": {
                "agents": "单 Agent 结构。",
            },
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
            "report_synthesis":
                FakeSynthesisSkill(),
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
    # 3. Human Review Approve -> Synthesis -> Finalizer
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

    # Synthesis 节点必须真的跑过，
    # 且拿到了前面各 Agent 的产出
    # （而不是只看自己那一次调用的入参）。
    synthesis = result.data["synthesis"]

    assert synthesis["available"] is True

    assert (
        synthesis["summary"]["one_line"]
        == "这是一个演示项目。"
    )

    synthesis_skill = context.skills[
        "report_synthesis"
    ]

    assert len(synthesis_skill.calls) == 1

    # 入参必须已经带上前面各 Agent 拍平后的产出，
    # 而不是只有启动时那几个字段。
    assert (
        synthesis_skill.calls[0]["repository"]
        == {"name": "demo"}
    )

    assert (
        synthesis_skill.calls[0]["readme"]
        == "# Demo"
    )

    assert (
        "architecture_analysis_agent"
        in synthesis_skill.calls[0]
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
    """
    报告必须包含 00 结论摘要与 01-11 章。

    注意：文档 15.3 要求的「关键源码」章已移除 ——
    它展示的是文件开头固定字符数，
    而 Python 文件开头必然是 import 块，
    渲染出来只有一堆 import，
    对理解项目没有帮助。
    """

    from app.skills.report_generation_skill import (
        ReportGenerationSkill,
    )

    content = ReportGenerationSkill._build_report({})

    for title in (
        "## 00 结论摘要",
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
        "## 11 Evidence",
    ):
        assert title in content

    # 关键源码章必须确实不在了。
    assert "关键源码" not in content


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


def test_report_is_rendered_as_markdown_not_json_dump():
    """
    01-12 章必须是可读的 markdown，
    不能再把中间数据结构直接 dump 成 JSON 代码块。
    """

    from app.skills.report_generation_skill import (
        ReportGenerationSkill,
    )

    data = {
        "repository": {
            "full_name": "demo/demo",
            "language": "Python",
            "topics": ["agents"],
            "stargazers_count": 1,
            "html_url": "https://github.com/demo/demo",
        },
        "technology_stack": {
            "frameworks": ["FastAPI"],
            "source_files": ["pyproject.toml"],
        },
        "directory_structure": {
            "available": True,
            "total_files": 10,
            "by_extension": {".py": 8},
            "top_level_dirs": [
                {"name": "src", "file_count": 8}
            ],
            "key_files": ["README.md"],
        },
        "project_structure": {
            "available": True,
            "basis": "readme+topics",
            "dimensions": {
                "agents": {
                    "declared": True,
                    "items": ["Planner"],
                    "topics": [],
                    "evidence": [],
                },
            },
        },
        "architecture_analysis_agent": {
            "modules": [
                {
                    "file_path": "src/main.py",
                    "content": "print('demo')\n",
                }
            ]
        },
        "evidence": [
            {
                "file_path": "README.md",
                "line_start": 1,
                "line_end": 5,
                "content": "# Demo\n",
            }
        ],
    }

    content = ReportGenerationSkill._build_report(
        data
    )

    # 只看 01 章之后：00 章在综合分析不可用时
    # 会用一个 ```text 小块写「不可用 + 原因」，
    # 那是刻意的提示块，不是数据 dump。
    body = content[
        content.index("## 01 项目概览"):
    ]

    assert "```text" not in body

    # 表格渲染出来了。
    assert "| 字段 | 值 |" in content

    assert "| 类别 | 检测结果 |" in content

    # 证据带行号。
    assert "`README.md:1-5`" in content


def test_report_rag_chapter_renders_declared_dimension():
    """
    08 RAG 在被分析项目声明了 rag 时，
    必须渲染自述条目与向量库检测结果。

    回归点：_structure_dimension 成功时
    返回的 dict 不带 "available" 键，
    旧代码用 declared.get("available") 判断，
    导致 RAG 章永远走「不可用」分支。
    """

    from app.skills.report_generation_skill import (
        ReportGenerationSkill,
    )

    data = {
        "technology_stack": {
            "embedding": ["Qdrant"],
        },
        "project_structure": {
            "available": True,
            "basis": "readme+topics",
            "dimensions": {
                "rag": {
                    "declared": True,
                    "items": ["semantic retrieval"],
                    "topics": [],
                    "evidence": [
                        {
                            "file_path": "README.md",
                            "line_start": 40,
                            "text": "- semantic retrieval",
                        }
                    ],
                },
            },
        },
    }

    content = ReportGenerationSkill._build_report(
        data
    )

    rag = content[
        content.index("## 08 RAG"):
        content.index("## 09 Memory")
    ]

    assert "semantic retrieval" in rag

    assert "Qdrant" in rag

    assert "README.md:40" in rag


def test_report_renders_synthesis_summary_and_judgments():
    """
    综合分析可用时，
    报告必须渲染 00 章与各章末尾的综合判断。
    """

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
                    "items": ["Planner"],
                    "topics": [],
                    "evidence": [],
                },
            },
        },
        "synthesis": {
            "available": True,
            "reason": None,
            "summary": {
                "one_line": "这是一个发票审批 Agent。",
                "core_design": ["draft-only"],
                "technology_choices": [],
                "highlights": [],
                "risks": ["RAG 维度数据不足"],
                "use_cases": [],
            },
            "dimensions": {
                "agents": "单 Agent + 显式状态机。",
            },
        },
    }

    content = ReportGenerationSkill._build_report(data)

    assert "## 00 结论摘要" in content

    assert "这是一个发票审批 Agent。" in content

    assert "### 风险与缺口" in content

    assert "RAG 维度数据不足" in content

    # 04 章末尾必须带上判断。
    assert "**综合判断**：单 Agent + 显式状态机。" in content

    # 没有判断的维度不应凭空多出一个空段落。
    assert content.count("**综合判断**") == 1


def test_report_states_when_synthesis_unavailable():
    """
    综合分析不可用时，
    00 章必须说明原因，
    且后续原始数据章节必须完整保留。
    """

    from app.skills.report_generation_skill import (
        ReportGenerationSkill,
    )

    content = ReportGenerationSkill._build_report(
        {
            "synthesis": {
                "available": False,
                "reason": "未配置 LLM_API_KEY。",
            }
        }
    )

    assert "## 00 结论摘要" in content

    assert "综合分析不可用。" in content

    assert "未配置 LLM_API_KEY。" in content

    # 降级不能牵连原始数据章节。
    assert "## 01 项目概览" in content

    assert "## 11 Evidence" in content

    # 不可用时不应出现任何综合判断段落。
    assert "**综合判断**" not in content


def test_plan_executor_does_not_duplicate_agent_results():
    """
    Agent 结果不能被重复存储。

    回归点：同名结果曾被写三遍
    （state.data[agent_name] + 拍平 + outputs），
    architecture 57KB、evidence 29KB，
    把 state_data 推到 263KB，
    越过 asyncmy 单字段 256KB 的缓冲区分片上限，
    报告接口读 checkpoint 直接
    Lost connection to MySQL server。
    """

    from app.workflow.nodes.plan_executor_node import (
        PlanExecutorNode,
    )

    big = {
        "project_structure": {"dimensions": {}},
        "modules": [{"file_path": "a.py"}],
        "files": ["a.py"],
        "directory_structure": {"available": True},
    }

    # architecture：只留读取方需要的子字段，
    # 最大的一块 project_structure 被剔掉。
    slim = PlanExecutorNode._slim_agent_result(
        "architecture_analysis_agent",
        big,
    )

    assert set(slim) == {
        "files",
        "modules",
        "directory_structure",
    }

    assert "project_structure" not in slim

    # evidence：没有任何读取方，整键不写。
    assert (
        PlanExecutorNode._slim_agent_result(
            "evidence_analysis_agent",
            {"evidence": [{"content": "x" * 1000}]},
        )
        is None
    )

    # 其余 Agent 原样保留 —— 删了会破坏断言它们的测试。
    small = {"passed": True, "errors": []}

    assert (
        PlanExecutorNode._slim_agent_result(
            "critic_agent",
            small,
        )
        == small
    )


def test_outputs_stores_marker_not_payload():
    """outputs 只留运行痕迹，不复制正文。"""

    from app.workflow.nodes.plan_executor_node import (
        PlanExecutorNode,
    )

    marker = PlanExecutorNode._output_marker(
        "architecture_analysis_agent",
        {
            "modules": [{"content": "x" * 5000}],
            "files": ["a.py"],
        },
    )

    assert marker["agent"] == (
        "architecture_analysis_agent"
    )

    assert marker["fields"] == ["files", "modules"]

    # 正文不在里面。
    assert "x" * 100 not in str(marker)
