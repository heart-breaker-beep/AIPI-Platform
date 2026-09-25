"""
Report Generation Skill


负责生成最终分析报告。


输入:

多个Skill / Agent分析结果


输出:

报告内容


"""


from app.skills.base import BaseSkill




class ReportGenerationSkill(
    BaseSkill
):
    """
    报告生成能力。
    """



    name = "report_generation"



    description = (
        "Generate final repository analysis report"
    )



    async def execute(
        self,
        context,
        input_data: dict
    ):
        """
        执行报告生成。


        input_data:

        {
            "repository": {},
            "architecture": {},
            "technology": {}
        }

        """


        # 获取报告导出工具

        exporter = (
            context.tools.get(
                "report_export"
            )
        )


        # 如果还没有接入真实导出工具

        # 返回结构化结果

        if exporter is None:

            return {


                "report":

                    input_data


            }

        report = await exporter.execute(

            data=input_data

        )
        return {


            "report":

                report

        }