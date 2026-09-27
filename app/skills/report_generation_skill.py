"""
Report Generation Skill。

负责生成最终分析报告。
"""

import json

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
        input_data: dict,
    ):
        """
        input_data：

        {
            "repository": {},
            "architecture": {},
            "technology": {}
        }
        """

        exporter = context.tools.get(
            "report_export"
        )

        # 没有导出工具时，
        # 仍返回结构化报告数据。
        if exporter is None:
            return {
                "report": input_data
            }

        title = input_data.get(
            "title",
            "Repository Analysis Report",
        )

        filename = input_data.get(
            "filename",
            "repository_analysis.md",
        )

        content = input_data.get(
            "content"
        )

        if not isinstance(
            content,
            str,
        ):
            content = json.dumps(
                input_data,
                ensure_ascii=False,
                indent=2,
                default=str,
            )

        report = await exporter.execute(
            title=title,
            content=content,
            filename=filename,
        )

        return {
            "report": report
        }