"""Memory Manager。"""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.memory.project_memory import (
    ProjectMemory,
)
from app.memory.run_memory import (
    RunMemory,
)


class MemoryManager:
    """统一管理 Run Memory 与 Project Memory。"""

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.run_memory = RunMemory(
            session
        )

        self.project_memory = ProjectMemory(
            session
        )

    async def get_run_memory(
        self,
        run_id: str,
    ) -> dict[str, Any] | None:
        """获取当前 Run 的记忆。"""

        return await self.run_memory.load(
            run_id
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

    async def retrieve(
        self,
        *,
        run_id: str,
        repository_id: int,
        query: str | None = None,
        project_memory_limit: int = 5,
    ) -> dict[str, Any]:
        """
        一次性取得 Context Manager
        所需的 Memory。
        """

        run_memory = (
            await self.get_run_memory(
                run_id
            )
        )

        project_memory = (
            await self.get_project_memory(
                repository_id,
                run_id=run_id,
                query=query,
                limit=project_memory_limit,
            )
        )

        return {
            "run_memory": run_memory,
            "project_memory": project_memory,
        }