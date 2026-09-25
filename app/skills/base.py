"""
Skill 基础抽象类。

Skill 和 Tool 的区别:

Tool:
    一个具体动作。
    例如:
        - 查询GitHub
        - 读取文件
        - 查询数据库


Skill:
    一个业务能力。
    可以组合多个 Tool 完成复杂任务。


例如:

RepositoryAnalysisSkill

    |
    +-- GitHubTool
    |
    +-- FileReaderTool
    |
    +-- DependencyAnalyzerTool

"""


from abc import ABC, abstractmethod



class BaseSkill(ABC):
    """
    所有 Skill 的基础接口。
    """


    # Skill唯一名称
    name: str


    # Skill功能描述
    description: str



    @abstractmethod
    async def execute(
        self,
        context,
        input_data: dict
    ):
        """
        执行 Skill。

        参数:

        context:
            Workflow运行上下文。

            保存:
                - tools
                - agents
                - skills


        input_data:
            当前Skill需要处理的数据。


        返回:
            Skill执行结果。

        """

        pass