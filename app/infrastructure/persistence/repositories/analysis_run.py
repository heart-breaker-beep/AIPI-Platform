"""
Analysis Run 数据访问层。
"""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.persistence.models.analysis_run import AnalysisRun
from app.infrastructure.persistence.repositories.base import BaseRepository


class AnalysisRunRepository(BaseRepository[AnalysisRun]):
    """负责 analysis_runs 表的数据访问。"""

    model = AnalysisRun

    async def create(
        self,
        *,
        run_id: str,
        repository_id: int,
        question: str | None = None,
    ) -> AnalysisRun:
        """创建一次 Analysis Run。"""

        return await super().create(
            id=run_id,
            repository_id=repository_id,
            question=question,
            status="pending",
        )

    async def get_by_id(
        self,
        run_id: str,
    ) -> Optional[AnalysisRun]:
        """根据 run_id 查询分析任务。"""
        return await super().get_by_id(run_id)

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

    # 用于把 error_message 显式清空的哨兵值。
    #
    # 不能用 None 表达「清空」：None 已经表示「这个字段不更新」，
    # 而重试成功后必须把上一轮的失败原因擦掉，
    # 否则前端会在一个 COMPLETED 的 run 上继续显示错误。
    CLEAR = object()

    async def update_runtime_state(
        self,
        run: AnalysisRun,
        *,
        status: str | None = None,
        current_node: str | None = None,
        retry_count: int | None = None,
        error_message=None,
    ) -> AnalysisRun:
        """
        更新 Workflow 运行状态。

        用于：
        - Pause
        - Resume
        - Retry
        - Checkpoint

        error_message 传 `AnalysisRunRepository.CLEAR` 表示清空。
        """

        if status is not None:
            run.status = status

        if current_node is not None:
            run.current_node = current_node

        if retry_count is not None:
            run.retry_count = retry_count

        if error_message is self.CLEAR:
            run.error_message = None

        elif error_message is not None:
            run.error_message = error_message

        await self.session.flush()

        return run