"""
Architecture Analysis Agent。


负责：

分析项目代码架构。


例如：

- 目录结构
- 模块关系
- 核心流程


"""


from app.agents.base import BaseAgent




class ArchitectureAnalysisAgent(
    BaseAgent
):


    name = (
        "architecture_analysis_agent"
    )



    async def execute(
        self,
        context,
        input_data
    ):


        # 获取架构分析Skill

        skill = self.get_skill(

            "architecture_analysis"

        )



        return await skill.execute(

            context,

            input_data

        )