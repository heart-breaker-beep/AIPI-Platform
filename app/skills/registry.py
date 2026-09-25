"""
Skill 注册中心。

作用:

统一管理系统中的 Skill。

Workflow / Agent 不需要关心 Skill 如何创建。

只需要:

registry.get("repository_analysis")

即可获取。


"""


from app.skills.repository_analysis_skill import (
    RepositoryAnalysisSkill
)


from app.skills.architecture_analysis_skill import (
    ArchitectureAnalysisSkill
)


from app.skills.technology_analysis_skill import (
    TechnologyAnalysisSkill
)


from app.skills.evidence_analysis_skill import (
    EvidenceAnalysisSkill
)


from app.skills.report_generation_skill import (
    ReportGenerationSkill
)




class SkillRegistry:
    """
    Skill管理器。
    """


    def __init__(self):

        # 保存所有Skill实例
        #
        # {
        #    "repository_analysis":
        #          RepositoryAnalysisSkill()
        # }

        self.skills = {}



    def register(
        self,
        skill
    ):
        """
        注册Skill。
        """


        self.skills[
            skill.name
        ] = skill



    def get(
        self,
        name:str
    ):
        """
        根据名称获取Skill。
        """

        return self.skills.get(
            name
        )




def create_skill_registry():
    """
    创建默认Skill集合。

    项目启动时调用。

    """


    registry = SkillRegistry()



    # 注册仓库分析Skill

    registry.register(
        RepositoryAnalysisSkill()
    )


    # 注册架构分析Skill

    registry.register(
        ArchitectureAnalysisSkill()
    )


    # 注册技术栈分析Skill

    registry.register(
        TechnologyAnalysisSkill()
    )


    # 注册证据分析Skill

    registry.register(
        EvidenceAnalysisSkill()
    )


    # 注册报告生成Skill

    registry.register(
        ReportGenerationSkill()
    )



    return registry