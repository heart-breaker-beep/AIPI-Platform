"""Analysis Run 数据访问层。"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.analysis_run import AnalysisRun


class AnalysisRunRepository:
    """负责 analysis_runs 表的数据访问。"""

    def __init__(self, session: AsyncSession) -> None:
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

    async def update_status(
        self,
        run: AnalysisRun,
        status: str,
    ) -> AnalysisRun:
        """更新分析任务状态。"""

        run.status = status

        await self.session.flush()

        return run
