"""Project Memory。"""

import re
from typing import Any


class ProjectMemory:
    """
    读取同一 Repository 的历史分析结果。

    Project Memory 第一版只做历史 Run 检索，
    不引入独立长期记忆表。
    """

    def __init__(
        self,
        repository,
    ) -> None:
        self.repository = repository

    async def load(
        self,
        repository_id: int,
        *,
        exclude_run_id: str | None = None,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """通过注入的历史存储读取数据。"""
        return await self.repository.load(
            repository_id, exclude_run_id=exclude_run_id, limit=limit
        )

    @staticmethod
    def filter_by_query(
        memories: list[dict[str, Any]],
        query: str | None,
        *,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """
        按关键词相关性过滤历史记忆。
        """

        if not query:
            return memories[:limit]

        keywords = set(
            re.findall(
                r"[A-Za-z0-9_]+|[\u4e00-\u9fff]{2,}",
                query.lower(),
            )
        )

        if not keywords:
            return memories[:limit]

        scored: list[tuple[int, dict[str, Any]]] = []

        for memory in memories:
            text = str(memory).lower()

            score = sum(1 for keyword in keywords if keyword in text)

            if score > 0:
                scored.append(
                    (
                        score,
                        memory,
                    )
                )

        scored.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [memory for _, memory in scored[:limit]]
