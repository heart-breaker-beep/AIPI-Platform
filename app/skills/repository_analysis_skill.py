"""
Repository Analysis Skill


负责分析 GitHub 项目基础信息。


执行流程:

RepositoryAnalysisSkill

        |
        |
        +---- GitHub Repository Tool
        |
        +---- File Reader Tool
        |
        +---- Dependency Analyzer Tool



输出:

{
    repository:{},

    readme:{},

    dependencies:{}

}

"""


from app.skills.base import BaseSkill




class RepositoryAnalysisSkill(
    BaseSkill
):


    # Skill名称

    name = "repository_analysis"



    description = (
        "Analyze github repository information"
    )



    async def execute(
        self,
        context,
        input_data
    ):
        """
        执行仓库分析。


        input_data:

        {
            "owner":"xxx",
            "repo":"xxx"
        }

        """


        result = {}



        # 从Context中获取工具

        github_tool = (
            context.tools[
                "github_repository"
            ]
        )


        file_reader = (
            context.tools[
                "file_reader"
            ]
        )


        dependency_tool = (
            context.tools[
                "dependency_analyzer"
            ]
        )



        # 获取仓库基本信息

        result["repository"] = (
            await github_tool.execute(
                **input_data
            )
        )



        # 获取README内容

        result["readme"] = (
            await file_reader.execute(

                **input_data,

                path="README.md"

            )
        )



        # 分析项目依赖

        result["dependencies"] = (
            await dependency_tool.execute(
                **input_data
            )
        )



        return result