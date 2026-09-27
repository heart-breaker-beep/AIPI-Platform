"""
Technology Analysis Skill。

负责分析项目技术栈。
"""

from app.skills.base import BaseSkill


class TechnologyAnalysisSkill(
    BaseSkill
):
    """
    分析项目技术栈。
    """

    name = "technology_analysis"

    description = (
        "Analyze technology stack"
    )

    async def execute(
        self,
        context,
        input_data,
    ):
        dependency_tool = (
            context.tools.get(
                "dependency_analyzer"
            )
        )

        if dependency_tool is None:
            raise RuntimeError(
                "Tool not found: dependency_analyzer"
            )

        project_path = input_data.get(
            "project_path"
        )

        if not project_path:
            raise ValueError(
                "Technology analysis requires "
                "'project_path'."
            )

        dependencies = (
            await dependency_tool.execute(
                project_path=project_path,
            )
        )

        return {
            "technology_stack": dependencies
        }