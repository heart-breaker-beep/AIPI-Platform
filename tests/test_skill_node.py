import pytest

from app.infrastructure.workflow.nodes.skill_node import (
    SkillNode
)

from app.infrastructure.workflow.state import WorkflowState

from app.infrastructure.workflow.context import WorkflowContext


class FakeSkill:

    async def execute(
        self,
        context,
        input_data
    ):

        return {
            "result": "skill success"
        }


@pytest.mark.asyncio
async def test_skill_node_execute():

    node = SkillNode(
        name="test_skill",
        skill=FakeSkill()
    )

    state = WorkflowState(
        run_id="test"
    )

    context = WorkflowContext(
        agents={},
        tools={},
        skills={},
        config={}
    )

    result = await node.execute(
        state,
        context
    )

    assert (
        result.data["test_skill"]["result"]
        ==
        "skill success"
    )

    assert len(
        result.outputs
    ) == 1