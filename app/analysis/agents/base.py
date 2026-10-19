"""
Agent 基础抽象类。


Agent 在系统中的职责：

    Agent
      |
      v
    Skill
      |
      v
    Tool


Agent:
    负责任务理解和能力调用。

Skill:
    封装具体业务能力。

Tool:
    执行具体操作。


例如：

RepositoryAnalysisAgent

        |
        v

RepositoryAnalysisSkill

        |
        +---- GitHub Tool
        |
        +---- File Reader Tool
        |
        +---- Dependency Tool


"""
from abc import ABC, abstractmethod
class BaseAgent(ABC):
    """
    所有 Agent 的基础接口。


    每个 Agent 必须：

    1. 有唯一名称
    2. 可以执行任务
    3. 可以访问 Skill Registry

    """
    # Agent唯一标识

    name: str

    # Agent功能描述

    description: str



    def __init__(
        self,
        skill_registry
    ):
        # Agent 不直接保存 Tool

        # 而是通过 Skill Registry 获取能力

        self.skill_registry = (
            skill_registry
        )

    def get_skill(
        self,
        skill_name
    ):

        """
        根据名称获取 Skill。


        例如：

        repository_analysis_agent

            获取

        repository_analysis_skill

        """

        return (
            self.skill_registry.get(
                skill_name
            )
        )

    @abstractmethod
    async def execute(
        self,
        context,
        input_data
    ):
        """
        Agent执行入口。


        context:
            当前运行上下文。


        input_data:
            当前任务数据。


        """

        pass