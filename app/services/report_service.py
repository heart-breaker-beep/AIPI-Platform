"""
Report Service（Phase 14.2）。

职责
====

把分析结果投影成一份**结构化的报告文档**，
再按格式输出：

    Analysis 结果（state.data）
        ↓
    ReportService.build_document()
        ↓
    结构化 Report Document（可 JSON 序列化）
        ↓
    ├── to_markdown()  → 给人读的 markdown
    └── to_json()      → 给程序消费的 JSON

为什么要有这一层
================

文档 17.2 的要求是「不要让 Agent 自己负责文件生成」，
并明确 Report Service 应该接收 Structured Report Data。

在此之前，报告数据只有一种形态：
`ReportGenerationSkill._build_report()` 直接把
state.data 渲染成 markdown 字符串。
想拿 JSON 只能去解析 markdown，既脆又丢信息。

本模块补上中间那一层：一份**稳定、有版本号、
字段含义明确**的文档结构。
markdown 与 JSON 都从它派生，
两者描述的是同一份数据，不会漂移。

与 markdown 的分工
==================

markdown 渲染仍然由 ReportGenerationSkill 负责 ——
它包含表格排版、要点归纳、focus 展开/压缩等
大量呈现逻辑，不适合塞进这里。
本模块只负责**结构化投影**，不碰排版。

schema_version
==============

字段增删会破坏消费方，
因此文档带 schema_version。
当前为 1。
"""

import json
from datetime import datetime, timezone


class ReportService:
    """结构化报告文档的构建与序列化。"""

    SCHEMA_VERSION = 1

    # JSON 里最多保留多少条 evidence。
    #
    # 报告正文的 Evidence 章是全量的，
    # 但 JSON 常常被程序读进内存，
    # 需要有个上限。
    MAX_EVIDENCE = 200

    @classmethod
    def build_document(
        cls,
        data: dict,
        *,
        run_id=None,
        title=None,
    ) -> dict:
        """
        把分析结果投影成结构化报告文档。

        只做字段挑选与归一化，
        不渲染、不归纳、不改写内容 ——
        数值与文本原样透传。
        """

        if not isinstance(data, dict):
            data = {}

        from app.project_analysis.analysis_focus import (
            AnalysisFocus,
        )

        focus = AnalysisFocus.from_plan(
            data.get("research_plan")
        )

        return {
            "schema_version": cls.SCHEMA_VERSION,
            "generated_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "run_id": run_id or data.get("run_id"),
            "title": title or (
                "GitHub Project Intelligence Report"
            ),
            "question": data.get("question"),
            "focus": focus.to_dict(),
            "project": cls._project(data),
            "technology_stack": cls._as_dict(
                data.get("technology_stack")
            ),
            "directory": cls._directory(data),
            "modules": cls._modules(data),
            "dimensions": cls._dimensions(data),
            "evidence": cls._evidence(data),
            "synthesis": cls._synthesis(data),
            "report": cls._report_file(data),
        }

    # ------------------------------------------------------------------
    # 各区块
    # ------------------------------------------------------------------

    @staticmethod
    def _as_dict(value) -> dict:
        """只接受 dict。"""

        return value if isinstance(value, dict) else {}

    @classmethod
    def _project(cls, data: dict) -> dict:
        """项目概览：GitHub API 的真实元数据。"""

        repository = cls._as_dict(
            data.get("repository")
        )

        if not repository:
            return {
                "available": False,
                "reason": "未获取到仓库信息。",
            }

        license_info = repository.get("license")

        return {
            "available": True,
            "name": repository.get("name"),
            "full_name": repository.get(
                "full_name"
            ),
            "description": repository.get(
                "description"
            ),
            "language": repository.get("language"),
            "topics": repository.get("topics")
            or [],
            "stars": repository.get(
                "stargazers_count"
            ),
            "forks": repository.get(
                "forks_count"
            ),
            "open_issues": repository.get(
                "open_issues_count"
            ),
            "license": (
                license_info.get("name")
                if isinstance(license_info, dict)
                else None
            ),
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
            "url": repository.get("html_url"),
        }

    @classmethod
    def _directory(cls, data: dict) -> dict:
        """
        目录结构。

        PlanExecutorNode 会把它拍平到顶层，
        同时也留在 architecture_analysis_agent 里，
        两个位置都看。
        """

        directory = data.get("directory_structure")

        if not isinstance(directory, dict):

            architecture = cls._as_dict(
                data.get(
                    "architecture_analysis_agent"
                )
            )

            directory = architecture.get(
                "directory_structure"
            )

        if not isinstance(directory, dict):
            return {
                "available": False,
                "reason": "未获取到仓库文件树。",
            }

        return directory

    @classmethod
    def _modules(cls, data: dict) -> list:
        """
        采集到的源码文件清单。

        刻意**不带正文**：
        正文每个文件最多 1200 字符，
        20 个文件就是 20 多 KB，
        而 JSON 常被程序读进内存。
        需要正文时按 file_path 自己去取。
        """

        modules = data.get("modules")

        if not isinstance(modules, list):
            return []

        return [
            {
                "file_path": module.get(
                    "file_path"
                ),
                "start_line": module.get(
                    "start_line",
                    1,
                ),
                "truncated": bool(
                    module.get("truncated")
                ),
            }
            for module in modules
            if isinstance(module, dict)
            and module.get("file_path")
        ]

    @classmethod
    def _dimensions(cls, data: dict) -> dict:
        """
        六个维度（agents / workflow / ...）。

        字段与 project_structure.dimensions 一致，
        额外的 details 只保留结构化部分，
        去掉 source 源码片段（体积大且
        默认报告不渲染）。
        """

        structure = cls._as_dict(
            data.get("project_structure")
        )

        if not structure.get("available"):

            return {
                "_available": False,
                "_reason": structure.get("reason")
                or "未产出项目结构。",
            }

        dimensions = cls._as_dict(
            structure.get("dimensions")
        )

        result = {}

        for name, entry in dimensions.items():

            if not isinstance(entry, dict):
                continue

            result[name] = {
                "declared": bool(
                    entry.get("declared")
                ),
                "declared_by": entry.get(
                    "declared_by"
                ),
                "items": entry.get("items") or [],
                "topics": entry.get("topics") or [],
                "evidence": entry.get("evidence")
                or [],
                "code_evidence": entry.get(
                    "code_evidence"
                )
                or [],
                "reason": entry.get("reason"),
                "details": [
                    {
                        "kind": item.get("kind"),
                        "name": item.get("name"),
                        "signature": item.get(
                            "signature"
                        ),
                        "file_path": item.get(
                            "file_path"
                        ),
                        "line": item.get("line"),
                        "methods": item.get(
                            "methods"
                        )
                        or [],
                        "calls": item.get("calls")
                        or [],
                        "literals": item.get(
                            "literals"
                        )
                        or [],
                    }
                    for item in (
                        entry.get("details") or []
                    )
                    if isinstance(item, dict)
                ],
            }

        return result

    @classmethod
    def _evidence(cls, data: dict) -> list:
        """证据清单。"""

        evidence = data.get("evidence")

        if not isinstance(evidence, list):
            return []

        items = []

        for item in evidence[: cls.MAX_EVIDENCE]:

            if not isinstance(item, dict):
                continue

            items.append(
                {
                    "file_path": item.get(
                        "file_path"
                    ),
                    "line_start": item.get(
                        "line_start"
                    ),
                    "line_end": item.get(
                        "line_end"
                    ),
                    "source_type": item.get(
                        "source_type"
                    ),
                    "source_url": item.get(
                        "source_url"
                    ),
                    "verification_status": item.get(
                        "verification_status"
                    ),
                    "content": item.get("content"),
                }
            )

        return items

    @classmethod
    def _synthesis(cls, data: dict) -> dict:
        """LLM 综合判断。"""

        synthesis = cls._as_dict(
            data.get("synthesis")
        )

        if not synthesis:
            return {
                "available": False,
                "reason": "未产出综合分析。",
            }

        return {
            "available": bool(
                synthesis.get("available")
            ),
            "reason": synthesis.get("reason"),
            "summary": synthesis.get(
                "summary"
            )
            or {},
            "dimensions": synthesis.get(
                "dimensions"
            )
            or {},
        }

    @classmethod
    def _report_file(cls, data: dict) -> dict:
        """已落盘的报告文件信息。"""

        final_report = cls._as_dict(
            data.get("final_report")
        )

        inner = final_report.get("report")

        if isinstance(inner, dict):
            return inner

        return {}

    # ------------------------------------------------------------------
    # 输出
    # ------------------------------------------------------------------

    @classmethod
    def to_json(
        cls,
        document: dict,
    ) -> str:
        """序列化成 JSON 文本。"""

        return json.dumps(
            document,
            ensure_ascii=False,
            indent=2,
            default=str,
        )

    @classmethod
    def to_markdown(
        cls,
        data: dict,
    ) -> str:
        """
        渲染成 markdown。

        委托给 ReportGenerationSkill ——
        表格排版、要点归纳、focus 展开/压缩
        都在那里，本模块不重复实现。
        """

        from app.skills.report_generation_skill import (
            ReportGenerationSkill,
        )

        return ReportGenerationSkill._build_report(
            data
        )
