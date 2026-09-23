"""
Workflow开始节点。
"""


from app.workflow.node import BaseNode



class StartNode(BaseNode):


    name = "start"



    async def execute(
        self,
        state,
        context
    ):

        state.status = "RUNNING"

        return state