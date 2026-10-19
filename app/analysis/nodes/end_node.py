"""
Workflow结束节点。
"""


from app.workflow.node import BaseNode
from app.workflow.state import WorkflowStatus



class EndNode(BaseNode):


    name = "end"



    async def execute(
        self,
        state,
        context
    ):

        state.status = WorkflowStatus.COMPLETED

        return state
