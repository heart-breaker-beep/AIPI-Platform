"""
Module Deep Dive Skill。

职责
====

针对**某一个模块**（agents / workflow / skills /
tools / rag / memory）做深入分析，
产出一份独立的深挖报告。

为什么要有它
============

默认报告是「概览」：
每个模块只给要点与证据锚点，
既不浅到看不出结构，也不深到读不完。

但用户经常只想弄清楚**一个**模块 ——
「这个项目的 workflow 到底怎么流转的」。
这时候重跑整份报告是浪费，
只看概览又不够。

深挖就是补这一刀：只盯一个模块，
读更多文件、看更多符号、
把函数签名 / 调用链 / 关键常量 / 源码片段
全部展开。

与默认报告的差别
================

                       默认报告        深挖报告
    读取文件数          20             40（且只看该模块相关）
    每模块明细上限      6              20
    明细内容            不入报告        签名 + 调用链
                                        + 常量 + 源码片段
    LLM 结论            全项目一段      该模块七个小节

一条重要约束
============

深挖只**展开**默认报告已经采集到的结构，
不改变「只归纳不推测」的规则：
LLM 拿到的仍然是真实源码与真实事实，
源码片段直接来自 AST 的源码切片，
不是模型复述。
"""

import json
import re

from app.project_analysis.code_structure_extractor import (
    CodeStructureExtractor,
)
from app.skills.base import BaseSkill
from app.skills.json_output import (
    parse_json_object,
)


class ModuleDeepDiveSkill(
    BaseSkill
):
    """单模块深度分析能力。"""

    name = "module_deep_dive"

    description = (
        "Deep dive into one module of an "
        "analyzed repository."
    )

    # 可深挖的模块，与报告的 04-09 章一一对应。
    MODULES = CodeStructureExtractor.DIMENSIONS

    # 深挖时最多读取多少个文件。
    #
    # 默认报告是 20 个（六个模块分摊），
    # 深挖只看一个模块，所以给到 40。
    # 代价是每个文件一次 GitHub 请求。
    MAX_FILES = 40

    # 深挖时单个模块最多展开多少条明细。
    MAX_DETAILS = 20

    # 源码片段最多展示多少字符。
    MAX_SOURCE_CHARS = 1200

    # 送进 prompt 的 README 最多多少字符。
    MAX_README_CHARS = 4000

    MODULE_TITLES = {
        "agents": "Agent 架构",
        "workflow": "Workflow",
        "skills": "Skill",
        "tools": "Tool",
        "rag": "RAG",
        "memory": "Memory",
    }

    # LLM 输出的小节，顺序即渲染顺序。
    ANALYSIS_FIELDS = (
        ("responsibility", "职责"),
        ("key_implementations", "关键实现"),
        ("data_structures", "涉及的数据结构"),
        ("call_flow", "调用流程"),
        ("boundaries", "边界与限制"),
        ("risks", "风险与可疑之处"),
        ("open_questions", "需要人工确认"),
    )

    async def execute(
        self,
        context,
        input_data: dict,
    ):
        module = str(
            input_data.get("module") or ""
        ).strip().lower()

        if module not in self.MODULES:

            raise ValueError(
                f"Unsupported module: {module!r}. "
                f"Expected one of "
                f"{', '.join(self.MODULES)}."
            )

        owner = input_data.get("owner")

        repo = input_data.get("repo")

        if not owner or not repo:

            raise ValueError(
                "Module deep dive requires "
                "'owner' and 'repo'."
            )

        branch = input_data.get(
            "branch",
            "main",
        )

        tree = await self._load_tree(
            context,
            owner,
            repo,
            branch,
        )

        file_paths = self._select_files(
            tree,
            module,
        )

        sources, read_failures = (
            await self._read_sources(
                context,
                owner,
                repo,
                branch,
                file_paths,
            )
        )

        extra_paths = [
            item.get("path")
            for item in tree
            if isinstance(item, dict)
            and item.get("path")
        ]

        code_structure = (
            CodeStructureExtractor.extract(
                sources,
                extra_paths=extra_paths,
                max_details=self.MAX_DETAILS,
                # 深挖要展示源码片段；
                # 默认报告不展示，因此默认关掉
                # （每条 1.5KB，会把 state_data 撑过
                #   asyncmy 的 256KB 单字段上限）。
                include_source=True,
            )
        )

        entry = (
            code_structure.get(
                "dimensions"
            )
            or {}
        ).get(module) or {
            "items": [],
            "evidence": [],
            "details": [],
        }

        analysis = await self._analyze(
            context,
            module=module,
            owner=owner,
            repo=repo,
            entry=entry,
            readme=input_data.get("readme"),
            parsed_files=code_structure.get(
                "parsed_files",
                0,
            ),
            unparsed=code_structure.get(
                "unparsed"
            )
            or [],
        )

        content = self._render(
            module=module,
            owner=owner,
            repo=repo,
            entry=entry,
            analysis=analysis,
            files=sources,
            read_failures=read_failures,
            parsed_files=code_structure.get(
                "parsed_files",
                0,
            ),
            unparsed=code_structure.get(
                "unparsed"
            )
            or [],
        )

        report = await self._export(
            context,
            module=module,
            repo=repo,
            content=content,
            run_id=input_data.get("run_id"),
        )

        return {
            "module": module,
            "title": (
                f"{repo} · "
                f"{self.MODULE_TITLES.get(module, module)}"
                " 模块深挖"
            ),
            "files_read": [
                item["file_path"]
                for item in sources
            ],
            "details": len(
                entry.get("details") or []
            ),
            "analysis": analysis,
            "report": report,
            "content": content,
        }

    # ------------------------------------------------------------------
    # 取材
    # ------------------------------------------------------------------

    @staticmethod
    async def _load_tree(
        context,
        owner,
        repo,
        branch,
    ):
        """读取仓库文件树；拿不到时返回空列表。"""

        tool = context.tools.get(
            "github_repository"
        )

        if tool is None:
            return []

        get_tree = getattr(
            tool,
            "get_tree",
            None,
        )

        if not callable(get_tree):
            return []

        tree = await get_tree(
            owner=owner,
            name=repo,
            branch=branch,
        )

        if not isinstance(tree, list):
            return []

        return tree

    def _select_files(
        self,
        tree,
        module: str,
    ) -> list:
        """
        挑出与目标模块相关的文件。

        先用路径信号（`src/app/agents/` 之类）挑，
        不够再按浅层优先的顺序补充其它源码文件 ——
        有些模块不靠目录命名体现
        （例如 Skill 类散落在 services/ 下），
        只按路径筛会一个文件都读不到，
        那种情况下仍然要读一批文件
        让 AST 去认符号。
        """

        matched = []

        others = []

        for item in tree:

            if not isinstance(item, dict):
                continue

            path = item.get("path")

            if not path:
                continue

            if not str(path).lower().endswith(
                self.SOURCE_EXTENSIONS
            ):
                continue

            if str(path).lower().endswith(
                "__init__.py"
            ):
                continue

            if module in (
                CodeStructureExtractor
                .dimensions_for_path(path)
            ):

                matched.append(path)

            elif self._is_skippable_path(path):

                # 兜底阶段不看测试 / 迁移 / 文档。
                #
                # 命中目标模块的文件仍然优先，
                # 因此这里跳过不会漏掉该模块自身的代码。
                continue

            else:

                others.append(path)

        key = lambda path: (path.count("/"), path)

        matched.sort(key=key)

        others.sort(key=key)

        remaining = max(
            self.MAX_FILES - len(matched),
            0,
        )

        return matched + others[
            : min(
                self.MAX_FALLBACK_FILES,
                remaining,
            )
        ]

    # 与 ArchitectureAnalysisSkill 保持一致的源码扩展名。
    SOURCE_EXTENSIONS = (
        ".py",
        ".js",
        ".ts",
        ".tsx",
        ".jsx",
        ".mjs",
        ".go",
        ".java",
        ".rs",
        ".rb",
        ".php",
        ".cs",
        ".kt",
        ".swift",
        ".vue",
    )

    # 兜底补充文件时跳过的路径。
    #
    # 深挖的配额是 40，但命中目标模块的文件往往只有 1-2 个
    # （真实案例：workflow 模块只有 workflow_service.py，
    #   其余 39 个名额全被 tests/ 与 alembic/ 吃掉）。
    # 每个文件都是一次 GitHub 请求，
    # 把配额喂给测试与迁移既慢又没信息。
    SKIP_PATH_PATTERNS = (
        re.compile(r"(^|/)tests?/"),
        re.compile(r"(^|/)test_[^/]*$"),
        re.compile(r"_test\.[a-z]+$"),
        re.compile(r"(^|/)migrations?/"),
        # 整个 alembic/ 都是迁移脚手架，
        # 不只是 versions/ —— env.py、script.py.mako
        # 同样与应用架构无关。
        re.compile(r"(^|/)alembic/"),
        re.compile(r"(^|/)(demo_data|examples?|samples?)/"),
        re.compile(r"(^|/)docs?/"),
    )

    # 兜底补充文件的上限。
    #
    # MAX_FILES 是总配额，但命中目标模块的文件
    # 往往只有 1-2 个；剩下的名额如果全部用无关文件填满，
    # 就是几十次纯浪费的 GitHub 请求
    # （实测：workflow 模块读 40 个文件耗时 69 秒，
    #   其中 39 个对 workflow 维度毫无贡献）。
    #
    # 因此兜底只补到够用为止：
    # 既覆盖「模块符号散落在非同名目录」的情况，
    # 又不至于为了凑数去扫全仓库。
    MAX_FALLBACK_FILES = 15

    @classmethod
    def _is_skippable_path(
        cls,
        path: str,
    ) -> bool:
        """判断兜底补充时是否应跳过该路径。"""

        normalized = str(path).lower()

        return any(
            pattern.search(normalized)
            for pattern in cls.SKIP_PATH_PATTERNS
        )

    async def _read_sources(
        self,
        context,
        owner,
        repo,
        branch,
        file_paths,
    ):
        """
        逐个读取文件。

        单个文件失败不影响其它文件，
        失败原因如实带出来。
        """

        reader = context.tools.get("file_reader")

        if reader is None:
            raise RuntimeError(
                "Tool not found: file_reader"
            )

        sources = []

        failures = []

        for path in file_paths:

            try:

                content = await reader.execute(
                    owner=owner,
                    name=repo,
                    file_path=path,
                    branch=branch,
                )

            except Exception as error:

                failures.append(
                    {
                        "file_path": path,
                        "error": (
                            f"{type(error).__name__}: "
                            f"{error}"
                        ),
                    }
                )

                continue

            if not isinstance(content, str):
                continue

            if not content.strip():
                continue

            sources.append(
                {
                    "file_path": path,
                    "content": content,
                }
            )

        return sources, failures

    # ------------------------------------------------------------------
    # LLM 分析
    # ------------------------------------------------------------------

    async def _analyze(
        self,
        context,
        *,
        module,
        owner,
        repo,
        entry,
        readme,
        parsed_files,
        unparsed,
    ):
        """
        生成该模块的分析结论。

        LLM 不可用时返回 available=False，
        由渲染层降级为「只给实现明细」，
        不抛异常。
        """

        tool = context.tools.get("llm_chat")

        if tool is None:

            return {
                "available": False,
                "reason": "未注册 llm_chat 工具。",
            }

        facts = self._build_facts(
            module=module,
            owner=owner,
            repo=repo,
            entry=entry,
            readme=readme,
            parsed_files=parsed_files,
            unparsed=unparsed,
        )

        result = await tool.execute(
            messages=[
                {
                    "role": "system",
                    "content": self._system_prompt(
                        module
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "<facts>\n"
                        + json.dumps(
                            facts,
                            ensure_ascii=False,
                            indent=2,
                        )
                        + "\n</facts>\n\n"
                        + self._output_instruction()
                    ),
                },
            ]
        )

        if not result.get("available"):

            return {
                "available": False,
                "reason": result.get("reason")
                or "LLM 未返回内容。",
            }

        parsed = self._parse(
            result.get("content") or ""
        )

        if parsed is None:

            return {
                "available": False,
                "reason": (
                    "LLM 返回的内容不是合法 JSON。"
                ),
            }

        return {
            "available": True,
            "reason": None,
            "sections": {
                key: self._as_text_list(
                    parsed.get(key)
                )
                for key, _ in self.ANALYSIS_FIELDS
            },
        }

    def _build_facts(
        self,
        *,
        module,
        owner,
        repo,
        entry,
        readme,
        parsed_files,
        unparsed,
    ) -> dict:
        """构建送进 prompt 的事实。"""

        readme_text = ""

        if isinstance(readme, str):
            readme_text = readme[
                : self.MAX_README_CHARS
            ]

        return {
            "repository": f"{owner}/{repo}",
            "module": module,
            "module_title": self.MODULE_TITLES.get(
                module,
                module,
            ),
            "declared_by": entry.get(
                "declared_by"
            ),
            "items": entry.get("items") or [],
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
            "readme_evidence": [
                {
                    "line": item.get("line_start"),
                    "text": item.get("text"),
                }
                for item in (
                    entry.get("evidence") or []
                )
                if isinstance(item, dict)
            ],
            "implementations": [
                {
                    "name": item.get("name"),
                    "kind": item.get("kind"),
                    "signature": item.get(
                        "signature"
                    ),
                    "file": item.get("file_path"),
                    "line": item.get("line"),
                    "methods": item.get("methods")
                    or [],
                    "calls": item.get("calls") or [],
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
            "source_excerpts": [
                {
                    "name": item.get("name"),
                    "file": item.get("file_path"),
                    "line": item.get("line"),
                    "code": str(
                        item.get("source") or ""
                    )[: self.MAX_SOURCE_CHARS],
                }
                for item in (
                    entry.get("details") or []
                )
                if isinstance(item, dict)
                and item.get("source")
            ],
            "code_extraction": {
                "parsed_files": parsed_files,
                "unparsed": unparsed,
            },
            "readme": readme_text,
        }

    def _system_prompt(self, module: str) -> str:
        """系统提示词。"""

        title = self.MODULE_TITLES.get(
            module,
            module,
        )

        return (
            "你是一名资深软件架构分析师，"
            f"正在对某个 GitHub 项目的 "
            f"「{title}」模块做深入分析。\n"
            "\n"
            "你必须严格遵守以下规则：\n"
            "\n"
            "1. 只能使用用户消息中 <facts> 标签内提供的事实。\n"
            "   禁止使用外部知识、行业常识、"
            "对同类项目的印象来补充任何信息。\n"
            "2. 事实不足时必须写「数据不足：<缺什么>」，"
            "不要给出看起来合理的猜测。\n"
            "3. facts.declared_by 表示证据来源：\n"
            "   code   —— 代码里确实存在，可以说「实现了」；\n"
            "   readme —— 只是 README 声称，"
            "必须写成「README 声称」；\n"
            "   code+readme —— 两者都有。\n"
            "4. code_extraction.parsed_files 为 0 时，"
            "说明源码没被成功解析，"
            "不得对该模块的代码结构下任何结论。\n"
            "5. 只输出 JSON，不要用 markdown 代码块包裹，"
            "不要在 JSON 前后添加解释文字。\n"
        )

    def _output_instruction(self) -> str:
        """输出格式说明。"""

        lines = []

        for index, (key, label) in enumerate(
            self.ANALYSIS_FIELDS
        ):

            comma = (
                ","
                if index
                < len(self.ANALYSIS_FIELDS) - 1
                else ""
            )

            lines.append(
                f'  "{key}": '
                f'["{label}，数据不足时写'
                f'「数据不足：<缺什么>」"{comma}'
            )

        return (
            "请严格按下面的 JSON 结构输出，"
            "不要增删字段：\n"
            "{\n"
            + "\n".join(lines)
            + "\n}\n"
            "\n"
            "每个字段都是字符串数组，最多 6 条，"
            "每条一句话，要具体到这个模块的实现，"
            "不要写适用于任何项目的空话。"
        )

    # ------------------------------------------------------------------
    # 渲染
    # ------------------------------------------------------------------

    def _render(
        self,
        *,
        module,
        owner,
        repo,
        entry,
        analysis,
        files,
        read_failures,
        parsed_files,
        unparsed,
    ) -> str:
        """渲染深挖报告。"""

        title = self.MODULE_TITLES.get(
            module,
            module,
        )

        blocks = [
            (
                f"# {repo} · {title} 模块深挖报告\n\n"
                f"> 分析对象：`{owner}/{repo}`\n"
                f"> 模块：`{module}`\n"
                f"> 读取文件：{len(files)} 个"
                f"（默认报告为 20 个）\n"
                f"> 解析成功：{parsed_files} 个文件\n"
                f"> 实现明细："
                f"{len(entry.get('details') or [])} 项"
            )
        ]

        blocks.append(
            self._render_analysis(
                title,
                analysis,
            )
        )

        blocks.append(
            self._render_implementations(
                entry.get("details") or []
            )
        )

        blocks.append(
            self._render_evidence(entry)
        )

        blocks.append(
            self._render_extraction_health(
                files=files,
                read_failures=read_failures,
                unparsed=unparsed,
            )
        )

        return "\n\n".join(
            block
            for block in blocks
            if block
        )

    def _render_analysis(
        self,
        title: str,
        analysis: dict,
    ) -> str:
        """渲染 LLM 结论。"""

        if not analysis.get("available"):

            return (
                "## 分析结论\n\n"
                "```text\n"
                f"本模块的结论分析不可用。\n"
                f"原因：{analysis.get('reason')}\n"
                "以下实现明细为未经归纳的原始抽取结果。\n"
                "```"
            )

        sections = analysis.get(
            "sections"
        ) or {}

        blocks = ["## 分析结论"]

        for key, label in self.ANALYSIS_FIELDS:

            values = sections.get(key)

            if not values:
                continue

            blocks.append(
                f"### {label}\n\n"
                + "\n".join(
                    f"- {item}" for item in values
                )
            )

        if len(blocks) == 1:

            blocks.append("LLM 未返回可用的结论内容。")

        return "\n\n".join(blocks)

    def _render_implementations(
        self,
        details: list,
    ) -> str:
        """渲染实现明细（签名 + 调用链 + 常量 + 源码）。"""

        if not details:

            return (
                "## 实现明细\n\n"
                "未抽取到实现明细"
                "（该模块没有匹配到可解析的函数 / 类）。"
            )

        blocks = ["## 实现明细"]

        for detail in details:

            blocks.append(
                self._render_detail(detail)
            )

        return "\n\n".join(blocks)

    def _render_detail(
        self,
        detail: dict,
    ) -> str:
        """渲染单条实现明细。"""

        name = str(
            detail.get("name") or ""
        ).strip()

        file_path = detail.get("file_path")

        line = detail.get("line")

        location = file_path or "（未知文件）"

        if line:
            location = f"{location}:{line}"

        heading = (
            f"### `{name}` · `{location}`"
            if name
            else f"### `{location}`"
        )

        blocks = [heading]

        signature = str(
            detail.get("signature") or ""
        ).strip()

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
                    f"`{item}`" for item in methods
                )
            )

        calls = detail.get("calls")

        if isinstance(calls, list) and calls:

            blocks.append(
                "- 调用："
                + "、".join(
                    f"`{item}`" for item in calls
                )
            )

        literals = detail.get("literals")

        if isinstance(literals, list) and literals:

            blocks.append(
                "- 关键常量："
                + "、".join(
                    f"`{item}`" for item in literals
                )
            )

        source = str(
            detail.get("source") or ""
        ).strip()

        if source:

            blocks.append(
                "**源码片段**\n\n"
                "```python\n"
                f"{source[: self.MAX_SOURCE_CHARS]}\n"
                "```"
            )

        return "\n\n".join(blocks)

    @staticmethod
    def _render_evidence(entry: dict) -> str:
        """渲染该模块的条目与证据锚点。"""

        blocks = []

        items = entry.get("items")

        if isinstance(items, list) and items:

            blocks.append(
                "## 结构化条目\n\n"
                + "\n".join(
                    f"- {item}" for item in items
                )
            )

        anchors = []

        for key in (
            "code_evidence",
            "evidence",
        ):

            for item in entry.get(key) or []:

                if not isinstance(item, dict):
                    continue

                file_path = (
                    item.get("file_path")
                    or item.get("file")
                    or "（未知文件）"
                )

                line = item.get("line_start")

                location = (
                    f"{file_path}:{line}"
                    if line
                    else file_path
                )

                anchors.append(
                    f"- `{location}` — {item.get('text')}"
                )

        if anchors:

            blocks.append(
                "## 证据锚点\n\n"
                + "\n".join(anchors)
            )

        return "\n\n".join(blocks)

    @staticmethod
    def _render_extraction_health(
        *,
        files,
        read_failures,
        unparsed,
    ) -> str:
        """
        如实交代这次的采集情况。

        深挖的价值在于「看得比默认报告多」，
        因此多读了哪些文件、
        哪些没读到、哪些没解析成功，
        必须写清楚，否则读者无法判断结论的覆盖面。
        """

        lines = [
            (
                "- 成功读取并解析："
                f"{len(files)} 个文件"
            )
        ]

        if read_failures:

            lines.append(
                f"- 读取失败：{len(read_failures)} 个"
            )

            for item in read_failures[:10]:

                lines.append(
                    f"  - `{item['file_path']}`"
                    f" — {item['error']}"
                )

        if unparsed:

            lines.append(
                f"- 解析失败：{len(unparsed)} 个"
            )

            for item in unparsed[:10]:

                lines.append(
                    f"  - `{item['file_path']}`"
                    f" — {item['error']}"
                )

        if files:

            lines.append("- 本次读取的文件：")

            for item in files:

                lines.append(
                    f"  - `{item['file_path']}`"
                )

        return (
            "## 本次采集范围\n\n"
            + "\n".join(lines)
        )

    # ------------------------------------------------------------------
    # 导出与工具方法
    # ------------------------------------------------------------------

    async def _export(
        self,
        context,
        *,
        module,
        repo,
        content,
        run_id,
    ):
        """写出深挖报告文件。"""

        exporter = context.tools.get(
            "report_export"
        )

        filename = (
            f"{run_id}_{module}_deep_dive.md"
            if run_id
            else f"{repo}_{module}_deep_dive.md"
        )

        if exporter is None:

            return {
                "format": "markdown",
                "content": content,
            }

        return await exporter.execute(
            title=(
                f"{repo} · {module} 模块深挖报告"
            ),
            content=content,
            filename=filename,
        )

    @staticmethod
    def _parse(
        content: str,
    ):
        """
        解析 LLM 返回的 JSON。

        与报告综合分析共用同一套容错逻辑
        （代码块包裹 / 前后噪声 / 被截断）。
        """

        return parse_json_object(content)

    @staticmethod
    def _as_text_list(value) -> list:
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

            text = str(item).strip()

            if not text:
                continue

            items.append(text)

            if len(items) >= 6:
                break

        return items
