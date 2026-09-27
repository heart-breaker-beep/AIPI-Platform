"""
Phase 12 前置集成测试。

验证：

1. AgentNode 使用新的 Agent.execute() 接口
2. Skill -> Tool 参数契约一致
3. Planner -> PlanExecutor -> Multi-Agent 可以真正串起来
4. Critic 可以读取前置 Agent 结果
"""

import pytest

from app.agents.critic_agent import CriticAgent
from app.agents.planner_agent import PlannerAgent
from app.workflow.context import WorkflowContext
from app.workflow.engine import WorkflowEngine
from app.workflow.nodes.agent_node import AgentNode
from app.workflow.nodes.base import BaseNode
from app.workflow.nodes.plan_executor_node import (
    PlanExecutorNode,
)
from app.workflow.state import WorkflowState
from app.workflow.transition import Transition
from app.workflow.workflow import Workflow

from app.skills.repository_analysis_skill import (
    RepositoryAnalysisSkill,
)
from app.skills.architecture_analysis_skill import (
    ArchitectureAnalysisSkill,
)
from app.skills.technology_analysis_skill import (
    TechnologyAnalysisSkill,
)
from app.skills.report_generation_skill import (
    ReportGenerationSkill,
)


class FakeGithubRepositoryTool:

    async def execute(
        self,
        *,
        owner,
        name,
    ):
        assert owner == "demo"
        assert name == "test-project"

        return {
            "owner": owner,
            "name": name,
        }


class FakeFileReaderTool:

    async def execute(
        self,
        *,
        owner,
        name,
        file_path,
        branch,
    ):
        assert owner == "demo"
        assert name == "test-project"

        assert file_path in {
            "README.md",
            "app/main.py",
        }

        if file_path == "README.md":
            return {
                "content": "# Demo Repository"
            }

        return {
            "content": (
                "class DemoApp:\n"
                "    pass\n"
            )
        }

class FakeDependencyAnalyzerTool:

    async def execute(
        self,
        *,
        project_path,
    ):
        assert project_path == (
            "D:/workspace/test-project"
        )

        return {
            "dependencies": [
                "fastapi",
                "sqlalchemy",
            ]
        }


class FakeCodeSearchTool:

    async def execute(
        self,
        *,
        keyword,
        repo,
    ):
        assert keyword == "class"
        assert repo == (
            "demo/test-project"
        )

        return [
            {
                "path": "app/main.py"
            }
        ]


class FakeReportExportTool:

    async def execute(
        self,
        *,
        title,
        content,
        filename,
    ):
        assert title == (
            "Repository Analysis Report"
        )

        assert filename == (
            "repository_analysis.md"
        )

        assert content

        return {
            "path": filename,
            "format": "markdown",
        }


class FakeSkillRegistry:

    def __init__(self):
        self.skills = {
            "repository_analysis":
                RepositoryAnalysisSkill(),
            "architecture_analysis":
                ArchitectureAnalysisSkill(),
            "technology_analysis":
                TechnologyAnalysisSkill(),
            "report_generation":
                ReportGenerationSkill(),
        }

    def get(self, name):
        return self.skills[name]


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


class StartNode(BaseNode):

    name = "start"

    async def execute(
        self,
        state,
        context,
    ):
        return state


class EndNode(BaseNode):

    name = "end"

    async def execute(
        self,
        state,
        context,
    ):
        return state


@pytest.mark.asyncio
async def test_agent_node_uses_new_execute_api():

    class NewApiAgent:

        async def execute(
            self,
            context,
            input_data,
        ):
            assert input_data[
                "question"
            ] == "test"

            return {
                "result": "ok"
            }

    state = WorkflowState(
        run_id="agent-node-test"
    )

    state.data = {
        "question": "test"
    }

    context = WorkflowContext(
        agents={},
        tools={},
        skills={},
        config={},
    )

    node = AgentNode(
        name="test_agent",
        agent=NewApiAgent(),
    )

    result = await node.execute(
        state,
        context,
    )

    assert result.data[
        "test_agent"
    ] == {
        "result": "ok"
    }


@pytest.mark.asyncio
async def test_skill_tool_contracts():

    context = WorkflowContext(
        agents={},
        tools={
            "github_repository":
                FakeGithubRepositoryTool(),
            "file_reader":
                FakeFileReaderTool(),
            "dependency_analyzer":
                FakeDependencyAnalyzerTool(),
            "github_code_search":
                FakeCodeSearchTool(),
            "report_export":
                FakeReportExportTool(),
        },
        skills={},
        config={},
    )

    input_data = {
        "owner": "demo",
        "repo": "test-project",
        "project_path":
            "D:/workspace/test-project",
    }

    repository_result = (
        await RepositoryAnalysisSkill().execute(
            context,
            input_data,
        )
    )

    assert (
        repository_result[
            "repository"
        ]["name"]
        == "test-project"
    )

    architecture_result = (
        await ArchitectureAnalysisSkill().execute(
            context,
            input_data,
        )
    )

    assert architecture_result[
        "modules"
    ][0]["file_path"] == "app/main.py"

    technology_result = (
        await TechnologyAnalysisSkill().execute(
            context,
            input_data,
        )
    )

    assert technology_result[
        "technology_stack"
    ]["dependencies"] == [
        "fastapi",
        "sqlalchemy",
    ]

    report_result = (
        await ReportGenerationSkill().execute(
            context,
            {
                "repository":
                    repository_result,
                "architecture":
                    architecture_result,
                "technology":
                    technology_result,
            },
        )
    )

    assert report_result[
        "report"
    ]["format"] == "markdown"


@pytest.mark.asyncio
async def test_planner_tasks_are_consumed_by_workflow():

    planner = PlannerAgent(
        FakeSkillRegistry()
    )

    planner_context = WorkflowContext(
        agents={},
        tools={},
        skills={},
        config={},
    )

    plan = await planner.execute(
        planner_context,
        {},
    )

    assert plan["tasks"] == [
        "repository_analysis_agent",
        "architecture_analysis_agent",
        "technology_analysis_agent",
        "evidence_analysis_agent",
        "critic_agent",
    ]

    repository_agent = FakeAgent(
        "repository_analysis_agent",
        {
            "repository": {
                "name": "demo"
            }
        },
    )

    architecture_agent = FakeAgent(
        "architecture_analysis_agent",
        {
            "architecture": {
                "modules": []
            }
        },
    )

    technology_agent = FakeAgent(
        "technology_analysis_agent",
        {
            "technology": {
                "stack": ["FastAPI"]
            }
        },
    )

    evidence_agent = FakeAgent(
        "evidence_analysis_agent",
        {
            "evidence": [
                {
                    "content":
                        "FastAPI application"
                }
            ]
        },
    )

    critic_agent = FakeAgent(
        "critic_agent",
        {
            "passed": True,
            "errors": [],
        },
    )

    context = WorkflowContext(
        agents={
            "repository_analysis_agent":
                repository_agent,
            "architecture_analysis_agent":
                architecture_agent,
            "technology_analysis_agent":
                technology_agent,
            "evidence_analysis_agent":
                evidence_agent,
            "critic_agent":
                critic_agent,
        },
        tools={},
        skills={},
        config={},
    )

    workflow = Workflow()

    workflow.add_node(
        StartNode()
    )

    workflow.add_node(
        AgentNode(
            name="planner_agent",
            agent=planner,
        )
    )

    workflow.add_node(
        PlanExecutorNode()
    )

    workflow.add_node(
        EndNode()
    )

    workflow.add_transition(
        Transition(
            "start",
            "planner_agent",
        )
    )

    workflow.add_transition(
        Transition(
            "planner_agent",
            "plan_executor",
        )
    )

    workflow.add_transition(
        Transition(
            "plan_executor",
            "end",
        )
    )

    state = WorkflowState(
        run_id="planner-integration"
    )

    state.data = {
        "owner": "demo",
        "repo": "test-project",
        "project_path":
            "D:/workspace/test-project",
    }

    result = await WorkflowEngine().run(
        workflow,
        state,
        context,
    )

    assert result.status == "COMPLETED"

    assert result.data[
        "executed_tasks"
    ] == [
        "repository_analysis_agent",
        "architecture_analysis_agent",
        "technology_analysis_agent",
        "evidence_analysis_agent",
        "critic_agent",
    ]

    assert "repository" in result.data
    assert "architecture" in result.data
    assert "technology" in result.data
    assert "evidence" in result.data

    assert result.data[
        "critic_agent"
    ]["passed"] is True

    assert len(
        repository_agent.calls
    ) == 1

    assert len(
        architecture_agent.calls
    ) == 1

    assert len(
        technology_agent.calls
    ) == 1

    assert len(
        evidence_agent.calls
    ) == 1

    assert len(
        critic_agent.calls
    ) == 1


@pytest.mark.asyncio
async def test_critic_accepts_agent_output_keys():

    critic = CriticAgent(
        FakeSkillRegistry()
    )

    context = WorkflowContext(
        agents={},
        tools={},
        skills={},
        config={},
    )

    result = await critic.execute(
        context,
        {
            "repository_analysis_agent": {
                "repository": {}
            },
            "architecture_analysis_agent": {
                "architecture": {}
            },
            "technology_analysis_agent": {
                "technology": {}
            },
        },
    )

    assert result["passed"] is True
    assert result["errors"] == []