"""
Agent抽象定义。
"""


from abc import ABC, abstractmethod



class BaseAgent(ABC):
    """
    Agent基础接口。
    """
    name: str

    @abstractmethod
    async def run(
        self,
        state,
        context
    ):
        """
        执行Agent任务。
        """

        pass