"""
Analysis Run 数据访问层。
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.analysis_run import AnalysisRun


class AnalysisRunRepository:
    """负责 analysis_runs 表的数据访问。"""

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:

        self.session = session

    async def create(
        self,
        *,
        run_id: str,
        repository_id: int,
        question: str | None = None,
    ) -> AnalysisRun:
        """创建一次 Analysis Run。"""

        run = AnalysisRun(
            id=run_id,
            repository_id=repository_id,
            question=question,
            status="pending",
        )

        self.session.add(run)

        await self.session.flush()

        return run

    async def get_by_id(
        self,
        run_id: str,
    ) -> AnalysisRun | None:
        """根据 run_id 查询分析任务。"""

        result = await self.session.execute(
            select(AnalysisRun).where(
                AnalysisRun.id == run_id
            )
        )

        return result.scalar_one_or_none()

    async def list_recent(
        self,
        limit: int = 20,
    ) -> list[AnalysisRun]:
        """
        按创建时间倒序列出最近的 Analysis Run。

        给前端的历史列表用。

        只读 analysis_runs 这张小表：
        state_data 在 checkpoints 里，
        这里不碰，避免大字段排序触发
        1038 Out of sort memory。
        """

        result = await self.session.execute(
            select(AnalysisRun)
            .order_by(
                AnalysisRun.created_at.desc()
            )
            .limit(limit)
        )

        return list(result.scalars().all())

    async def update_status(
        self,
        run: AnalysisRun,
        status: str,
    ) -> AnalysisRun:
        """更新分析任务状态。"""

        run.status = status

        await self.session.flush()

        return run

    async def update_runtime_state(
        self,
        run: AnalysisRun,
        *,
        status: str | None = None,
        current_node: str | None = None,
        retry_count: int | None = None,
    ) -> AnalysisRun:
        """
        更新 Workflow 运行状态。

        用于：
        - Pause
        - Resume
        - Retry
        - Checkpoint
        """

        if status is not None:
            run.status = status

        if current_node is not None:
            run.current_node = current_node

        if retry_count is not None:
            run.retry_count = retry_count

        await self.session.flush()

        return run