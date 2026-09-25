"""
Technology Analysis Agent。


负责：

分析项目技术栈。

例如：

- Python
- FastAPI
- Database
- LLM
- Docker


"""


from app.agents.base import BaseAgent




class TechnologyAnalysisAgent(
    BaseAgent
):


    name = (
        "technology_analysis_agent"
    )



    async def execute(
        self,
        context,
        input_data
    ):


        skill = self.get_skill(

            "technology_analysis"

        )


        return await skill.execute(

            context,

            input_data

        )