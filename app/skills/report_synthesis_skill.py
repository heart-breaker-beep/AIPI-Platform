"""
Report Synthesis Skill。

职责
====

在 Finalizer 生成报告之前，
把已被各 Agent 采集到的**真实事实**
交给 LLM，产出一层「判断」：

    - 00 结论摘要（一句话结论 / 核心设计 / 技术选型
                   / 亮点 / 风险与缺口 / 适用场景）
    - 各维度（agents / workflow / skills / tools
             / rag / memory）的综合判断

为什么需要这一层
================

在此之前，报告是 state.data 的 JSON 序列化：
有事实、没有结论。
本 Skill 负责从「事实」跨到「判断」。

硬性约束
========

1. LLM **只能**使用 prompt 中 <facts> 提供的事实，
   禁止补充外部知识、行业常识或猜测。
2. 事实不足时必须写「数据不足：<缺什么>」，
   不允许编造一个看起来合理的答案。
3. LLM 不可用（无 Key / 超时 / 返回非法 JSON）时，
   本 Skill 返回 available=False 并给出原因，
   **不抛异常**，报告仍然正常产出。

这三点与 ReportGenerationSkill 中
「不使用任何硬编码占位内容」的约束是同一条原则。
"""

import json

from app.skills.base import BaseSkill
from app.skills.json_output import (
    parse_json_object,
)


class ReportSynthesisSkill(
    BaseSkill
):
    """基于已采集事实生成综合判断。"""

    name = "report_synthesis"

    description = (
        "Synthesize judgments from "
        "collected analysis facts."
    )

    # 送进 prompt 的 README 最多多少字符。
    #
    # README 是当前最主要的事实来源，
    # 但个别仓库的 README 有数万字符，
    # 全量送入会撑爆上下文。
    MAX_README_CHARS = 6000

    # 送进 prompt 的单个源码片段最多多少字符。
    MAX_SOURCE_CHARS = 600

    # 最多送入多少个源码片段。
    MAX_SOURCE_FILES = 6

    # 最多送入多少条 Evidence。
    MAX_EVIDENCE = 12

    # 输出 JSON 中每个列表最多保留多少条。
    #
    # LLM 偶尔会写得很长，
    # 这里做上限保护，避免报告被一段话淹没。
    MAX_BULLETS = 6

    # 需要 LLM 给出判断的维度，
    # 与报告 04-09 章一一对应。
    DIMENSIONS = (
        "agents",
        "workflow",
        "skills",
        "tools",
        "rag",
        "memory",
    )

    # 维度名 -> 报告章节标题，用于 prompt 中给出上下文。
    DIMENSION_TITLES = {
        "agents": "Agent 架构",
        "workflow": "Workflow",
        "skills": "Skill",
        "tools": "Tool",
        "rag": "RAG",
        "memory": "Memory",
    }

    async def execute(
        self,
        context,
        input_data: dict,
    ):
        llm_tool = context.tools.get(
            "llm_chat"
        )

        if llm_tool is None:

            return self._unavailable(
                "Tool not found: llm_chat，"
                "无法生成综合分析。"
            )

        facts = self._build_facts(
            input_data
        )

        prompt = self._build_prompt(
            facts,
            question=input_data.get(
                "question"
            ),
        )

        result = await llm_tool.execute(
            messages=[
                {
                    "role": "system",
                    "content": (
                        self._system_prompt()
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ]
        )

        if not result.get("available"):

            return self._unavailable(
                result.get("reason")
                or "LLM 未返回内容。"
            )

        parsed = self._parse(
            result.get("content") or ""
        )

        if parsed is None:

            return self._unavailable(
                "LLM 返回的内容不是合法 JSON，"
                "无法解析为综合分析。"
            )

        summary = parsed.get("summary")

        if not isinstance(summary, dict):

            return self._unavailable(
                "LLM 返回的 JSON 缺少 summary 字段。"
            )

        return {
            "available": True,
            "reason": None,
            "summary": self._normalize_summary(
                summary
            ),
            "dimensions": (
                self._normalize_dimensions(
                    parsed.get("dimensions")
                )
            ),
        }

    @staticmethod
    def _unavailable(
        reason: str,
    ) -> dict:
        """统一的「综合分析不可用」表示。"""

        return {
            "available": False,
            "reason": reason,
            "summary": {},
            "dimensions": {},
        }

    # ------------------------------------------------------------------
    # prompt 构建
    # ------------------------------------------------------------------

    @staticmethod
    def _system_prompt() -> str:
        """
        系统提示词。

        这里是「只归纳不推测」约束的落点，
        修改时不要放宽这三条。
        """

        return (
            "你是一名资深软件架构分析师，"
            "正在为一份 GitHub 项目分析报告撰写结论部分。\n"
            "\n"
            "你必须严格遵守以下规则：\n"
            "\n"
            "1. 你只能使用用户消息中 <facts> 标签内提供的事实。\n"
            "   禁止使用你自己的外部知识、行业常识、"
            "对同类项目的印象来补充任何信息。\n"
            "2. 如果某个问题在 <facts> 中找不到依据，"
            "必须直接写「数据不足：<具体缺什么>」，"
            "绝对不要给出一个看起来合理的猜测。\n"
            "3. <facts> 中标记为 available=false 的部分，"
            "说明该项数据没有被采集到，"
            "对应的判断必须写成数据不足，"
            "不能说「未使用该技术」或「没有实现该能力」。\n"
            "   同样地，code_extraction.available=false "
            "或 parsed_files=0 时，"
            "说明源码没有被成功解析，"
            "此时不得对代码结构下任何结论。\n"
            "4. declared_by 表示结论的来源：\n"
            "   code    —— 代码里确实存在，可以说「实现了」；\n"
            "   readme  —— 只是 README 声称，"
            "必须写成「README 声称」而不是「实现了」；\n"
            "   code+readme  —— 两者都有，可以说「实现了」。\n"
            "5. 不要复述 JSON 原文，要给出结论性的判断，"
            "每条判断都要能对应到 <facts> 中的具体事实。\n"
            "6. 只输出 JSON，不要用 markdown 代码块包裹，"
            "不要在 JSON 前后添加任何解释文字。\n"
        )

    def _build_prompt(
        self,
        facts: dict,
        question=None,
    ) -> str:
        """构建用户消息。"""

        parts = []

        if isinstance(
            question,
            str,
        ) and question.strip():

            parts.append(
                "本次分析要回答的问题：\n"
                f"{question.strip()}\n"
            )

        parts.append(
            "<facts>\n"
            + json.dumps(
                facts,
                ensure_ascii=False,
                indent=2,
            )
            + "\n</facts>\n"
        )

        parts.append(
            self._output_instruction()
        )

        return "\n".join(parts)

    def _output_instruction(self) -> str:
        """输出格式说明。"""

        dimension_lines = "\n".join(
            f'    "{name}": "针对「'
            f'{self.DIMENSION_TITLES[name]}」'
            f'的综合判断，'
            f'数据不足时写「数据不足：<缺什么>」"'
            + ("," if index < len(
                self.DIMENSIONS
            ) - 1 else "")
            for index, name in enumerate(
                self.DIMENSIONS
            )
        )

        return (
            "请严格按下面的 JSON 结构输出，"
            "不要增删字段：\n"
            "\n"
            "{\n"
            '  "summary": {\n'
            '    "one_line": '
            '"一句话说清这个项目是什么、'
            '核心设计是什么",\n'
            '    "core_design": ["核心设计判断", "..."],\n'
            '    "technology_choices": '
            '["技术选型判断，'
            '说明这些技术组合意味着什么", "..."],\n'
            '    "highlights": ["这个项目做得好的地方", "..."],\n'
            '    "risks": ["风险、缺口、可疑之处", "..."],\n'
            '    "use_cases": ["适合用来做什么 / 参考什么", "..."]\n'
            "  },\n"
            '  "dimensions": {\n'
            f"{dimension_lines}\n"
            "  }\n"
            "}\n"
            "\n"
            "其中 summary 的每个列表字段最多 "
            f"{self.MAX_BULLETS} 条，"
            "每条一句话。\n"
            "facts 中没有依据的字段，"
            "写成「数据不足：<缺什么>」即可。"
        )

    # ------------------------------------------------------------------
    # 事实摘要
    # ------------------------------------------------------------------

    def _build_facts(
        self,
        data: dict,
    ) -> dict:
        """
        从 state.data 构建送入 LLM 的事实摘要。

        刻意只挑选与判断相关的字段：
        state.data 里还有 modules 全文、
        executed_tasks 等执行细节，
        全量送入既浪费上下文，
        又会把 AIPI 自身的执行状态
        混进对被分析项目的判断里。
        """

        if not isinstance(data, dict):
            data = {}

        return {
            "project_overview": (
                self._project_overview(data)
            ),
            "readme": self._readme(data),
            "technology_stack": (
                self._as_dict(
                    data.get("technology_stack")
                )
            ),
            "directory_structure": (
                self._as_dict(
                    data.get(
                        "directory_structure"
                    )
                )
            ),
            "declared_structure": (
                self._declared_structure(data)
            ),
            "code_extraction": (
                self._code_extraction(data)
            ),
            "source_files": (
                self._source_files(data)
            ),
            "evidence": self._evidence(data),
        }

    @staticmethod
    def _as_dict(value) -> dict:
        """只接受 dict，其它一律当空。"""

        if isinstance(value, dict):
            return value

        return {}

    @staticmethod
    def _project_overview(
        data: dict,
    ) -> dict:
        """项目概览：GitHub API 的真实元数据。"""

        repository = data.get(
            "repository"
        )

        if not isinstance(
            repository,
            dict,
        ):
            return {
                "available": False,
                "reason": "未获取到仓库信息。",
            }

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
            "available": True,
            "name": repository.get("name"),
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
            "size_kb": repository.get("size"),
            "created_at": repository.get(
                "created_at"
            ),
            "pushed_at": repository.get(
                "pushed_at"
            ),
        }

    def _readme(
        self,
        data: dict,
    ) -> dict:
        """README：被分析项目最主要的事实来源。"""

        readme = data.get("readme")

        if not isinstance(
            readme,
            str,
        ) or not readme.strip():

            return {
                "available": False,
                "reason": (
                    data.get("readme_error")
                    or "未读取到 README 内容。"
                ),
            }

        return {
            "available": True,
            "characters": len(readme),
            "truncated": (
                len(readme)
                > self.MAX_README_CHARS
            ),
            "content": readme[
                : self.MAX_README_CHARS
            ],
        }

    def _declared_structure(
        self,
        data: dict,
    ) -> dict:
        """
        被分析项目自述结构的各维度。

        直接把 declared / items / topics / evidence
        交给 LLM，
        并显式带上 available / reason，
        让模型知道哪些是真没有、哪些是没采到。
        """

        structure = data.get(
            "project_structure"
        )

        if (
            not isinstance(
                structure,
                dict,
            )
            or not structure.get("available")
        ):

            return {
                "available": False,
                "reason": (
                    "未产出被分析项目的自述结构"
                    "（project_structure）。"
                ),
            }

        dimensions = (
            structure.get("dimensions")
            or {}
        )

        result = {}

        for name in self.DIMENSIONS:

            entry = dimensions.get(name)

            if not isinstance(entry, dict):

                result[name] = {
                    "available": False,
                    "reason": (
                        "该维度没有被抽取。"
                    ),
                }

                continue

            result[name] = {
                "available": bool(
                    entry.get("declared")
                ),
                # 结论来自代码还是 README。
                #
                # 这个区别对判断很关键：
                # declared_by=readme 时，
                # 只能说「README 声称有」，
                # 不能说「代码里确实有」。
                "declared_by": entry.get(
                    "declared_by"
                ),
                "items": entry.get(
                    "items"
                )
                or [],
                "topics": entry.get(
                    "topics"
                )
                or [],
                "reason": entry.get(
                    "reason"
                ),
                "code_evidence": [
                    {
                        "file": item.get(
                            "file_path"
                        ),
                        "line": item.get(
                            "line_start"
                        ),
                        "text": item.get(
                            "text"
                        ),
                    }
                    for item in (
                        entry.get(
                            "code_evidence"
                        )
                        or []
                    )
                    if isinstance(
                        item,
                        dict,
                    )
                ],
                "readme_evidence": [
                    {
                        "line": item.get(
                            "line_start"
                        ),
                        "text": item.get(
                            "text"
                        ),
                    }
                    for item in (
                        entry.get("evidence")
                        or []
                    )
                    if isinstance(
                        item,
                        dict,
                    )
                ],
                # 实现明细：函数签名 / 调用链 / 关键常量。
                #
                # 这是判断「做到什么程度」的依据：
                # 只有符号名时只能说「有这个方法」，
                # 有了签名与调用链才能说
                # 「它查了哪些字段、阈值多少」。
                "details": [
                    {
                        "name": item.get("name"),
                        "signature": item.get(
                            "signature"
                        ),
                        "file": item.get(
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

    @staticmethod
    def _code_extraction(
        data: dict,
    ) -> dict:
        """
        代码抽取的执行情况。

        必须交给 LLM：
        「解析了 8 个文件、0 个失败」
        和「一个文件都没读到」
        会得出完全不同的可靠性判断。
        """

        structure = data.get(
            "project_structure"
        )

        if not isinstance(
            structure,
            dict,
        ):
            return {
                "available": False,
                "reason": "未产出结构信息。",
            }

        meta = structure.get(
            "code_extraction"
        )

        if not isinstance(meta, dict):
            return {
                "available": False,
                "reason": "未执行代码结构抽取。",
            }

        return meta

    def _source_files(
        self,
        data: dict,
    ) -> list:
        """
        真实读到的源码片段。

        这是当前唯一来自代码而非 README 的证据，
        虽然采样很浅，
        但对判断「README 说的和代码是否一致」
        已经够用。
        """

        modules = data.get("modules")

        if not isinstance(modules, list):
            return []

        files = []

        for module in modules:

            if not isinstance(
                module,
                dict,
            ):
                continue

            if module.get("error"):
                continue

            content = str(
                module.get("content") or ""
            )

            if not content.strip():
                continue

            files.append(
                {
                    "file_path": module.get(
                        "file_path"
                    ),
                    "content": content[
                        : self.MAX_SOURCE_CHARS
                    ],
                    "truncated": (
                        len(content)
                        > self.MAX_SOURCE_CHARS
                    ),
                }
            )

            if len(files) >= self.MAX_SOURCE_FILES:
                break

        return files

    def _evidence(
        self,
        data: dict,
    ) -> list:
        """Evidence 摘要：只给文件、行号与片段。"""

        evidence = data.get("evidence")

        if not isinstance(evidence, list):
            return []

        items = []

        for item in evidence[
            : self.MAX_EVIDENCE
        ]:

            if not isinstance(item, dict):
                continue

            content = item.get("content")

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
                    "content": str(
                        content or ""
                    )[:200],
                }
            )

        return items

    # ------------------------------------------------------------------
    # 输出解析
    # ------------------------------------------------------------------

    @staticmethod
    def _parse(
        content: str,
    ):
        """
        解析 LLM 返回的 JSON。

        兼容纯 JSON / ```json 包裹 /
        前后有解释文字 / 被截断四种情况。
        解析失败返回 None，由调用方降级。
        """

        return parse_json_object(content)

    def _normalize_summary(
        self,
        summary: dict,
    ) -> dict:
        """
        规整 summary。

        列表字段统一成字符串列表并限长；
        one_line 统一成字符串。
        """

        normalized = {
            "one_line": self._as_text(
                summary.get("one_line")
            )
        }

        for key in (
            "core_design",
            "technology_choices",
            "highlights",
            "risks",
            "use_cases",
        ):

            normalized[key] = (
                self._as_text_list(
                    summary.get(key)
                )
            )

        return normalized

    def _normalize_dimensions(
        self,
        dimensions,
    ) -> dict:
        """规整 dimensions：只保留已知维度且值为文本。"""

        if not isinstance(
            dimensions,
            dict,
        ):
            return {}

        return {
            name: self._as_text(
                dimensions.get(name)
            )
            for name in self.DIMENSIONS
            if dimensions.get(name)
        }

    @staticmethod
    def _as_text(value) -> str:
        """把任意值转成去空白的字符串。"""

        if value is None:
            return ""

        if isinstance(value, str):
            return value.strip()

        if isinstance(
            value,
            (list, tuple),
        ):
            return "；".join(
                str(item).strip()
                for item in value
                if str(item).strip()
            )

        return str(value).strip()

    def _as_text_list(
        self,
        value,
    ) -> list:
        """把任意值转成限长的字符串列表。"""

        if value is None:
            return []

        if isinstance(value, str):

            text = value.strip()

            return [text] if text else []

        if not isinstance(
            value,
            (list, tuple),
        ):
            return [str(value)]

        items = []

        for item in value:

            text = ReportSynthesisSkill._as_text(
                item
            )

            if not text:
                continue

            items.append(text)

            if len(items) >= self.MAX_BULLETS:
                break

        return items
