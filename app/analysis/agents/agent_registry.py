"""
Agent Registry。

统一管理系统中的 Agent。
"""

from app.analysis.agents.critic_agent import (
    CriticAgent,
)
from app.analysis.agents.generic_skill_agent import (
    GenericSkillAgent,
)
from app.analysis.agents.planner_agent import (
    PlannerAgent,
)


class AgentRegistry:
    """Agent 管理器。"""

    def __init__(self):
        """初始化 Agent Registry。"""

        self.agents = {}

    def register(
        self,
        agent,
    ):
        """注册 Agent。"""

        self.agents[
            agent.name
        ] = agent

    def get(
        self,
        name,
    ):
        """根据名称获取 Agent。"""

        return self.agents.get(
            name
        )


def create_agent_registry(
    skill_registry,
):
    """
    创建默认 Agent 集合。
    """

    registry = AgentRegistry()

    agents = [
        PlannerAgent(
            skill_registry
        ),
        GenericSkillAgent(
            skill_registry,
            "repository_analysis_agent",
            "repository_analysis",
            "Analyze repository information",
        ),
        GenericSkillAgent(
            skill_registry,
            "architecture_analysis_agent",
            "architecture_analysis",
            "Analyze repository architecture",
        ),
        GenericSkillAgent(
            skill_registry,
            "technology_analysis_agent",
            "technology_analysis",
            "Analyze GitHub project technology stack",
        ),
        GenericSkillAgent(
            skill_registry,
            "evidence_analysis_agent",
            "evidence_analysis",
            "Extract traceable evidence from repository analysis results",
        ),
        CriticAgent(
            skill_registry
        ),
    ]

    for agent in agents:
        registry.register(
            agent
        )

    return registry