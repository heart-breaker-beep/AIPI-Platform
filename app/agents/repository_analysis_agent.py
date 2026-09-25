"""
Repository Analysis Agent。


负责：

分析 GitHub 项目的基础信息。


调用链：

RepositoryAnalysisAgent

        |

        v

RepositoryAnalysisSkill

        |

        v

GitHub Tool
File Reader Tool
Dependency Tool


"""


from app.agents.base import BaseAgent




class RepositoryAnalysisAgent(
    BaseAgent
):


    # Agent名称

    name = (
        "repository_analysis_agent"
    )



    description = (
        "Analyze repository information"
    )



    async def execute(
        self,
        context,
        input_data
    ):


        # 获取对应Skill

        skill = self.get_skill(

            "repository_analysis"

        )



        # 执行Skill

        result = await skill.execute(

            context,

            input_data

        )



        return result