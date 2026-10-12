"""
Learning Path Skill（Phase 14.1）。

职责
====

输入：一个已经分析完的项目 + 用户目标
输出：

    学习顺序          先看什么、再看什么
    需要掌握的技术     读懂这个项目要会哪些东西
    核心源码          该精读哪几个文件
    推荐阅读路径      从入口到细节的走法
    改造建议          想动手改的话从哪下手

为什么它必须和分析结果绑定
==========================

学习路线很容易写成那种「先学 Python，
再学 FastAPI，再学 LangGraph」的通用清单 ——
放之四海而皆准，但对这个项目毫无用处。

因此本 Skill 的硬性约束与分析报告一致：

1. LLM 只能使用 <facts> 里提供的**这个项目的真实事实**
   （目录结构、各维度代码证据、关键文件、技术栈）
2. 事实不足时必须写「数据不足：<缺什么>」，
   不要给通用建议
3. prompt 里明确禁止「先学某语言/框架」这类
   与项目无关的通用路径

推荐的核心源码必须来自真实读到的文件清单，
不能是模型凭印象编的文件名。

产物形态
========

与分析报告、深挖报告一样，
是一份**独立的 markdown**，
不修改已有产物。
"""

from app.infrastructure.skills._common import (
    as_text_list,
    dumps_prompt,
)
from app.infrastructure.enrichment.context.injection import (
    build_history_block,
    resolve_repository_id,
)
from app.infrastructure.tools.project.code_structure_extractor import (
    CodeStructureExtractor,
)
from app.infrastructure.skills.llm_skill_base import (
    LLMSkillBase,
)


class LearningPathSkill(
    LLMSkillBase
):
    """生成项目的学习路线。"""

    # 文案沿用合并前的措辞（前端与测试都在读）。
    LLM_TOOL_MISSING_REASON = (
        "Tool not found: llm_chat，"
        "无法生成学习路线。"
    )

    LLM_JSON_INVALID_REASON = (
        "LLM 返回的内容不是合法 JSON，"
        "无法解析为学习路线。"
    )

    name = "learning_path"

    description = (
        "Generate a learning path for an "
        "analyzed repository."
    )

    # 送进 prompt 的 README 上限。
    MAX_README_CHARS = 3000

    # 最多列出多少个核心源码文件。
    MAX_CORE_FILES = 8

    # 单条建议最多多少字符，防止模型写成段落。
    MAX_ITEM_CHARS = 200

    # 各小节的展示名，顺序即渲染顺序。
    SECTIONS = (
        ("learning_order", "学习顺序"),
        ("prerequisites", "需要掌握的技术"),
        ("core_source", "核心源码"),
        ("reading_path", "推荐阅读路径"),
        ("improvements", "改造建议"),
    )

    async def execute(
        self,
        context,
        input_data: dict,
    ):
        # 先看工具在不在：原来这条判断在事实校验之前，
        # 顺序变了会让「两个条件同时不满足」时给出不同的原因。
        if context.tools.get("llm_chat") is None:

            return self._unavailable(
                self.LLM_TOOL_MISSING_REASON
            )

        facts = self._build_facts(input_data)

        if not facts.get("has_project_data"):

            return self._unavailable(
                "该 run 没有可用于生成学习路线的"
                "分析数据（缺少仓库信息与分析结果）。"
            )

        # 跨 run 历史记忆（同一仓库此前的分析）。
        history = await build_history_block(
            context,
            run_id=input_data.get("run_id"),
            repository_id=(
                resolve_repository_id(
                    context,
                    input_data,
                )
            ),
            query=(
                input_data.get("goal")
                or input_data.get("question")
            ),
        )

        prompt = self._build_prompt(
            facts,
            goal=(
                input_data.get("goal")
                or input_data.get("question")
            ),
            history=history,
        )

        parsed, reason = await self._ask_llm(
            context,
            system=self._system_prompt(),
            prompt=prompt,
        )

        if parsed is None:

            return self._unavailable(reason)

        sections = {
            key: as_text_list(
                parsed.get(key),
                max_items=6,
                max_chars=self.MAX_ITEM_CHARS,
            )
            for key, _ in self.SECTIONS
        }

        if not any(sections.values()):

            return self._unavailable(
                "LLM 返回的 JSON 里没有任何可用内容。"
            )

        content = self._render(facts, sections)

        report = await self._export(
            context,
            content=content,
            run_id=input_data.get("run_id"),
            repo=facts.get("repo"),
        )

        return {
            "available": True,
            "reason": None,
            "sections": sections,
            "report": report,
            "content": content,
        }

    @staticmethod
    def _unavailable(reason: str) -> dict:
        """统一的「学习路线不可用」表示。"""

        return {
            "available": False,
            "reason": reason,
            "sections": {},
            "report": {},
            "content": "",
        }

    # ------------------------------------------------------------------
    # 事实
    # ------------------------------------------------------------------

    def _build_facts(
        self,
        data: dict,
    ) -> dict:
        """
        构建送进 prompt 的事实。

        与分析报告共用同一批数据，
        不重新联网、不重新分析。
        """

        if not isinstance(data, dict):
            data = {}

        repository = data.get("repository")

        if not isinstance(repository, dict):
            repository = {}

        structure = data.get("project_structure")

        if not isinstance(structure, dict):
            structure = {}

        return {
            "has_project_data": bool(
                repository or structure.get("available")
            ),
            "repo": repository.get("name"),
            "full_name": repository.get(
                "full_name"
            ),
            "description": repository.get(
                "description"
            ),
            "language": repository.get("language"),
            "topics": repository.get("topics")
            or [],
            "technology_stack": (
                data.get("technology_stack") or {}
            ),
            "directory": self._directory(data),
            "readme": self._readme(data),
            "dimensions": self._dimensions(data),
            "core_files": self._core_files(data),
        }

    @staticmethod
    def _directory(data: dict) -> dict:
        """目录结构摘要。"""

        directory = data.get("directory_structure")

        if not isinstance(directory, dict):

            architecture = data.get(
                "architecture_analysis_agent"
            )

            if isinstance(architecture, dict):
                directory = architecture.get(
                    "directory_structure"
                )

        if not isinstance(directory, dict):
            return {"available": False}

        return {
            "available": True,
            "total_files": directory.get(
                "total_files"
            ),
            "top_level_dirs": (
                directory.get("top_level_dirs")
                or []
            ),
            "by_extension": (
                directory.get("by_extension") or {}
            ),
            "key_files": (
                directory.get("key_files") or []
            ),
        }

    def _readme(self, data: dict) -> dict:
        """README 摘要。"""

        readme = data.get("readme")

        if not isinstance(
            readme,
            str,
        ) or not readme.strip():

            return {
                "available": False,
                "reason": "未读取到 README。",
            }

        return {
            "available": True,
            "content": readme[
                : self.MAX_README_CHARS
            ],
        }

    @staticmethod
    def _dimensions(data: dict) -> dict:
        """
        六个维度的要点与代码证据。

        只给条目名与 文件:行号 ——
        学习路线要的是「去看哪里」，
        不需要把实现明细也塞进来。
        """

        structure = data.get("project_structure")

        if not isinstance(
            structure,
            dict,
        ) or not structure.get("available"):
            return {}

        dimensions = structure.get("dimensions")

        if not isinstance(dimensions, dict):
            return {}

        result = {}

        for name in CodeStructureExtractor.DIMENSIONS:

            entry = dimensions.get(name)

            if not isinstance(entry, dict):
                continue

            result[name] = {
                "declared": bool(
                    entry.get("declared")
                ),
                "declared_by": entry.get(
                    "declared_by"
                ),
                "items": (
                    entry.get("items") or []
                )[:8],
                "reason": entry.get("reason"),
                "code_evidence": [
                    {
                        "file": item.get("file_path"),
                        "line": item.get("line_start"),
                        "text": item.get("text"),
                    }
                    for item in (
                        entry.get("code_evidence")
                        or []
                    )[:4]
                    if isinstance(item, dict)
                ],
            }

        return result

    def _core_files(self, data: dict) -> list:
        """
        本次真实读到的源码文件。

        推荐核心源码必须从这里挑 ——
        模型不能凭空写出一个仓库里不存在的文件名。
        """

        modules = data.get("modules")

        if not isinstance(modules, list):
            return []

        files = []

        for module in modules:

            if not isinstance(module, dict):
                continue

            # 读取失败的模块不能进清单：
            # 它的 content 是空字符串，
            # 推荐它等于让用户去精读一个我们根本没读到的文件。
            # 与 report_synthesis_skill 的过滤保持一致。
            if module.get("error"):
                continue

            path = module.get("file_path")

            if not path:
                continue

            files.append(path)

            # 名额只被真正可用的文件占用 ——
            # 先切片再过滤的话，
            # 前面的失败条目会把后面的真实源码挤出去。
            if len(files) >= self.MAX_CORE_FILES:
                break

        return files

    # ------------------------------------------------------------------
    # prompt
    # ------------------------------------------------------------------

    @staticmethod
    def _system_prompt() -> str:
        """系统提示词。"""

        return (
            "你是一名资深工程师，"
            "正在为一位想读懂某个开源项目的开发者"
            "规划学习路线。\n"
            "\n"
            "你必须严格遵守以下规则：\n"
            "\n"
            "1. 只能使用用户消息中 <facts> 标签内"
            "提供的**这个项目的事实**。\n"
            "   禁止使用你自己的外部知识补充。\n"
            "2. **禁止给通用学习路线**。\n"
            "   「先学 Python，再学 FastAPI」这类建议"
            "对任何项目都成立，因此毫无价值。\n"
            "   每一条都必须指向这个项目的"
            "具体文件、具体类、具体模块。\n"
            "3. 推荐的核心源码必须从 facts.core_files "
            "里挑，\n"
            "   不允许写出清单之外的文件名 —— "
            "那会是编造的。\n"
            "4. 事实不足以支撑某个小节时，"
            "直接写「数据不足：<缺什么>」，"
            "不要用通用建议填充。\n"
            "5. 只输出 JSON，不要 markdown 包裹，"
            "不要解释文字。\n"
            "6. 用户消息中可能出现 <history> 标签，"
            "它是同一仓库**历史分析**的摘要，"
            "可信度低于 <facts>：\n"
            "   - 其中的任何结论，必须在本次 <facts> 中找到依据才能引用；\n"
            "   - 两者冲突时，一律以 <facts> 为准；\n"
            "   - 不得把 <history> 的内容表述为「本次分析的结果」；\n"
            "   - 不得仅因 <history> 提到某事物，"
            "就认为本项目当前具备该能力；\n"
            "   - <history> 与本次目标无关时，直接忽略。\n"
        )

    def _build_prompt(
        self,
        facts: dict,
        goal=None,
        history: str = "",
    ) -> str:
        """构建用户消息。"""

        parts = []

        if isinstance(
            goal,
            str,
        ) and goal.strip():

            parts.append(
                "学习者的目标：\n"
                f"{goal.strip()}\n"
            )

        # 历史放在 <facts> 之前：不可信内容在前、
        # 权威事实在后。为空时不占位，输出与改动前一致。
        if history:

            parts.append(
                history.strip() + "\n"
            )

        parts.append(
            "<facts>\n"
            + dumps_prompt(facts)
            + "\n</facts>\n"
        )

        parts.append(self._output_instruction())

        return "\n".join(parts)

    @staticmethod
    def _output_instruction() -> str:
        """输出格式说明。"""

        return (
            "请严格按下面的 JSON 结构输出：\n"
            "\n"
            "{\n"
            '  "learning_order": '
            '["第 1 步读什么、为什么", "第 2 步…"],\n'
            '  "prerequisites": '
            '["读懂这个项目需要掌握的技术，'
            '要说明它在项目里用在哪"],\n'
            '  "core_source": '
            '["`文件路径` — 这个文件为什么值得精读"],\n'
            '  "reading_path": '
            '["从一个具体入口出发的阅读顺序"],\n'
            '  "improvements": '
            '["想动手改造的话，建议从哪下手"]\n'
            "}\n"
            "\n"
            "每个数组最多 6 条，每条一句话。\n"
            "core_source 里的文件必须来自 facts.core_files。\n"
            "没有依据的小节写「数据不足：<缺什么>」。"
        )

    # ------------------------------------------------------------------
    # 渲染与导出
    # ------------------------------------------------------------------

    def _render(
        self,
        facts: dict,
        sections: dict,
    ) -> str:
        """渲染学习路线 markdown。"""

        title = (
            facts.get("full_name")
            or facts.get("repo")
            or "项目"
        )

        blocks = [
            (
                f"# {title} · 学习路线\n\n"
                "> 基于已有分析结果生成，"
                "不重新采集。\n"
                "> 所有建议都指向这个项目的"
                "真实文件与模块。"
            )
        ]

        for key, label in self.SECTIONS:

            values = sections.get(key)

            if not values:
                continue

            blocks.append(
                f"## {label}\n\n"
                + "\n".join(
                    f"- {item}" for item in values
                )
            )

        core = facts.get("core_files")

        if core:

            blocks.append(
                "## 本次可用于精读的文件\n\n"
                "以下文件是分析时真实读取过的，"
                "上面的建议从其中挑选：\n\n"
                + "\n".join(
                    f"- `{path}`" for path in core
                )
            )

        return "\n\n".join(blocks)

    async def _export(
        self,
        context,
        *,
        content: str,
        run_id,
        repo,
    ):
        """写出学习路线文件。"""

        exporter = context.tools.get(
            "report_export"
        )

        if exporter is None:

            return {
                "format": "markdown",
                "content": content,
            }

        if run_id:

            filename = f"{run_id}_learning_path.md"

        else:

            filename = (
                f"{repo or 'project'}_learning_path.md"
            )

        return await exporter.execute(
            title=(
                f"{repo or '项目'} · 学习路线"
            ),
            content=content,
            filename=filename,
        )
