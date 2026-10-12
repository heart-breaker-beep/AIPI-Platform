"""
Workflow节点抽象。
"""

from abc import ABC, abstractmethod


class BaseNode(ABC):
    """
    Workflow执行节点基类。
    """

    # 节点名称
    name: str

    @abstractmethod
    async def execute(
        self,
        state,
        context
    ):
        """
        执行节点逻辑。
        """
        pass