import pytest


from app.workflow.engine import WorkflowEngine

from app.workflow.workflow import Workflow

from app.workflow.state import WorkflowState

from app.workflow.context import WorkflowContext


from app.workflow.nodes.skill_node import SkillNode


from app.workflow.nodes.base import BaseNode

from app.workflow.transition import Transition



from app.skills.repository_analysis_skill import (
    RepositoryAnalysisSkill
)



class StartNode(BaseNode):


    name="start"



    async def execute(
        self,
        state,
        context
    ):

        return state





class EndNode(BaseNode):


    name="end"



    async def execute(
        self,
        state,
        context
    ):

        state.status="COMPLETED"

        return state




class GithubTool:

    async def execute(
        self,
        **kwargs
    ):

        return {
            "repo":
            kwargs["name"]
        }





class FileTool:


    async def execute(
        self,
        **kwargs
    ):


        return "README"





class DependencyTool:


    async def execute(
        self,
        **kwargs
    ):


        return [

            "fastapi"

        ]





def create_workflow():


    workflow = Workflow()


    workflow.add_node(
        StartNode()
    )


    workflow.add_node(

        SkillNode(

            "repository_analysis",

            RepositoryAnalysisSkill()

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





@pytest.mark.asyncio
async def test_full_skill_workflow():


    workflow=create_workflow()



    state=WorkflowState(

        run_id="test"

    )


    state.data={

        "owner":
        "demo",

        "repo":
        "test"

    }



    context=WorkflowContext(

        agents={},


        tools={


            "github_repository":
                GithubTool(),


            "file_reader":
                FileTool(),


            "dependency_analyzer":
                DependencyTool()


        },


        skills={},


        config={}

    )



    result = await WorkflowEngine().run(

        workflow,

        state,

        context

    )


    assert (
        result.status
        ==
        "COMPLETED"
    )


    assert (

        "repository_analysis"

        in result.data

    )