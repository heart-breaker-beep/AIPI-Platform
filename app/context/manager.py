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


class ContextManager:
    """
    把 Memory、Workflow State
    和语义检索结果组装成受控上下文。
    """

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

        # Filter + Rank + Deduplicate
        items = self.filter_and_rank(
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
    ) -> list[ContextItem]:
        """
        过滤空内容、去重，
        并按照关键词相关性排序。
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

            if len(unique) >= self.max_items:
                break

        return unique

    def assemble(
        self,
        *,
        query: str,
        items: list[ContextItem],
        workflow_state: Any | None = None,
        user_instruction: str | None = None,
    ) -> str:
        """把 Context 组装成 Agent 可使用的文本。"""

        sections = [
            "## Current Question",
            query.strip(),
        ]

        if user_instruction:

            sections.extend(
                [
                    "## User Instruction",
                    user_instruction.strip(),
                ]
            )

        if workflow_state is not None:

            sections.extend(
                [
                    "## Workflow State",
                    self._stringify(
                        workflow_state
                    ),
                ]
            )

        if items:

            sections.append(
                "## Retrieved Context"
            )

            for index, item in enumerate(
                items,
                start=1,
            ):

                sections.extend(
                    [
                        (
                            f"### Context {index} "
                            f"[{item.source}]"
                        ),
                        item.content,
                    ]
                )

        text = "\n\n".join(
            section
            for section in sections
            if section.strip()
        )

        if len(text) <= self.max_chars:
            return text

        return (
            text[
                : self.max_chars
            ].rstrip()
            + "\n...[context truncated]"
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

            for task in run_memory.get(
                "task_results",
                [],
            )[-8:]:

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
            )[-5:]:

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
            )[-10:]:

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
                    content=str(
                        memory_item
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