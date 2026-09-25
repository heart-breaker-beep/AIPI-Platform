"""Project Memory。"""

import re
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.analysis_run import AnalysisRun
from app.models.analysis_task import AnalysisTask


class ProjectMemory:
    """
    读取同一 Repository 的历史分析结果。

    Project Memory 第一版只做历史 Run 检索，
    不引入独立长期记忆表。
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

    async def load(
        self,
        repository_id: int,
        *,
        exclude_run_id: str | None = None,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """加载指定 Repository 最近的历史分析。"""

        query = (
            select(AnalysisRun)
            .where(
                AnalysisRun.repository_id
                == repository_id
            )
            .order_by(
                AnalysisRun.created_at.desc()
            )
            .limit(
                max(limit, 1)
            )
        )

        result = await self.session.execute(
            query
        )

        runs = list(
            result.scalars().all()
        )

        if exclude_run_id is not None:
            runs = [
                run
                for run in runs
                if run.id != exclude_run_id
            ]

        if not runs:
            return []

        run_ids = [
            run.id
            for run in runs
        ]

        task_result = await self.session.execute(
            select(AnalysisTask)
            .where(
                AnalysisTask.run_id.in_(
                    run_ids
                )
            )
            .order_by(
                AnalysisTask.created_at
            )
        )

        tasks = list(
            task_result.scalars().all()
        )

        tasks_by_run: dict[
            str,
            list[dict[str, Any]]
        ] = {
            run_id: []
            for run_id in run_ids
        }

        for task in tasks:
            tasks_by_run.setdefault(
                task.run_id,
                [],
            ).append(
                {
                    "task_type": (
                        task.task_type
                    ),
                    "status": (
                        task.status
                    ),
                    "output": (
                        task.output
                    ),
                    "error": (
                        task.error
                    ),
                }
            )

        return [
            {
                "run_id": run.id,
                "question": run.question,
                "status": run.status,
                "current_node": (
                    run.current_node
                ),
                "created_at": (
                    run.created_at.isoformat()
                ),
                "tasks": (
                    tasks_by_run.get(
                        run.id,
                        [],
                    )
                ),
            }
            for run in runs
        ]

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

        scored: list[
            tuple[int, dict[str, Any]]
        ] = []

        for memory in memories:
            text = str(memory).lower()

            score = sum(
                1
                for keyword in keywords
                if keyword in text
            )

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

        return [
            memory
            for _, memory
            in scored[:limit]
        ]