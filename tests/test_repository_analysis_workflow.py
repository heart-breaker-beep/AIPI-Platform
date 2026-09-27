import pytest


from app.workflow.workflow import Workflow

from app.workflow.engine import WorkflowEngine

from app.workflow.state import WorkflowState

from app.workflow.context import WorkflowContext


from app.workflow.nodes.skill_node import SkillNode


from app.skills.repository_analysis_skill import (
    RepositoryAnalysisSkill
)


from app.workflow.nodes.base import BaseNode

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
        SkillNode(
            name="repository_analysis",
            skill=RepositoryAnalysisSkill()
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

    assert (
        result.data[
            "repository_analysis"
        ][
            "repository"
        ][
            "repo"
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