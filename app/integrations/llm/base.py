"""
LLM抽象接口。
"""

from abc import ABC, abstractmethod

class BaseLLM(ABC):


    @abstractmethod
    async def chat(
        self,
        messages
    ):
        pass