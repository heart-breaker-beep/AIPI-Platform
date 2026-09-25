"""
Technology Analysis Skill


分析项目技术栈。


例如:

- Python
- FastAPI
- LangChain
- Vector DB
- Docker


"""


from app.skills.base import BaseSkill




class TechnologyAnalysisSkill(
    BaseSkill
):


    name = "technology_analysis"



    description = (
        "Analyze technology stack"
    )



    async def execute(
        self,
        context,
        input_data
    ):


        # 获取依赖分析工具

        dependency_tool = (
            context.tools[
                "dependency_analyzer"
            ]
        )



        dependencies = await dependency_tool.execute(
            **input_data
        )



        return {


            "technology_stack":

                dependencies

        }