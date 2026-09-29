"""
Report Generation Skill。

负责生成 Project Intelligence Report。

Phase 12 文档 15.3 要求报告至少包含：

    项目概览 / 技术栈 / 目录结构 / Agent架构 / Workflow
    / Skill / Tool / RAG / Memory / 数据库 / 关键源码 / Evidence

本 Skill 的硬性约束：

- 所有章节内容都来自被分析项目的真实分析结果
- 取不到的章节必须明确写「真实数据不存在」并给出原因
- 不使用任何硬编码占位内容
  （旧版本曾把 AIPI 自己的 Tool 列表和
   {"context_enabled": true} 写进报告，
   那会让报告看起来完整但内容是假的）
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

    # 「关键源码」章节最多展示多少个文件。
    MAX_SOURCE_FILES = 8

    # 每个源码文件最多展示多少字符。
    SOURCE_EXCERPT_CHARS = 800

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

    @classmethod
    def _build_report(
        cls,
        data: dict,
    ) -> str:
        """
        按 Phase 12 文档 15.3 生成报告。

        章节顺序与文档一致，内容全部来自真实数据。
        """

        technology_stack = data.get(
            "technology_stack"
        )

        if not isinstance(
            technology_stack,
            dict,
        ):
            technology_stack = {}

        architecture = (
            data.get("architecture")
            or data.get(
                "architecture_analysis_agent"
            )
        )

        if not isinstance(
            architecture,
            dict,
        ):
            architecture = {}

        project_structure = data.get(
            "project_structure"
        )

        if not isinstance(
            project_structure,
            dict,
        ):
            project_structure = {}

        sections = [
            cls._section(
                "01 项目概览",
                cls._project_overview(data),
            ),

            cls._section(
                "02 技术栈",
                technology_stack
                or cls._missing(
                    "真实数据不存在"
                    "（Technology Agent 未产出 "
                    "technology_stack）。"
                ),
            ),

            cls._section(
                "03 目录结构",
                architecture.get(
                    "directory_structure"
                )
                or cls._missing(
                    "真实数据不存在"
                    "（未获取到仓库文件树）。"
                ),
            ),

            cls._section(
                "04 Agent 架构",
                cls._structure_dimension(
                    project_structure,
                    "agents",
                ),
            ),

            cls._section(
                "05 Workflow",
                cls._structure_dimension(
                    project_structure,
                    "workflow",
                ),
            ),

            cls._section(
                "06 Skill",
                cls._structure_dimension(
                    project_structure,
                    "skills",
                ),
            ),

            cls._section(
                "07 Tool",
                cls._structure_dimension(
                    project_structure,
                    "tools",
                ),
            ),

            cls._section(
                "08 RAG",
                cls._rag_dimension(
                    project_structure,
                    technology_stack,
                ),
            ),

            cls._section(
                "09 Memory",
                cls._structure_dimension(
                    project_structure,
                    "memory",
                ),
            ),

            cls._section(
                "10 数据库",
                {
                    "database": technology_stack.get(
                        "database",
                        [],
                    ),
                    "source": (
                        "workflow_state.data."
                        "technology_stack.database"
                    ),
                }
                if technology_stack
                else cls._missing(
                    "真实数据不存在"
                    "（未产出 technology_stack）。"
                ),
            ),

            cls._section(
                "11 关键源码",
                cls._source_excerpts(
                    architecture
                ),
            ),

            cls._section(
                "12 Evidence",
                data.get("evidence")
                or cls._missing(
                    "真实数据不存在"
                    "（Evidence Agent 未产出证据）。"
                ),
            ),
        ]

        return "\n\n".join(
            sections
        )

    @staticmethod
    def _missing(
        reason: str,
    ) -> dict:
        """统一的「真实数据不存在」表示。"""

        return {
            "available": False,
            "reason": reason,
        }

    @staticmethod
    def _project_overview(
        data: dict,
    ) -> dict:
        """项目概览：来自 GitHub API 的真实仓库信息。"""

        repository = data.get(
            "repository"
        )

        if (
            not isinstance(repository, dict)
            or not repository
        ):
            return ReportGenerationSkill._missing(
                "真实数据不存在"
                "（未获取到仓库信息）。"
            )

        license_info = repository.get(
            "license"
        )

        license_name = None

        if isinstance(
            license_info,
            dict,
        ):
            license_name = license_info.get(
                "name"
            )

        return {
            "name": repository.get(
                "name"
            ),
            "full_name": repository.get(
                "full_name"
            ),
            "description": repository.get(
                "description"
            ),
            "language": repository.get(
                "language"
            ),
            "topics": repository.get(
                "topics"
            ),
            "stars": repository.get(
                "stargazers_count"
            ),
            "forks": repository.get(
                "forks_count"
            ),
            "open_issues": repository.get(
                "open_issues_count"
            ),
            "license": license_name,
            "default_branch": repository.get(
                "default_branch"
            ),
            "size_kb": repository.get("size"),
            "created_at": repository.get(
                "created_at"
            ),
            "pushed_at": repository.get(
                "pushed_at"
            ),
            "html_url": repository.get(
                "html_url"
            ),
            "readme_characters": len(
                data.get("readme") or ""
            ),
        }

    @staticmethod
    def _structure_dimension(
        project_structure: dict,
        name: str,
    ) -> dict:
        """
        从 project_structure 取出某个维度的可读内容。

        该结构来自被分析项目的 README 与 GitHub topics，
        每条都带 README 行号，可人工复核。
        """

        if not project_structure.get(
            "available"
        ):
            return ReportGenerationSkill._missing(
                project_structure.get("reason")
                or (
                    "真实数据不存在"
                    "（未产出被分析项目的自述结构）。"
                )
            )

        entry = (
            project_structure.get(
                "dimensions"
            )
            or {}
        ).get(name)

        if not isinstance(entry, dict):
            return ReportGenerationSkill._missing(
                "真实数据不存在"
                f"（无 {name} 维度）。"
            )

        if not entry.get("declared"):
            return ReportGenerationSkill._missing(
                entry.get("reason")
                or (
                    "被分析项目未声明该能力"
                    "（README / topics 中没有相关描述）。"
                )
            )

        return {
            "items": entry.get("items") or [],
            "topics": entry.get("topics") or [],
            "evidence": [
                {
                    "file": item.get("file_path"),
                    "line": item.get("line_start"),
                    "text": item.get("text"),
                }
                for item in (
                    entry.get("evidence") or []
                )
            ],
        }

    @staticmethod
    def _rag_dimension(
        project_structure: dict,
        technology_stack: dict,
    ) -> dict:
        """
        RAG 章节。

        README 自述的 rag 信号是主要来源；
        technology_stack.embedding 只是
        「是否检测到向量库」的辅助信息，
        不能单独代表完整的 RAG 实现。
        """

        declared = ReportGenerationSkill._structure_dimension(
            project_structure,
            "rag",
        )

        embedding = technology_stack.get(
            "embedding",
            [],
        )

        if declared.get("available"):

            declared["vector_store_detected"] = (
                embedding
            )

            return declared

        return {
            "available": False,
            "reason": declared.get("reason"),
            "vector_store_detected": embedding,
        }

    @classmethod
    def _source_excerpts(
        cls,
        architecture: dict,
    ) -> str:
        """关键源码：展示真实读取到的源码片段。"""

        modules = architecture.get(
            "modules"
        )

        if not isinstance(modules, list) or not modules:
            return json.dumps(
                cls._missing(
                    "真实数据不存在"
                    "（未读取到任何源码文件）。"
                ),
                ensure_ascii=False,
                indent=2,
            )

        lines = []

        for module in modules[
            : cls.MAX_SOURCE_FILES
        ]:

            if not isinstance(module, dict):
                continue

            file_path = module.get(
                "file_path"
            )

            error = module.get("error")

            if error:

                lines.append(
                    f"{file_path}\n"
                    f"  [读取失败] {error}\n"
                )

                continue

            content = str(
                module.get("content") or ""
            )

            if not content.strip():
                continue

            excerpt = content[
                : cls.SOURCE_EXCERPT_CHARS
            ]

            suffix = (
                "  ...[已截断]"
                if len(content)
                > cls.SOURCE_EXCERPT_CHARS
                else ""
            )

            lines.append(
                f"{file_path}"
                f"  ({len(content)} 字符)\n"
                f"{excerpt}{suffix}\n"
            )

        if not lines:
            return json.dumps(
                cls._missing(
                    "真实数据不存在"
                    "（读取到的源码文件为空）。"
                ),
                ensure_ascii=False,
                indent=2,
            )

        return "\n".join(lines)

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
