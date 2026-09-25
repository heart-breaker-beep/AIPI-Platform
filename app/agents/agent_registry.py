"""
Agent Registry。


作用：

统一管理系统中的 Agent。


类似 SkillRegistry：

SkillRegistry:
    管理 Skill


AgentRegistry:
    管理 Agent



避免业务代码：

RepositoryAnalysisAgent()

TechnologyAgent()

大量硬编码创建。


"""


from app.agents.planner_agent import (
    PlannerAgent
)


from app.agents.repository_analysis_agent import (
    RepositoryAnalysisAgent
)


from app.agents.architecture_analysis_agent import (
    ArchitectureAnalysisAgent
)


from app.agents.technology_analysis_agent import (
    TechnologyAnalysisAgent
)


from app.agents.evidence_analysis_agent import (
    EvidenceAnalysisAgent
)


from app.agents.critic_agent import (
    CriticAgent
)





class AgentRegistry:
    """
    Agent 管理器。


    保存：

    {
        agent_name:
            agent_instance
    }

    """



    def __init__(self):


        # 保存所有Agent实例

        self.agents = {}



    def register(
        self,
        agent
    ):

        """
        注册 Agent。

        """

        self.agents[
            agent.name
        ] = agent




    def get(
        self,
        name
    ):

        """
        根据名称获取 Agent。
        """

        return self.agents.get(
            name
        )





def create_agent_registry(
    skill_registry
):
    """
    创建默认 Agent 集合。


    项目启动时调用。

    """

    registry = AgentRegistry()



    # 初始化所有领域Agent

    agents = [
        # 任务规划Agent

        PlannerAgent(
            skill_registry
        ),

        # 仓库分析Agent

        RepositoryAnalysisAgent(
            skill_registry
        ),



        # 架构分析Agent

        ArchitectureAnalysisAgent(
            skill_registry
        ),



        # 技术栈分析Agent

        TechnologyAnalysisAgent(
            skill_registry
        ),



        # 证据分析Agent

        EvidenceAnalysisAgent(
            skill_registry
        ),



        # 结果检查Agent

        CriticAgent(
            skill_registry
        )

    ]



    # 注册到Registry

    for agent in agents:


        registry.register(
            agent
        )



    return registry