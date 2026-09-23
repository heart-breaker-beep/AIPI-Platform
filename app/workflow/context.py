"""
Workflow执行上下文。
"""


from dataclasses import dataclass


@dataclass
class WorkflowContext:
    """
    保存Workflow运行环境。
    """

    # Agent集合
    agents: dict


    # Tool集合
    tools: dict


    # Skill集合
    skills: dict


    # 配置参数
    config: dict