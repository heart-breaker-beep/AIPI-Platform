"""
Human-In-The-Loop节点。
"""

from .base import BaseNode

class HumanNode(BaseNode):
    """
    人工审核节点。
    """

    name = "human_review"

    async def execute(
        self,
        state,
        context
    ):

        # 暂停Workflow
        state.status = (
            "WAITING_HUMAN"
        )


        return state