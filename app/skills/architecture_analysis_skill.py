"""
Architecture Analysis Skill


负责分析项目代码结构。


主要分析:

- 文件结构
- 模块关系
- 核心代码


依赖:

Code Search Tool

File Reader Tool

"""


from app.skills.base import BaseSkill




class ArchitectureAnalysisSkill(
    BaseSkill
):


    name = "architecture_analysis"



    description = (
        "Analyze repository architecture"
    )



    async def execute(
        self,
        context,
        input_data
    ):


        # 获取代码搜索工具

        code_search = (
            context.tools[
                "github_code_search"
            ]
        )


        file_reader = (
            context.tools[
                "file_reader"
            ]
        )



        # 搜索项目文件

        files = await code_search.execute(
            **input_data
        )



        architecture = {

            "files": files,

            "modules":[]

        }



        # 读取代码内容

        for file in files:


            content = await file_reader.execute(

                **input_data,

                path=file

            )


            architecture[
                "modules"
            ].append(
                content
            )



        return architecture