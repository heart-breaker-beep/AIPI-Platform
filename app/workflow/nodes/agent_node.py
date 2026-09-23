"""
Agent类型Workflow节点。
"""


from .base import BaseNode



class AgentNode(BaseNode):
    """
    封装Agent执行。
    """


    def __init__(
        self,
        name,
        agent
    ):

        self.name = name

        self.agent = agent



    async def execute(
        self,
        state,
        context
    ):

        # 调用Agent
        result = await self.agent.run(
            state,
            context
        )


        # 保存结果
        state.outputs.append(
            result
        )


        return state