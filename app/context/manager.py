"""Context Manager。

负责：

Retrieval
    ↓
Context Filtering
    ↓
Ranking
    ↓
Context Assembly
"""


import re

from dataclasses import dataclass
from typing import (
    Any,
    Awaitable,
    Callable,
)


@dataclass(frozen=True)
class ContextItem:
    """一个可供 Agent 使用的上下文片段。"""

    source: str

    content: str

    score: float = 0.0

    metadata: dict[str, Any] | None = None


def _render_history_entry(
    memory: dict[str, Any],
) -> str:
    """
    把一条历史 run 压成单行摘要。

    刻意只保留「问题 / 状态 / 任务类型与状态」，
    不带任务 output 原文 —— 原文既可能几十 KB，
    又最容易让模型把上一轮的结论误当成本轮的事实。
    """

    line = (
        f"- ({memory.get('created_at') or '时间未知'}) "
        f"问题：{memory.get('question') or '（未记录）'}"
        f" ｜ 状态：{memory.get('status') or '未知'}"
    )

    tasks = memory.get("tasks") or []

    if tasks:

        summary = ", ".join(
            f"{task.get('task_type') or '?'}:"
            f"{task.get('status') or '?'}"
            for task in tasks[:6]
        )

        line += f" ｜ 任务：{summary}"

    return line


class ContextManager:
    """
    把 Memory、Workflow State
    和语义检索结果组装成受控上下文。
    """

    # 跨 run 历史记忆在最终 Context 中的保底名额。
    #
    # 背景：project_memory 的权重只有 2.0，而 run 内的 evidence
    # 是 4.0 且一次最多 10 条。只按分数降序取 max_items 条时，
    # 12 个名额会被 question + research_plan + 10 条 evidence
    # 全部占满，跨 run 历史永远进不来 —— 而它恰恰是
    # ContextManager 唯一不可替代的那部分内容。
    #
    # 这里给结构性保底，而不是调高权重：关键词加分是无界叠加的，
    # 调权重会在长文本条目上被偶然命中淹没，不稳定。
    PROJECT_MEMORY_SOURCE = "project_memory"

    RESERVED_PROJECT_MEMORY = 3

    # 注入 LLM 提示用的历史记忆上限。
    #
    # 与 build() 的全量装配不同，这是「给模型看」的，
    # 必须小而稳：3 条历史 run、1500 字符封顶。
    HISTORY_MAX_RUNS = 3

    HISTORY_MAX_CHARS = 1500

    def __init__(
        self,
        memory_manager,
        retriever: (
            Callable[
                [str],
                Awaitable[
                    list[dict[str, Any]]
                ],
            ]
            | None
        ) = None,
        *,
        max_items: int = 12,
        max_chars: int = 12000,
    ) -> None:

        self.memory_manager = (
            memory_manager
        )

        self.retriever = retriever

        self.max_items = max_items

        self.max_chars = max_chars

    async def build(
        self,
        *,
        run_id: str,
        repository_id: int,
        query: str,
        workflow_state: Any | None = None,
        user_instruction: str | None = None,
    ) -> dict[str, Any]:
        """
        构建结构化 Context
        和最终文本 Context。
        """

        memory = (
            await self.memory_manager.retrieve(
                run_id=run_id,
                repository_id=repository_id,
                query=query,
            )
        )

        items = self._memory_items(
            memory
        )

        # 可选语义检索。
        #
        # 如果接入 Qdrant，
        # retriever 会返回相关源码片段。
        if (
            self.retriever is not None
            and query.strip()
        ):
            retrieved = await self.retriever(
                query
            )

            items.extend(
                self._retrieval_items(
                    retrieved
                )
            )

        # Filter + Rank + Deduplicate + 保底名额
        items = self.select(
            items,
            query,
        )

        # Context Assembly
        text = self.assemble(
            query=query,
            items=items,
            workflow_state=workflow_state,
            user_instruction=user_instruction,
        )

        return {
            "query": query,
            "items": [
                {
                    "source": item.source,
                    "content": item.content,
                    "score": item.score,
                    "metadata": (
                        item.metadata or {}
                    ),
                }
                for item in items
            ],
            "text": text,
        }

    def filter_and_rank(
        self,
        items: list[ContextItem],
        query: str,
        *,
        cap: bool = True,
    ) -> list[ContextItem]:
        """
        过滤空内容、去重，
        并按照关键词相关性排序。

        cap=False 时不做数量截断，返回全部排序结果 ——
        select() 需要先拿到完整排名，再自己分配名额。
        """

        keywords = re.findall(
            r"[A-Za-z0-9_]+|[\u4e00-\u9fff]{2,}",
            query.lower(),
        )

        scored: list[ContextItem] = []

        for item in items:

            content = item.content.strip()

            if not content:
                continue

            lowered = content.lower()

            keyword_score = sum(
                1
                for keyword in keywords
                if keyword in lowered
            )

            score = (
                item.score
                + keyword_score
            )

            scored.append(
                ContextItem(
                    source=item.source,
                    content=content,
                    score=score,
                    metadata=item.metadata,
                )
            )

        scored.sort(
            key=lambda item: item.score,
            reverse=True,
        )

        # 去重
        unique: list[ContextItem] = []

        seen: set[str] = set()

        for item in scored:

            key = item.content

            if key in seen:
                continue

            seen.add(key)

            unique.append(item)

            if cap and len(unique) >= self.max_items:
                break

        return unique

    def select(
        self,
        items: list[ContextItem],
        query: str,
    ) -> list[ContextItem]:
        """
        排序去重后按名额选取，并为跨 run 历史保留保底名额。

        与 filter_and_rank 的区别：后者是纯「按分数截断」，
        run 内条目分数普遍更高时会把 project_memory 全部挤掉。
        这里先给 project_memory 预留名额，再让其余条目
        竞争剩下的名额。
        """

        ranked = self.filter_and_rank(
            items,
            query,
            cap=False,
        )

        reserved = [
            item
            for item in ranked
            if item.source
            == self.PROJECT_MEMORY_SOURCE
        ][: self.RESERVED_PROJECT_MEMORY]

        others = [
            item
            for item in ranked
            if item.source
            != self.PROJECT_MEMORY_SOURCE
        ]

        remaining = max(
            self.max_items - len(reserved),
            0,
        )

        picked = reserved + others[:remaining]

        # 展示顺序仍按相关性分数降序 ——
        # 保底只决定「谁能进来」，不决定「谁排在前面」。
        picked.sort(
            key=lambda item: item.score,
            reverse=True,
        )

        return picked

    # 各小节的字符预算。
    #
    # 原实现只有一个全局 max_chars 尾截断，且把序列化后的
    # ## Workflow State 排在 ## Retrieved Context 之前 ——
    # state 一旦到几十 KB，真正有内容的小节会被整段切掉。
    # 改成每节独立预算，并让 Workflow State 退到最后。
    QUESTION_CHARS = 1500

    INSTRUCTION_CHARS = 1500

    WORKFLOW_STATE_CHARS = 1200

    MIN_RETRIEVED_CHARS = 2000

    def assemble(
        self,
        *,
        query: str,
        items: list[ContextItem],
        workflow_state: Any | None = None,
        user_instruction: str | None = None,
    ) -> str:
        """把 Context 组装成 Agent 可使用的文本。"""

        question = (query or "").strip()

        instruction = (
            user_instruction or ""
        ).strip()

        head_parts: list[str] = [
            "## Current Question",
            self._truncate(
                question,
                self.QUESTION_CHARS,
            ),
        ]

        # 与问题内容重复时不再单列。
        #
        # 调用方常把同一个 question 同时当 query 和
        # user_instruction 传进来，原实现会原样输出
        # 两个内容完全相同的小节。
        if instruction and instruction != question:

            head_parts.extend(
                [
                    "## User Instruction",
                    self._truncate(
                        instruction,
                        self.INSTRUCTION_CHARS,
                    ),
                ]
            )

        state_parts: list[str] = []

        if workflow_state is not None:

            state_parts = [
                "## Workflow State",
                self._truncate(
                    self._stringify(
                        workflow_state
                    ),
                    self.WORKFLOW_STATE_CHARS,
                ),
            ]

        # Retrieved Context 拿「总预算 − 固定小节开销」。
        # 固定小节已各自限长，不会再抢走它的份额。
        static_chars = sum(
            len(part)
            for part in head_parts + state_parts
        )

        budget = max(
            self.max_chars - static_chars,
            self.MIN_RETRIEVED_CHARS,
        )

        parts = list(head_parts)

        if items:

            parts.append("## Retrieved Context")

            rendered = self._render_items(
                items,
                budget,
            )

            if rendered:
                parts.append(rendered)

        # 状态放最后：真触发兜底截断时，牺牲的是状态而非历史。
        parts.extend(state_parts)

        text = "\n\n".join(
            part
            for part in parts
            if part.strip()
        )

        # 分段预算已保证不超限，这里只兜底极端边界。
        if len(text) <= self.max_chars:
            return text

        return (
            text[
                : self.max_chars
            ].rstrip()
            + "\n...[context truncated]"
        )

    @staticmethod
    def _truncate(
        value: str,
        limit: int,
    ) -> str:
        """按字符上限截断单段文本。"""

        if len(value) <= limit:
            return value

        return (
            value[:limit].rstrip()
            + "…[truncated]"
        )

    @staticmethod
    def _render_items(
        items: list[ContextItem],
        budget: int,
    ) -> str:
        """
        渲染 Retrieved Context 的条目。

        在条目边界截断，而不是字符中间 ——
        切一半的片段对模型是噪声。
        """

        blocks: list[str] = []

        used = 0

        for index, item in enumerate(
            items,
            start=1,
        ):

            block = (
                f"### Context {index} "
                f"[{item.source}]\n"
                f"{item.content.strip()}"
            )

            if used + len(block) > budget:

                # 第一条就超预算时至少给出截断内容，
                # 否则整个 Retrieved Context 会消失。
                if not blocks:

                    blocks.append(
                        block[:budget].rstrip()
                        + "\n…[truncated]"
                    )

                break

            blocks.append(block)

            used += len(block) + 2

        return "\n\n".join(blocks)

    async def build_history(
        self,
        *,
        run_id: str,
        repository_id: int,
        query: str | None = None,
        limit: int | None = None,
        max_chars: int | None = None,
    ) -> str:
        """
        组装「同一仓库历史分析」的紧凑文本块。

        这是 ContextManager 唯一不可替代的输出：
        本次 run 的数据各 Skill 已从 state 里拿到，
        只有跨 run 的历史是它们拿不到的。
        """

        memories = (
            await self.memory_manager
            .get_project_memory(
                repository_id,
                run_id=run_id,
                query=query,
                limit=(
                    limit
                    or self.HISTORY_MAX_RUNS
                ),
            )
        )

        if not memories:
            return ""

        lines = [
            "<history>",
            (
                "同一仓库此前的分析记录摘要（跨 run 历史）。"
                "可信度低于 <facts>，仅作线索。"
            ),
        ]

        for memory in memories:

            lines.append(
                _render_history_entry(memory)
            )

        lines.append("</history>")

        text = "\n".join(lines)

        char_limit = (
            max_chars
            or self.HISTORY_MAX_CHARS
        )

        if len(text) <= char_limit:
            return text

        return (
            text[:char_limit].rstrip()
            + "\n…[history truncated]"
        )

    @staticmethod
    def _memory_items(
        memory: dict[str, Any],
    ) -> list[ContextItem]:
        """把 Memory 转换成 ContextItem。"""

        items: list[ContextItem] = []

        run_memory = memory.get(
            "run_memory"
        )

        if run_memory:

            if run_memory.get(
                "question"
            ):

                items.append(
                    ContextItem(
                        source=(
                            "run_memory.question"
                        ),
                        content=str(
                            run_memory[
                                "question"
                            ]
                        ),
                        score=5.0,
                    )
                )

            if run_memory.get(
                "research_plan"
            ):

                items.append(
                    ContextItem(
                        source=(
                            "run_memory.research_plan"
                        ),
                        content=str(
                            run_memory[
                                "research_plan"
                            ]
                        ),
                        score=4.0,
                    )
                )

            if run_memory.get(
                "final_report"
            ):

                items.append(
                    ContextItem(
                        source=(
                            "run_memory.final_report"
                        ),
                        content=str(
                            run_memory[
                                "final_report"
                            ]
                        ),
                        score=2.5,
                    )
                )

            # run 内条目的窗口刻意收紧。
            #
            # 这些内容各 Skill 已从 state 拿到，
            # 放进 Context 只会挤占跨 run 历史的名额。
            for task in run_memory.get(
                "task_results",
                [],
            )[-5:]:

                items.append(
                    ContextItem(
                        source=(
                            "run_memory.task_result"
                        ),
                        content=str(task),
                        score=3.0,
                        metadata={
                            "task_id": task.get(
                                "id"
                            ),
                            "task_type": task.get(
                                "task_type"
                            ),
                        },
                    )
                )

            for output in run_memory.get(
                "agent_outputs",
                [],
            )[-3:]:

                items.append(
                    ContextItem(
                        source=(
                            "run_memory.agent_output"
                        ),
                        content=str(
                            output
                        ),
                        score=3.0,
                    )
                )

            for evidence in run_memory.get(
                "evidences",
                [],
            )[-6:]:

                items.append(
                    ContextItem(
                        source=(
                            "run_memory.evidence"
                        ),
                        content=str(
                            evidence
                        ),
                        score=4.0,
                        metadata={
                            "evidence_id": (
                                evidence.get(
                                    "id"
                                )
                            ),
                            "file_path": (
                                evidence.get(
                                    "file_path"
                                )
                            ),
                            "line_start": (
                                evidence.get(
                                    "line_start"
                                )
                            ),
                            "line_end": (
                                evidence.get(
                                    "line_end"
                                )
                            ),
                        },
                    )
                )

        for memory_item in memory.get(
            "project_memory",
            [],
        ):

            items.append(
                ContextItem(
                    source=(
                        "project_memory"
                    ),
                    # 压成单行摘要：原始 dict 里的
                    # tasks[].output 可能几十 KB。
                    content=(
                        _render_history_entry(
                            memory_item
                        )
                    ),
                    score=2.0,
                    metadata={
                        "run_id": (
                            memory_item.get(
                                "run_id"
                            )
                        ),
                    },
                )
            )

        return items

    @staticmethod
    def _retrieval_items(
        results: list[dict[str, Any]],
    ) -> list[ContextItem]:
        """
        把 Qdrant / 其他 Retriever
        的结果转换成 ContextItem。
        """

        items: list[ContextItem] = []

        for result in results:

            content = (
                result.get("content")
                or result.get("text")
                or result.get("payload")
                or ""
            )

            items.append(
                ContextItem(
                    source=(
                        "semantic_retrieval"
                    ),
                    content=str(
                        content
                    ),
                    score=float(
                        result.get(
                            "score",
                            1.0,
                        )
                    ),
                    metadata=result,
                )
            )

        return items

    @staticmethod
    def _stringify(
        value: Any,
    ) -> str:

        if isinstance(
            value,
            str,
        ):
            return value

        return str(value)