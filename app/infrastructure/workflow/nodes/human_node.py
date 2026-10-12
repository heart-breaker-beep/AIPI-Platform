"""
Human-In-The-Loop Workflow Node。

负责：

Workflow
    ↓
HumanNode
    ↓
WAITING_HUMAN
    ↓
Checkpoint
    ↓
等待人工操作
"""

from .base import BaseNode


class HumanNode(BaseNode):
    """人工审核节点。"""

    name = "human_review"

    async def execute(
        self,
        state,
        context,
    ):
        """
        进入人工审核状态。

        WorkflowEngine 会检测 WAITING_HUMAN，
        保存 Checkpoint 后停止。
        """

        state.status = (
            "WAITING_HUMAN"
        )

        state.pause_reason = (
            "human_review_required"
        )

        return state