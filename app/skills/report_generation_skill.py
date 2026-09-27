"""
Report Generation Skill。

负责生成第一版 Project Intelligence Report。
"""

import json

from app.skills.base import BaseSkill


class ReportGenerationSkill(
    BaseSkill
):
    """项目智能分析报告生成能力。"""

    name = "report_generation"

    description = (
        "Generate final GitHub project "
        "intelligence report."
    )

    async def execute(
        self,
        context,
        input_data: dict,
    ):
        exporter = context.tools.get(
            "report_export"
        )

        title = input_data.get(
            "title",
            "Repository Analysis Report",
        )

        filename = input_data.get(
            "filename",
            "repository_analysis.md",
        )

        content = self._build_report(
            input_data
        )

        if exporter is None:
            return {
                "report": {
                    "format": "markdown",
                    "content": content,
                }
            }

        report = await exporter.execute(
            title=title,
            content=content,
            filename=filename,
        )

        return {
            "report": report,
            "content": content,
        }

    @staticmethod
    def _build_report(
        data: dict,
    ) -> str:
        """生成第一版结构化项目报告。"""

        sections = []

        sections.append(
            ReportGenerationSkill._section(
                "01 项目概览",
                data.get(
                    "repository"
                ),
            )
        )

        sections.append(
            ReportGenerationSkill._section(
                "02 技术栈",
                data.get(
                    "technology_stack"
                )
                or data.get(
                    "technology_analysis_agent"
                ),
            )
        )

        sections.append(
            ReportGenerationSkill._section(
                "03 目录与源码结构",
                data.get(
                    "architecture"
                )
                or data.get(
                    "architecture_analysis_agent"
                ),
            )
        )

        sections.append(
            ReportGenerationSkill._section(
                "04 Agent 架构",
                data.get(
                    "executed_tasks"
                ),
            )
        )

        sections.append(
            ReportGenerationSkill._section(
                "05 Workflow",
                {
                    "executed_tasks": data.get(
                        "executed_tasks",
                        [],
                    ),
                    "research_plan": data.get(
                        "research_plan"
                    ),
                },
            )
        )

        sections.append(
            ReportGenerationSkill._section(
                "06 Skill",
                {
                    "repository_analysis": data.get(
                        "repository"
                    ),
                    "architecture_analysis": data.get(
                        "architecture"
                    ),
                    "technology_analysis": data.get(
                        "technology_stack"
                    ),
                },
            )
        )

        sections.append(
            ReportGenerationSkill._section(
                "07 Tool",
                {
                    "github_repository": (
                        "GitHub Repository Tool"
                    ),
                    "github_code_search": (
                        "GitHub Code Search Tool"
                    ),
                    "file_reader": (
                        "File Reader Tool"
                    ),
                    "dependency_analyzer": (
                        "Dependency Analyzer Tool"
                    ),
                    "qdrant_search": (
                        "Qdrant Search Tool"
                    ),
                    "report_export": (
                        "Report Export Tool"
                    ),
                },
            )
        )

        sections.append(
            ReportGenerationSkill._section(
                "08 RAG / Evidence",
                data.get(
                    "evidence"
                ),
            )
        )

        sections.append(
            ReportGenerationSkill._section(
                "09 Memory / Context",
                {
                    "context_enabled": True,
                    "memory_enabled": True,
                },
            )
        )

        sections.append(
            ReportGenerationSkill._section(
                "10 数据库",
                {
                    "database": (
                        data.get(
                            "technology_stack",
                            {},
                        ).get(
                            "database",
                            []
                        )
                        if isinstance(
                            data.get(
                                "technology_stack"
                            ),
                            dict,
                        )
                        else []
                    )
                },
            )
        )

        sections.append(
            ReportGenerationSkill._section(
                "11 Evidence",
                data.get(
                    "evidence"
                ),
            )
        )

        return "\n\n".join(
            sections
        )

    @staticmethod
    def _section(
        title: str,
        value,
    ) -> str:
        if value is None:
            value = "暂无数据"

        if isinstance(
            value,
            str,
        ):
            content = value
        else:
            content = json.dumps(
                value,
                ensure_ascii=False,
                indent=2,
                default=str,
            )

        return (
            f"## {title}\n\n"
            f"```text\n"
            f"{content}\n"
            f"```"
        )