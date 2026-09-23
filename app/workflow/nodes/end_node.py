"""
Workflow结束节点。
"""


from app.workflow.node import BaseNode



class EndNode(BaseNode):


    name = "end"



    async def execute(
        self,
        state,
        context
    ):

        state.status = "COMPLETED"

        return state