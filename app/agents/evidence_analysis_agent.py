"""
Evidence Analysis Agent。


负责：

分析结果证据追踪。


保证：

报告中的结论可以追溯：

源码

文档

向量库


"""


from app.agents.base import BaseAgent




class EvidenceAnalysisAgent(
    BaseAgent
):


    name = (
        "evidence_analysis_agent"
    )



    async def execute(
        self,
        context,
        input_data
    ):


        skill = self.get_skill(

            "evidence_analysis"

        )


        return await skill.execute(

            context,

            input_data

        )