"""
分析节点。
"""


from app.workflow.node import BaseNode



class AnalysisNode(BaseNode):


    name = "analysis"



    async def execute(
        self,
        state,
        context
    ):

        # 模拟业务结果
        state.data[
            "result"
        ] = "analysis completed"


        return state