"""
Skill类型Workflow节点。
"""


from .base import BaseNode

class SkillNode(BaseNode):
    """
    执行Skill能力。
    """

    def __init__(
        self,
        name,
        skill
    ):

        self.name = name

        self.skill = skill

    async def execute(
        self,
        state,
        context
    ):

        result = await self.skill.execute(
            state
        )

        state.outputs.append(
            result
        )


        return state