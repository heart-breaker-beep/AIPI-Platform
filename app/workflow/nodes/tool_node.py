"""
Tool类型Workflow节点。
"""


from .base import BaseNode



class ToolNode(BaseNode):
    """
    封装Tool调用。
    """


    def __init__(
        self,
        name,
        tool
    ):

        self.name = name

        self.tool = tool



    async def execute(
        self,
        state,
        context
    ):


        # 从 state.data 中按节点名取调用参数
        args = state.data.get(
            self.name,
            {}
        )


        # 执行Tool
        result = await self.tool.execute(
            **args
        )


        state.outputs.append(
            result
        )


        return state