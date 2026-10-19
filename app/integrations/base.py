"""
Tool基础接口。
"""

from abc import ABC, abstractmethod


class BaseTool(ABC):

    # Tool名称
    name: str


    @abstractmethod
    async def execute(
        self,
        **kwargs
    ):
        pass