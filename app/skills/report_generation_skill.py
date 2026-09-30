"""
Report Generation Skill。

负责生成 Project Intelligence Report。

Phase 12 文档 15.3 要求报告至少包含：

    项目概览 / 技术栈 / 目录结构 / Agent架构 / Workflow
    / Skill / Tool / RAG / Memory / 数据库 / 关键源码 / Evidence

实际产出调整为：

    00 结论摘要 + 01-11 章

改动与原因：

  关键源码章已移除
      它展示的是每个文件开头的固定字符数，
      而 Python 文件开头必然是 import 块，
      渲染出来只有一堆 import，对理解项目没有帮助。

  04-09 章跟随「本次重点」展开或压缩
      用户在问题里点名了某个模块时
      （例如「分析项目的 agent」），
      重点章展开实现明细，
      其余章压成一行要点并注明未展开 ——
      否则把每章都铺开写一遍，重点就被淹没了。

各章末尾的「综合判断」来自 ReportSynthesisSkill
（由 LLM 基于已采集事实归纳，只归纳不推测）。

渲染方式
========

01-12 章由本 Skill 确定性地渲染成 markdown
（表格 / 列表 / 带语言标注的代码块），
不再把中间数据结构 dump 成 JSON。

这样做的好处：

- 数值仍是一字不改的真实数据，可逐条复核；
- 不经过 LLM，
  因此 LLM 不可用时报告依然完整可读，
  也不存在幻觉面。

每个字段的取值都来自各 Agent 的真实产出，
渲染层只负责排版，不补充、不推断任何信息。

本 Skill 的硬性约束：

- 所有章节内容都来自被分析项目的真实分析结果
- 取不到的章节必须明确写「真实数据不存在」并给出原因
- 不使用任何硬编码占位内容
  （旧版本曾把 AIPI 自己的 Tool 列表和
   {"context_enabled": true} 写进报告，
   那会让报告看起来完整但内容是假的）
- 「综合判断」不可用时静默省略，
  原始数据章节必须完整保留
"""

import json
import re

from app.project_analysis.analysis_focus import (
    AnalysisFocus,
)
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

    # 维度章节 -> 综合分析里的维度名。
    #
    # 章标题里的名字（Agent 架构 / Skill）
    # 与综合分析里的名字（agents / skills）
    # 不一致，且顺序需要显式固定，
    # 因此用一张表对应起来。
    DIMENSION_SECTIONS = (
        ("04 Agent 架构", "agents"),
        ("05 Workflow", "workflow"),
        ("06 Skill", "skills"),
        ("07 Tool", "tools"),
        ("08 RAG", "rag"),
        ("09 Memory", "memory"),
    )

    # 结论摘要各小节的展示名。
    SUMMARY_FIELDS = (
        ("core_design", "核心设计"),
        ("technology_choices", "技术选型"),
        ("highlights", "亮点"),
        ("risks", "风险与缺口"),
        ("use_cases", "适用场景"),
    )

    # 支持的输出格式。
    #
    #   markdown  只出 markdown（旧行为）
    #   both      再加一份结构化 JSON
    #
    # 默认仍是 markdown，避免改变既有调用方的行为。
    SUPPORTED_FORMATS = ("markdown", "both")

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

        fmt = input_data.get("format", "markdown")

        if fmt not in self.SUPPORTED_FORMATS:
            fmt = "markdown"

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

        # markdown 始终产出 ——
        # 它是给人读的主产物，
        # JSON 只是额外的一份结构化导出。
        report = await exporter.execute(
            title=title,
            content=content,
            filename=filename,
        )

        result = {
            "report": report,
            "content": content,
        }

        if fmt == "both":

            result["json_report"] = (
                await self._export_json(
                    exporter,
                    input_data,
                    title,
                    filename,
                )
            )

        return result

    @staticmethod
    async def _export_json(
        exporter,
        input_data: dict,
        title: str,
        filename: str,
    ):
        """
        额外导出一份结构化报告（Phase 14.2）。

        document 只放文件路径与格式，不放正文 ——
        正文进 state 会把 checkpoint 撑大，
        那是之前修过的坑。
        """

        from app.services.report_service import (
            ReportService,
        )

        export_json = getattr(
            exporter,
            "export_json",
            None,
        )

        if not callable(export_json):

            return {
                "available": False,
                "reason": (
                    "当前 report_export 工具"
                    "不支持 JSON 导出。"
                ),
            }

        document = ReportService.build_document(
            input_data,
            run_id=input_data.get("run_id"),
            title=title,
        )

        json_filename = (
            filename.rsplit(".", 1)[0] + ".json"
            if "." in filename
            else filename + ".json"
        )

        exported = await export_json(
            document,
            json_filename,
        )

        exported["available"] = True

        return exported

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

        # 综合分析结论。
        #
        # 不可用时为 None，
        # 此时 00 章仍会渲染，
        # 但内容明确写「综合分析不可用」与原因，
        # 而不是让这一章凭空消失
        # （消失会让人误以为报告本来就没有结论层）。
        synthesis = data.get("synthesis")

        if not isinstance(
            synthesis,
            dict,
        ):
            synthesis = {}

        # 用于在各章末尾给出深挖接口的调用地址。
        # 拿不到时渲染成 {run_id} 占位。
        run_id = data.get("run_id")

        # 本次分析的重点维度。
        #
        # research_plan 里带 focus；
        # 旧 run 没有该字段时 from_plan 会退回
        # 用 question 做关键词匹配。
        focus = AnalysisFocus.from_plan(
            data.get("research_plan")
        )

        sections = [
            cls._summary_section(
                synthesis,
                question=data.get("question"),
                focus=focus,
            ),

            cls._section(
                "01 项目概览",
                cls._overview_markdown(
                    cls._project_overview(data)
                ),
            ),

            cls._section(
                "02 技术栈",
                cls._technology_markdown(
                    technology_stack
                ),
            ),

            cls._section(
                "03 目录结构",
                cls._directory_markdown(
                    # PlanExecutorNode 会把
                    # architecture 的产出拍平到顶层，
                    # 因此两个位置都要看。
                    architecture.get(
                        "directory_structure"
                    )
                    or data.get(
                        "directory_structure"
                    )
                ),
            ),

            cls._section_with_judgment(
                "04 Agent 架构",
                cls._dimension_markdown(
                    cls._structure_dimension(
                        project_structure,
                        "agents",
                    ),
                    dimension="agents",
                    run_id=run_id,
                    focus=focus,
                ),
                synthesis,
                "agents",
            ),

            cls._section_with_judgment(
                "05 Workflow",
                cls._dimension_markdown(
                    cls._structure_dimension(
                        project_structure,
                        "workflow",
                    ),
                    dimension="workflow",
                    run_id=run_id,
                    focus=focus,
                ),
                synthesis,
                "workflow",
            ),

            cls._section_with_judgment(
                "06 Skill",
                cls._dimension_markdown(
                    cls._structure_dimension(
                        project_structure,
                        "skills",
                    ),
                    dimension="skills",
                    run_id=run_id,
                    focus=focus,
                ),
                synthesis,
                "skills",
            ),

            cls._section_with_judgment(
                "07 Tool",
                cls._dimension_markdown(
                    cls._structure_dimension(
                        project_structure,
                        "tools",
                    ),
                    dimension="tools",
                    run_id=run_id,
                    focus=focus,
                ),
                synthesis,
                "tools",
            ),

            cls._section_with_judgment(
                "08 RAG",
                cls._dimension_markdown(
                    cls._rag_dimension(
                        project_structure,
                        technology_stack,
                    ),
                    dimension="rag",
                    run_id=run_id,
                    focus=focus,
                ),
                synthesis,
                "rag",
            ),

            cls._section_with_judgment(
                "09 Memory",
                cls._dimension_markdown(
                    cls._structure_dimension(
                        project_structure,
                        "memory",
                    ),
                    dimension="memory",
                    run_id=run_id,
                    focus=focus,
                ),
                synthesis,
                "memory",
            ),

            cls._section(
                "10 数据库",
                cls._database_markdown(
                    technology_stack
                ),
            ),

            # 「关键源码」章已移除。
            #
            # 它展示的是每个文件开头的固定字符数，
            # 而 Python 文件开头必然是 import 块 ——
            # 实际渲染出来就是一堆
            # `import sqlite3` / `from decimal import Decimal`，
            # 对理解项目没有任何帮助。
            # 想看真实实现请看各模块章的「证据锚点」，
            # 或对该模块做深挖。

            cls._section(
                "11 Evidence",
                cls._evidence_markdown(
                    data.get("evidence")
                ),
            ),
        ]

        return "\n\n".join(
            sections
        )

    # ------------------------------------------------------------------
    # 通用渲染工具
    # ------------------------------------------------------------------

    @staticmethod
    def _text(value) -> str:
        """把任意标量渲染成表格里的一个值。"""

        if value is None:
            return "—"

        if isinstance(value, bool):
            return "是" if value else "否"

        if isinstance(
            value,
            (list, tuple),
        ):
            items = [
                str(item).strip()
                for item in value
                if str(item).strip()
            ]

            return ", ".join(items) if items else "—"

        text = str(value).strip()

        return text or "—"

    @staticmethod
    def _table(
        headers: list,
        rows: list,
    ) -> str:
        """渲染 markdown 表格。"""

        lines = [
            "| "
            + " | ".join(headers)
            + " |",
            "| "
            + " | ".join(
                "---" for _ in headers
            )
            + " |",
        ]

        for row in rows:

            lines.append(
                "| "
                + " | ".join(
                    str(cell) for cell in row
                )
                + " |"
            )

        return "\n".join(lines)

    @staticmethod
    def _bullets(items: list) -> str:
        """渲染 markdown 无序列表。"""

        return "\n".join(
            f"- {item}" for item in items
        )

    @staticmethod
    def _is_missing(value) -> bool:
        """判断是否为 _missing() 产出的「数据不存在」标记。"""

        return (
            isinstance(value, dict)
            and value.get("available") is False
            and "reason" in value
        )

    @classmethod
    def _missing_text(
        cls,
        reason: str,
    ) -> str:
        """
        渲染「数据不存在」。

        原因文本原样输出：
        它是报告里唯一说明「为什么没有」的线索。
        """

        return reason

    # ------------------------------------------------------------------
    # 各章渲染
    # ------------------------------------------------------------------

    @classmethod
    def _overview_markdown(
        cls,
        overview: dict,
    ) -> str:
        """01 项目概览：字段表格。"""

        if cls._is_missing(overview):
            return cls._missing_text(
                overview["reason"]
            )

        rows = [
            (
                "项目全名",
                cls._text(
                    overview.get("full_name")
                ),
            ),
            (
                "描述",
                cls._text(
                    overview.get("description")
                ),
            ),
            (
                "主语言",
                cls._text(
                    overview.get("language")
                ),
            ),
            (
                "Topics",
                cls._text(
                    overview.get("topics")
                ),
            ),
            (
                "Stars / Forks",
                (
                    f"{cls._text(overview.get('stars'))}"
                    " / "
                    f"{cls._text(overview.get('forks'))}"
                ),
            ),
            (
                "Open Issues",
                cls._text(
                    overview.get("open_issues")
                ),
            ),
            (
                "License",
                cls._text(
                    overview.get("license")
                ),
            ),
            (
                "默认分支",
                cls._text(
                    overview.get(
                        "default_branch"
                    )
                ),
            ),
            (
                "仓库体积",
                (
                    f"{cls._text(overview.get('size_kb'))}"
                    " KB"
                ),
            ),
            (
                "创建 / 最近推送",
                (
                    f"{cls._text(overview.get('created_at'))}"
                    " / "
                    f"{cls._text(overview.get('pushed_at'))}"
                ),
            ),
            (
                "README 字符数",
                cls._text(
                    overview.get(
                        "readme_characters"
                    )
                ),
            ),
            (
                "地址",
                cls._text(
                    overview.get("html_url")
                ),
            ),
        ]

        return cls._table(
            ["字段", "值"],
            rows,
        )

    @classmethod
    def _technology_markdown(
        cls,
        technology_stack: dict,
    ) -> str:
        """
        02 技术栈：分类表格。

        技术栈是「把若干配置文件拼成一个大字符串
        再做子串匹配」得到的，
        因此无法把某一项准确归到某一个文件，
        这里只列出「检测依据」扫过哪些文件，
        不编造逐项的文件归属。
        """

        if not technology_stack:
            return cls._missing_text(
                "真实数据不存在"
                "（Technology Agent 未产出 "
                "technology_stack）。"
            )

        labels = (
            ("frameworks", "框架"),
            ("llm", "LLM"),
            ("database", "数据库"),
            ("embedding", "Embedding"),
            ("deployment", "部署"),
        )

        rows = []

        for key, label in labels:

            values = technology_stack.get(
                key
            )

            if isinstance(
                values,
                (list, tuple),
            ) and values:

                rendered = ", ".join(
                    str(item)
                    for item in values
                )

            else:

                rendered = "未检测到"

            rows.append((label, rendered))

        blocks = [
            cls._table(
                ["类别", "检测结果"],
                rows,
            )
        ]

        source_files = technology_stack.get(
            "source_files"
        )

        if source_files:

            blocks.append(
                "**检测依据**（以下文件被读取后做关键词匹配）："
                "\n\n"
                + cls._bullets(
                    f"`{path}`"
                    for path in source_files
                )
            )

        failures = technology_stack.get(
            "read_failures"
        )

        if isinstance(failures, dict) and failures:

            blocks.append(
                "**读取失败**：\n\n"
                + cls._bullets(
                    f"`{path}` — {reason}"
                    for path, reason
                    in failures.items()
                )
            )

        return "\n\n".join(blocks)

    @classmethod
    def _directory_markdown(
        cls,
        directory,
    ) -> str:
        """03 目录结构：文件数 + 顶层目录表 + 关键文件。"""

        if not isinstance(
            directory,
            dict,
        ) or not directory.get("available"):

            return cls._missing_text(
                "真实数据不存在"
                "（未获取到仓库文件树）。"
            )

        blocks = [
            f"共 {cls._text(directory.get('total_files'))} 个文件。"
        ]

        top_level = directory.get(
            "top_level_dirs"
        )

        if isinstance(top_level, list) and top_level:

            blocks.append(
                cls._table(
                    ["顶层目录", "文件数"],
                    [
                        (
                            cls._text(
                                item.get("name")
                            ),
                            cls._text(
                                item.get(
                                    "file_count"
                                )
                            ),
                        )
                        for item in top_level
                        if isinstance(item, dict)
                    ],
                )
            )

        by_extension = directory.get(
            "by_extension"
        )

        if isinstance(
            by_extension,
            dict,
        ) and by_extension:

            blocks.append(
                "**按文件类型**\n\n"
                + cls._table(
                    ["扩展名", "文件数"],
                    [
                        (
                            cls._text(name),
                            cls._text(count),
                        )
                        for name, count
                        in by_extension.items()
                    ],
                )
            )

        key_files = directory.get(
            "key_files"
        )

        if isinstance(key_files, list) and key_files:

            blocks.append(
                "**关键文件**\n\n"
                + cls._bullets(
                    f"`{path}`"
                    for path in key_files
                )
            )

        return "\n\n".join(blocks)

    # 结论来源 -> 展示文案。
    DECLARED_BY_LABELS = {
        "code": "代码证据",
        "readme": "README 自述",
        "code+readme": "代码证据 + README 自述",
    }

    # 默认报告每章最多几条要点 / 几条证据锚点。
    #
    # 默认报告是「概览」，不是「实现说明书」：
    # 只给要点与可回溯的锚点，
    # 具体某个模块想知道更多时走深挖。
    MAX_HIGHLIGHTS = 6

    MAX_ANCHORS = 5

    # 证据锚点里最多留给 README 出处的名额。
    MAX_README_ANCHORS = 2

    # 单条要点里最多列几个名字。
    MAX_NAMES_PER_HIGHLIGHT = 8

    @classmethod
    def _dimension_markdown(
        cls,
        entry: dict,
        dimension: str,
        run_id=None,
        focus=None,
    ) -> str:
        """
        04-09 的维度章。

        三种渲染形态：

            无重点（focus 为空）
                全量等深：要点 + 证据锚点 + 深挖指引

            本次重点维度
                再加「实现明细」（签名 / 调用链 / 关键常量）

            本次非重点维度
                压成一行要点 + 一句未展开说明

        为什么要有第三种：用户问「分析这个项目的 agent」
        时，把 05-09 章都铺开写一遍，
        重点就被淹没了 ——
        这正是「报告里还是什么都有」的来源。
        """

        if cls._is_missing(entry):
            return cls._missing_text(
                entry["reason"]
            )

        focused = (
            focus is not None
            and focus.is_focused
        )

        if focused and not focus.is_primary(
            dimension
        ):

            return cls._compressed_markdown(
                entry,
                dimension,
                run_id,
                focus,
            )

        blocks = []

        declared_by = entry.get(
            "declared_by"
        )

        if declared_by:

            blocks.append(
                "**结论来源**："
                + cls.DECLARED_BY_LABELS.get(
                    declared_by,
                    declared_by,
                )
            )

        highlights = cls._highlights(entry)

        if highlights:

            blocks.append(
                "**要点**\n\n"
                + cls._bullets(highlights)
            )

        else:

            blocks.append(
                "**要点**\n\n未抽取到结构化条目。"
            )

        topics = entry.get("topics")

        if isinstance(topics, list) and topics:

            blocks.append(
                "**命中的 GitHub topics**："
                + ", ".join(
                    f"`{topic}`"
                    for topic in topics
                )
            )

        # RAG 章额外带上向量库检测结果。
        vector_store = entry.get(
            "vector_store_detected"
        )

        if isinstance(
            vector_store,
            list,
        ):

            blocks.append(
                "**检测到的向量库**："
                + (
                    ", ".join(vector_store)
                    if vector_store
                    else (
                        "未检测到"
                        "（当前只识别 qdrant / "
                        "chromadb）"
                    )
                )
            )

        anchors = cls._anchors(entry)

        if anchors:

            blocks.append(
                "**证据锚点**\n\n"
                + cls._bullets(anchors)
            )

        details = entry.get("details")

        # 报告里实际展开了多少条明细。
        # 0 表示没展开（非重点维度或没有明细），
        # 深挖指引的措辞要据此区分。
        shown_count = 0

        # 本次重点维度：把实现明细展开在报告里。
        #
        # 非重点维度不展开 ——
        # 它们已经走 _compressed_markdown 提前返回了。
        if (
            focused
            and focus.is_primary(dimension)
            and isinstance(details, list)
            and details
        ):

            rendered = [
                cls._detail_markdown(item)
                for item in details
                if isinstance(item, dict)
            ]

            rendered = [
                item for item in rendered if item
            ]

            if rendered:

                shown_count = len(rendered)

                blocks.append(
                    "**实现明细**\n\n"
                    + "\n\n".join(rendered)
                )

        detail_count = len(
            entry.get("details") or []
        )

        if detail_count:

            blocks.append(
                cls._deep_dive_hint(
                    dimension,
                    detail_count,
                    run_id,
                    shown_count=shown_count,
                )
            )

        return "\n\n".join(blocks)

    @classmethod
    def _compressed_markdown(
        cls,
        entry: dict,
        dimension: str,
        run_id,
        focus,
    ) -> str:
        """
        非重点维度的压缩形态。

        只留一行要点与一句说明 ——
        不是删掉这一章（那会让报告缺章），
        而是把它压到「知道有这回事」的程度。
        """

        highlights = cls._highlights(entry)

        summary = (
            "；".join(highlights)
            if highlights
            else "未抽取到结构化条目。"
        )

        if run_id:

            hint = (
                "> 查看完整内容与实现明细："
                f"`POST /analysis/{run_id}/deep-dive"
                f"?module={dimension}`"
            )

        else:

            hint = (
                "> 查看完整内容："
                "`reports/{run_id}_analysis.md`"
            )

        return (
            f"本次未展开。要点：{summary}\n\n"
            "> 本次分析的重点是 "
            + "、".join(focus.titles())
            + "，该模块未按问题展开。\n"
            ">\n"
            f"{hint}"
        )

    @classmethod
    def _scope_note(
        cls,
        question,
        focus,
    ) -> str:
        """
        报告开头的「本次问题 / 重点」抬头。

        必须写清楚，否则用户无法判断
        报告为什么有的章详细、有的章只有一行。
        """

        lines = []

        if isinstance(
            question,
            str,
        ) and question.strip():

            lines.append(
                "**本次问题**："
                + question.strip()
            )

        if focus is not None and focus.is_focused:

            lines.append(
                "**本次重点**："
                + "、".join(focus.titles())
                + "（这几个模块展开，其余压缩）"
            )

            if focus.notes:

                lines.append(
                    "**关注点**："
                    + focus.notes
                )

        if not lines:
            return ""

        return "\n\n".join(lines) + "\n\n"

    @classmethod
    def _deep_dive_hint(
        cls,
        dimension: str,
        detail_count: int,
        run_id,
        shown_count: int = 0,
    ) -> str:
        """
        指向该模块深挖报告的指引。

        detail_count 是采集到的明细总数。
        本次重点维度已经在报告里展开了，
        措辞要跟着变 ——
        否则会出现「刚展示完明细，
        下一行又说这些明细未放入报告」的矛盾。
        """

        target = (
            f"/analysis/{run_id}/deep-dive"
            if run_id
            else "/analysis/{run_id}/deep-dive"
        )

        if shown_count:

            return (
                "> 以上为本次展开的实现明细。"
                "**源码片段**与其余明细见深挖：\n"
                ">\n"
                f"> `POST {target}"
                f"?module={dimension}`"
            )

        return (
            "> 本模块另有 "
            f"{detail_count} 项实现明细"
            "（函数签名 / 调用链 / 关键常量 / 源码片段），"
            "未放入本报告。\n"
            ">\n"
            f"> 查看方式：`POST {target}"
            f"?module={dimension}`"
        )

    # 要点分组的展示顺序与名称。
    #
    # 顺序即优先级：
    # 图结构与类最能说明一个模块在做什么，
    # 依赖与目录只是旁证。
    HIGHLIGHT_GROUPS = (
        # 叫「图结构」而不是「图节点」：
        # 这一组里既有 StateGraph 构造，
        # 也有 add_node / add_edge，
        # 统称节点会与 add_node 的节点名混起来。
        ("graph", "图结构"),
        ("class", "类"),
        ("function", "函数"),
        ("import", "依赖"),
        ("path", "目录"),
        ("readme", "README 自述"),
    )

    @classmethod
    def _highlights(cls, entry: dict) -> list:
        """
        把扁平条目归纳成「要点」。

        条目是原始符号（`builder.add_node('x', ...)` /
        `class BaseAgent(ABC)` / `路径 src/app/agents/`），
        直接列出来只是堆符号；
        按类别归并并计数之后才是要点。

        纯字符串处理，不经过 LLM。
        """

        items = entry.get("items")

        if not isinstance(items, list):
            return []

        grouped = {
            key: []
            for key, _ in cls.HIGHLIGHT_GROUPS
        }

        for item in items:

            text = str(item).strip()

            if not text:
                continue

            grouped[
                cls._highlight_group(text)
            ].append(text)

        highlights = []

        for key, label in cls.HIGHLIGHT_GROUPS:

            values = grouped[key]

            if not values:
                continue

            highlights.append(
                cls._highlight_line(
                    label,
                    key,
                    values,
                )
            )

            if len(highlights) >= cls.MAX_HIGHLIGHTS:
                break

        return highlights

    @classmethod
    def _highlight_group(
        cls,
        text: str,
    ) -> str:
        """判断一条条目属于哪个要点分组。"""

        if cls._GRAPH_CALL_PATTERN.search(text):

            return "graph"

        if text.startswith("class "):

            return "class"

        if text.startswith(("def ", "@")):

            return "function"

        if text.startswith("import "):

            return "import"

        if text.startswith("路径 "):

            return "path"

        return "readme"

    # 图调用：`builder.add_node('x', ...)` 之类。
    _GRAPH_CALL_PATTERN = re.compile(
        r"\.(add_node|add_edge|add_conditional_edges"
        r"|set_entry_point|set_finish_point)\("
        r"|^StateGraph\("
    )

    # 从 add_node('name', ...) 里取节点名。
    _NODE_NAME_PATTERN = re.compile(
        r"add_node\(\s*['\"]([^'\"]+)['\"]"
    )

    # 从 add_edge('a', 'b') 里取两端。
    #
    # 显示成 `a → b` 比 `graph.add_edge` 有信息量得多。
    _EDGE_PATTERN = re.compile(
        r"add_(?:conditional_)?edge\(\s*"
        r"['\"]([^'\"]+)['\"]\s*,\s*"
        r"['\"]([^'\"]+)['\"]"
    )

    # 从 class Foo(Bar) / def foo(...) 里取名字。
    _DEFINITION_NAME_PATTERN = re.compile(
        r"^(?:class|def)\s+([A-Za-z_][A-Za-z0-9_]*)"
    )

    @classmethod
    def _highlight_line(
        cls,
        label: str,
        key: str,
        values: list,
    ) -> str:
        """渲染一条要点。"""

        names = []

        for value in values:

            names.append(
                cls._highlight_name(key, value)
            )

        shown = names[
            : cls.MAX_NAMES_PER_HIGHLIGHT
        ]

        rest = len(names) - len(shown)

        text = "、".join(
            f"`{name}`" for name in shown
        )

        if rest > 0:

            text += f" 等 {len(names)} 项"

        return f"{label}（{len(names)}）：{text}"

    @classmethod
    def _highlight_name(
        cls,
        key: str,
        value: str,
    ) -> str:
        """从原始条目里取出适合展示的名字。"""

        if key == "graph":

            node = cls._NODE_NAME_PATTERN.search(
                value
            )

            if node:
                return node.group(1)

            edge = cls._EDGE_PATTERN.search(value)

            if edge:
                return f"{edge.group(1)} → {edge.group(2)}"

            # StateGraph(...) -> StateGraph
            return value.split("(")[0]

        if key == "path":

            return value[len("路径 "):]

        if key == "import":

            return value[len("import "):]

        if key == "readme":

            # 自述条目可能是一整句，
            # 太长就截断，避免要点变成段落。
            return (
                value
                if len(value) <= 40
                else value[:40] + "…"
            )

        matched = cls._DEFINITION_NAME_PATTERN.match(
            value
        )

        if matched:
            return matched.group(1)

        return value

    @classmethod
    def _anchors(cls, entry: dict) -> list:
        """
        证据锚点：代码证据 + README 出处，合并限长。

        代码证据排在前面：
        它比 README 自述更接近项目实际做了什么。

        但要给 README 预留名额：
        declared_by 常常是 code+readme，
        而代码证据通常更多，
        不预留的话 README 锚点会被全部挤掉，
        读者就看不到「自述」那一半证据。
        """

        code = [
            item
            for item in (
                entry.get("code_evidence") or []
            )
            if isinstance(item, dict)
        ]

        readme = [
            item
            for item in (
                entry.get("evidence") or []
            )
            if isinstance(item, dict)
        ]

        # 最多给 README 留 2 个名额，
        # 且不超过它实际有的条数。
        reserved = min(
            cls.MAX_README_ANCHORS,
            len(readme),
        )

        code_budget = max(
            cls.MAX_ANCHORS - reserved,
            1,
        )

        anchors = [
            cls._code_evidence_line(item)
            for item in code[:code_budget]
        ]

        for item in readme:

            if len(anchors) >= cls.MAX_ANCHORS:
                break

            anchors.append(
                cls._code_evidence_line(item)
            )

        return anchors

    # 明细类型 -> 展示名。
    DETAIL_KIND_LABELS = {
        "graph": "图节点",
        "class": "类",
        "function": "函数",
    }

    @classmethod
    def _detail_markdown(
        cls,
        detail: dict,
    ) -> str:
        """
        渲染一条实现明细。

        形如：

            ### `duplicate_check` · `workflow_service.py:342`

            ```python
            def _node_duplicate_check(self, state: AgentState) -> AgentState
            ```

            - 调用：`find_similar_invoices`
            - 关键常量：`0.85`、`'duplicate_suspected'`
        """

        name = str(
            detail.get("name") or ""
        ).strip()

        signature = str(
            detail.get("signature") or ""
        ).strip()

        if not name and not signature:
            return ""

        file_path = detail.get("file_path")

        line = detail.get("line")

        location = file_path or "（未知文件）"

        if line:
            location = f"{location}:{line}"

        heading = "### "

        if name:

            heading += f"`{name}`"

            kind = cls.DETAIL_KIND_LABELS.get(
                str(detail.get("kind") or "")
            )

            if kind:
                heading += f" · {kind}"

            heading += f" · `{location}`"

        else:

            heading += f"`{location}`"

        blocks = [heading]

        if signature:

            blocks.append(
                "```python\n"
                f"{signature}\n"
                "```"
            )

        methods = detail.get("methods")

        if isinstance(methods, list) and methods:

            blocks.append(
                "- 方法："
                + "、".join(
                    f"`{item}`"
                    for item in methods
                )
            )

        calls = detail.get("calls")

        if isinstance(calls, list) and calls:

            blocks.append(
                "- 调用："
                + "、".join(
                    f"`{item}`"
                    for item in calls
                )
            )

        literals = detail.get("literals")

        if isinstance(literals, list) and literals:

            blocks.append(
                "- 关键常量："
                + "、".join(
                    f"`{item}`"
                    for item in literals
                )
            )

        return "\n\n".join(blocks)

    @staticmethod
    def _code_evidence_line(item: dict) -> str:
        """
        渲染一条代码证据。

        路径信号没有行号，
        直接照搬会变成
        「`src/app/graph/` — 路径 src/app/graph/」
        这种把同一句话说了两遍的样子，
        因此单独处理。
        """

        text = str(item.get("text") or "")

        line = (
            item.get("line")
            or item.get("line_start")
        )

        if line:

            return (
                f"`{ReportGenerationSkill._location(item)}`"
                f" — {text}"
            )

        # 无行号的一律是路径信号。
        return (
            f"目录/文件名命中架构关键词："
            f"`{ReportGenerationSkill._location(item)}`"
        )

    @staticmethod
    def _location(item: dict) -> str:
        """
        渲染证据位置。

        路径信号（例如「路径 src/app/agents/」）
        没有行号，此时只显示路径，
        不能渲染成 `src/app/agents/:None`。
        """

        file_path = (
            item.get("file")
            or item.get("file_path")
            or "（未知文件）"
        )

        line = (
            item.get("line")
            or item.get("line_start")
        )

        if line:

            return f"{file_path}:{line}"

        return str(file_path)

    @classmethod
    def _database_markdown(
        cls,
        technology_stack: dict,
    ) -> str:
        """10 数据库。"""

        if not technology_stack:
            return cls._missing_text(
                "真实数据不存在"
                "（未产出 technology_stack）。"
            )

        databases = technology_stack.get(
            "database"
        )

        if isinstance(
            databases,
            (list, tuple),
        ) and databases:

            body = cls._bullets(
                f"`{name}`" for name in databases
            )

        else:

            body = "未检测到数据库。"

        return (
            body
            + "\n\n"
            + "数据来源："
            "`workflow_state.data."
            "technology_stack.database`"
        )

    @classmethod
    def _evidence_markdown(
        cls,
        evidence,
    ) -> str:
        """12 Evidence：文件 + 行号 + 内容片段。"""

        if not isinstance(
            evidence,
            list,
        ) or not evidence:

            return cls._missing_text(
                "真实数据不存在"
                "（Evidence Agent 未产出证据）。"
            )

        blocks = []

        for item in evidence:

            if not isinstance(item, dict):
                continue

            file_path = (
                item.get("file_path")
                or "（未知文件）"
            )

            line_start = item.get(
                "line_start"
            )

            line_end = item.get(
                "line_end"
            )

            if line_start and line_end:

                location = (
                    f"{file_path}:"
                    f"{line_start}-{line_end}"
                )

            elif line_start:

                location = (
                    f"{file_path}:{line_start}"
                )

            else:

                location = file_path

            content = str(
                item.get("content") or ""
            ).strip()

            # 单条证据的 content 可能很长，
            # 这里只取首行做摘要，
            # 完整内容在 Evidence 表里。
            first_line = (
                content.splitlines()[0]
                if content
                else ""
            )

            block = f"**`{location}`**"

            if first_line:

                block += (
                    "\n\n> "
                    + first_line[:160]
                )

            blocks.append(block)

        if not blocks:
            return cls._missing_text(
                "真实数据不存在"
                "（Evidence Agent 未产出证据）。"
            )

        return "\n\n".join(blocks)

    @staticmethod
    def _missing(
        reason: str,
    ) -> dict:
        """统一的「真实数据不存在」表示。"""

        return {
            "available": False,
            "reason": reason,
        }

    # ------------------------------------------------------------------
    # 综合分析章节
    # ------------------------------------------------------------------

    @classmethod
    def _summary_section(
        cls,
        synthesis: dict,
        question=None,
        focus=None,
    ) -> str:
        """
        渲染 00 结论摘要。

        与其它章节不同，
        这一章是给人读的散文，
        不套 ```text JSON 代码块。

        综合分析不可用时仍然渲染该章，
        并写明原因 —— 缺席会被误读成
        「报告本来就没有结论层」。
        """

        if not synthesis.get("available"):

            reason = (
                synthesis.get("reason")
                or "综合分析未产出。"
            )

            return (
                "## 00 结论摘要\n\n"
                + cls._scope_note(question, focus)
                + "```text\n"
                "综合分析不可用。\n"
                f"原因：{reason}\n"
                "以下 01-11 章为未经归纳的原始分析数据。\n"
                "```"
            )

        summary = synthesis.get("summary")

        if not isinstance(summary, dict):
            summary = {}

        # 抬头：本次问了什么、重点在哪。
        #
        # 必须写清楚，否则用户无法判断
        # 报告为什么有的章详细、有的章只有一行。
        blocks = ["## 00 结论摘要"]

        scope = cls._scope_note(question, focus)

        if scope:
            blocks.append(scope.strip())

        blocks.append(
            "> 本章由 LLM 基于各 Agent 已采集的真实事实归纳，\n"
            "> 只做归纳、不做推测；\n"
            "> 事实不足处会明确标注「数据不足」。\n"
            "> 原始事实见下方 01-11 章。"
        )

        one_line = str(
            summary.get("one_line") or ""
        ).strip()

        if one_line:

            blocks.append(
                "### 一句话结论\n\n"
                f"{one_line}"
            )

        for key, title in cls.SUMMARY_FIELDS:

            items = summary.get(key)

            if not isinstance(items, list):
                continue

            bullets = [
                str(item).strip()
                for item in items
                if str(item).strip()
            ]

            if not bullets:
                continue

            blocks.append(
                f"### {title}\n\n"
                + "\n".join(
                    f"- {item}"
                    for item in bullets
                )
            )

        # summary 全空时（LLM 返回了合法 JSON
        # 但内容为空），明确说明而不是留一个空章。
        if len(blocks) == 1:

            blocks.append(
                "LLM 未返回可用的结论内容。"
            )

        return "\n\n".join(blocks)

    @classmethod
    def _section_with_judgment(
        cls,
        title: str,
        value,
        synthesis: dict,
        dimension: str,
    ) -> str:
        """
        渲染维度章节，并在末尾追加综合判断。

        综合判断不可用、或该维度没有判断时，
        只渲染原始数据章节，不追加空段落。
        """

        section = cls._section(
            title,
            value,
        )

        judgment = cls._dimension_judgment(
            synthesis,
            dimension,
        )

        if not judgment:
            return section

        return (
            f"{section}\n\n"
            f"**综合判断**：{judgment}"
        )

    @staticmethod
    def _dimension_judgment(
        synthesis: dict,
        dimension: str,
    ) -> str:
        """取出某个维度的综合判断，取不到返回空串。"""

        if not synthesis.get("available"):
            return ""

        dimensions = synthesis.get(
            "dimensions"
        )

        if not isinstance(
            dimensions,
            dict,
        ):
            return ""

        judgment = dimensions.get(
            dimension
        )

        if not isinstance(
            judgment,
            str,
        ):
            return ""

        return judgment.strip()

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
            # 来自真实源码的 AST 证据。
            #
            # 与上面的 README 证据分开，
            # 因为两者性质不同：
            # 一个是「项目说自己有什么」，
            # 一个是「项目代码里确实有什么」。
            "code_evidence": [
                {
                    "file": item.get("file_path"),
                    "line": item.get("line_start"),
                    "text": item.get("text"),
                }
                for item in (
                    entry.get("code_evidence") or []
                )
                if isinstance(item, dict)
            ],
            "declared_by": entry.get(
                "declared_by"
            ),
            # 实现明细：函数签名 / 调用链 / 关键字面量。
            #
            # 比 items 重，但正是它回答了
            # 「这个模块具体怎么做的」。
            "details": [
                item
                for item in (
                    entry.get("details") or []
                )
                if isinstance(item, dict)
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

        # 注意：_structure_dimension 成功时
        # 返回的是 {"items", "topics", "evidence"}，
        # 并不带 "available" 键；
        # 只有失败时才返回 _missing() 的
        # {"available": False, "reason": ...}。
        #
        # 这里曾经用 declared.get("available") 判断，
        # 成功路径永远取到 None，
        # 于是 RAG 章一直走「不可用」分支，
        # 还带着一个 None 的 reason。
        if not ReportGenerationSkill._is_missing(
            declared
        ):

            declared["vector_store_detected"] = (
                embedding
            )

            return declared

        return {
            "available": False,
            "reason": declared.get("reason")
            or (
                "真实数据不存在"
                "（被分析项目未声明 RAG 相关能力）。"
            ),
            "vector_store_detected": embedding,
        }

    @staticmethod
    def _section(
        title: str,
        value,
    ) -> str:
        """
        渲染一个章节。

        value 为字符串时按 markdown 原样输出；
        其它类型（理论上不应出现）退化成
        JSON 代码块，保证不会丢数据。
        """

        if value is None:
            value = "暂无数据"

        if isinstance(
            value,
            str,
        ):
            body = value.strip()
        else:
            body = (
                "```text\n"
                + json.dumps(
                    value,
                    ensure_ascii=False,
                    indent=2,
                    default=str,
                )
                + "\n```"
            )

        return (
            f"## {title}\n\n"
            f"{body}"
        )
