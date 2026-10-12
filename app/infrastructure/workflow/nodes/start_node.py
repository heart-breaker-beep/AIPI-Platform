"""
Workflow开始节点。
"""


from app.infrastructure.workflow.node import BaseNode
from app.infrastructure.workflow.state import WorkflowStatus



class StartNode(BaseNode):


    name = "start"



    async def execute(
        self,
        state,
        context
    ):

        # "RUNNING" 不是 WorkflowStatus 里的常量，
        # 分析阶段的状态就是 ANALYZING。
        state.status = WorkflowStatus.ANALYZING

        return state
