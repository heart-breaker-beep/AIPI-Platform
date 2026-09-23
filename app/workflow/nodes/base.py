"""
Workflow节点基类。
"""

from abc import ABC, abstractmethod

class BaseNode(ABC):
    """
    所有Workflow节点的父类。
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
        执行节点。
        """

        pass