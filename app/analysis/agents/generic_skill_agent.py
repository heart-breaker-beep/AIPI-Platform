"""
通用 Skill Agent。

取代了之前的：
- ArchitectureAnalysisAgent
- EvidenceAnalysisAgent
- TechnologyAnalysisAgent
- RepositoryAnalysisAgent

这些 Agent 都只是调用对应的 Skill，业务逻辑完全相同。
"""

from app.analysis.agents.base import BaseAgent


class GenericSkillAgent(BaseAgent):
    """通用的 Skill 代理，消除重复的 Agent 实现。"""

    def __init__(
        self,
        skill_registry,
        agent_name: str,
        skill_name: str,
        description: str = "",
    ):
        """
        初始化通用 Skill Agent。

        Args:
            skill_registry: Skill 注册表
            agent_name: Agent 唯一名称
            skill_name: 对应的 Skill 名称
            description: Agent 描述（可选）
        """
        super().__init__(skill_registry)
        self.name = agent_name
        self.description = description or f"Execute {skill_name} skill"
        self._skill_name = skill_name

    async def execute(
        self,
        context,
        input_data,
    ):
        """执行对应的 Skill。"""

        skill = self.get_skill(self._skill_name)
        return await skill.execute(context, input_data)
