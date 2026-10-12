"""
Skill Node


Workflow中的Skill执行节点。


职责:

Workflow

    ↓

SkillNode

    ↓

Skill

    ↓

Tool


"""
from .base import BaseNode

class SkillNode(BaseNode):


    def __init__(
        self,
        name,
        skill
    ):
        # 节点名称

        self.name = name


        # 对应Skill实例

        self.skill = skill

    async def execute(
        self,
        state,
        context
    ):
        """
        执行Skill。


        """
        result = await self.skill.execute(

            context=context,

            input_data=state.data

        )

        # 保存当前Skill输出

        state.data[
            self.name
        ] = result

        # 保存执行历史

        state.outputs.append(
            result
        )
        return state