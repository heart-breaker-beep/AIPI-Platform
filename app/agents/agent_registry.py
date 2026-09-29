"""
Agent Registry。

统一管理系统中的 Agent。
"""

from app.agents.architecture_analysis_agent import (
    ArchitectureAnalysisAgent,
)
from app.agents.comparison_agent import (
    ComparisonAgent,
)
from app.agents.critic_agent import (
    CriticAgent,
)
from app.agents.evidence_analysis_agent import (
    EvidenceAnalysisAgent,
)
from app.agents.planner_agent import (
    PlannerAgent,
)
from app.agents.repository_analysis_agent import (
    RepositoryAnalysisAgent,
)
from app.agents.technology_analysis_agent import (
    TechnologyAnalysisAgent,
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
        RepositoryAnalysisAgent(
            skill_registry
        ),
        ArchitectureAnalysisAgent(
            skill_registry
        ),
        TechnologyAnalysisAgent(
            skill_registry
        ),
        EvidenceAnalysisAgent(
            skill_registry
        ),
        CriticAgent(
            skill_registry
        ),
        ComparisonAgent(
            skill_registry
        ),
    ]

    for agent in agents:
        registry.register(
            agent
        )

    return registry