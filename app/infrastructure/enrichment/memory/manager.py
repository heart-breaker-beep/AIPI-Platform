"""Memory Manager。"""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.enrichment.memory.project_memory import (
    ProjectMemory,
)


class MemoryManager:
    """管理跨 Run 的 Project Memory。"""

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.project_memory = ProjectMemory(
            session
        )

    async def get_project_memory(
        self,
        repository_id: int,
        *,
        run_id: str | None = None,
        query: str | None = None,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """获取并按当前问题过滤项目历史记忆。"""

        memories = await self.project_memory.load(
            repository_id,
            exclude_run_id=run_id,
            limit=max(
                limit * 2,
                limit,
            ),
        )

        return (
            self.project_memory.filter_by_query(
                memories,
                query,
                limit=limit,
            )
        )
