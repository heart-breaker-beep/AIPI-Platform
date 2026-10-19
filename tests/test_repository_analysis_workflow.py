import pytest


from app.workflow.workflow import Workflow

from app.workflow.engine import WorkflowEngine

from app.workflow.state import WorkflowState

from app.workflow.context import WorkflowContext


from app.analysis.nodes.agent_node import AgentNode


from app.analysis.skills.repository_analysis_skill import (
    RepositoryAnalysisSkill
)


from app.analysis.nodes.base import BaseNode

from app.workflow.transition import Transition


#
# Mock Tool
#

class FakeGithubRepositoryTool:

    async def execute(
        self,
        **kwargs
    ):

        return {
            "repo": kwargs["name"],
            "owner": kwargs["owner"],
            "name": kwargs["name"],
        }


class FakeFileReaderTool:

    async def execute(
        self,
        **kwargs
    ):

        return {
            "content":
            "# Demo Repository"
        }


class FakeDependencyAnalyzerTool:

    async def execute(
        self,
        **kwargs
    ):

        return {
            "dependencies": [
                "fastapi",
                "sqlalchemy"
            ]
        }


class StartNode(BaseNode):

    name = "start"

    async def execute(
        self,
        state,
        context
    ):

        return state


class RepositoryAnalysisAgent:
    """
    把 Skill 包成 Agent。

    SkillNode 已删除（它只在测试里有调用方），
    这里改用生产链路上真正在跑的 AgentNode ——
    它按 Agent.execute(context, input_data) 契约取结果。
    """

    def __init__(
        self,
        skill,
    ):

        self.skill = skill

    async def execute(
        self,
        context,
        input_data,
    ):

        return await self.skill.execute(
            context,
            input_data,
        )


class EndNode(BaseNode):

    name = "end"

    async def execute(
        self,
        state,
        context
    ):

        state.status = "COMPLETED"

        return state


#
# 构建 Workflow
#

def build_workflow():

    workflow = Workflow()

    workflow.add_node(
        StartNode()
    )

    workflow.add_node(
        AgentNode(
            name="repository_analysis",
            agent=RepositoryAnalysisAgent(
                RepositoryAnalysisSkill()
            ),
        )
    )

    workflow.add_node(
        EndNode()
    )

    workflow.add_transition(
        Transition(
            "start",
            "repository_analysis"
        )
    )

    workflow.add_transition(
        Transition(
            "repository_analysis",
            "end"
        )
    )

    return workflow


#
# 构建 Context
#

def build_context():

    return WorkflowContext(
        agents={},

        tools={
            "github_repository":
                FakeGithubRepositoryTool(),

            "file_reader":
                FakeFileReaderTool(),

            "dependency_analyzer":
                FakeDependencyAnalyzerTool()
        },

        skills={
            "repository_analysis":
                RepositoryAnalysisSkill()
        },

        config={}
    )


#
# Workflow 集成测试
#

@pytest.mark.asyncio
async def test_repository_analysis_skill_workflow():

    workflow = build_workflow()

    state = WorkflowState(
        run_id="repo-analysis-test"
    )

    state.data = {
        "owner": "demo",
        "repo": "test-project",
        "project_path": "."
    }

    context = build_context()

    result = await WorkflowEngine().run(
        workflow,
        state,
        context
    )

    assert result.status == "COMPLETED"

    assert (
        "repository_analysis"
        in result.data
    )

    # Phase 12: RepositoryAnalysisSkill 现在只保留
    # 真实 GitHub API 里存在的字段。
    # 旧断言用的 "repo" 并不是 GitHub API 字段，
    # 因此改用 name。
    assert (
        result.data[
            "repository_analysis"
        ][
            "repository"
        ][
            "name"
        ]
        ==
        "test-project"
    )

    assert (
        result.data[
            "repository_analysis"
        ][
            "readme"
        ][
            "content"
        ]
        ==
        "# Demo Repository"
    )

    assert (
        result.data[
            "repository_analysis"
        ][
            "dependencies"
        ][
            "dependencies"
        ]
        ==
        [
            "fastapi",
            "sqlalchemy"
        ]
    )
