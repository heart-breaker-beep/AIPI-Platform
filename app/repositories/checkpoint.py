"""
Workflow Checkpoint 数据访问层。
"""

from sqlalchemy import (
    delete,
    desc,
    func,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.checkpoint import Checkpoint
from app.workflow.state import WorkflowState


class CheckpointRepository:
    """负责 checkpoints 表的数据访问。"""

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:

        self.session = session

    async def save(
        self,
        state: WorkflowState,
    ) -> Checkpoint:
        """保存 WorkflowState 快照。"""

        checkpoint = Checkpoint(
            run_id=state.run_id,
            checkpoint_version=(
                state.checkpoint_version
            ),
            status=state.status,
            current_node=state.current_node,
            state_data=state.data,
            outputs=state.outputs,
            errors=state.errors,
            retry_count=state.retry_count,
            pause_reason=state.pause_reason,
            human_approved=state.human_approved,
        )

        self.session.add(
            checkpoint
        )

        await self.session.flush()

        return checkpoint

    async def get_latest(
        self,
        run_id: str,
    ) -> WorkflowState | None:
        """
        获取指定 run 的最新 Checkpoint。

        实现说明：

        不能用 ORDER BY checkpoint_version DESC LIMIT 1。

        state_data 是可能达到数百 KB 的 JSON
        （包含目录结构、关键源码、Evidence、报告），
        MySQL 在对这种大行排序时会报：

            OperationalError 1038
            Out of sort memory,
            consider increasing server sort buffer size

        因此改成两步：

            1. 只查最大版本号（只读整数列，不需要排序大行）
            2. 按 (run_id, version) 精确取行（等值查询，不排序）
        """

        version_result = await self.session.execute(
            select(
                func.max(
                    Checkpoint.checkpoint_version
                )
            ).where(
                Checkpoint.run_id == run_id
            )
        )

        latest_version = (
            version_result.scalar_one_or_none()
        )

        if latest_version is None:
            return None

        result = await self.session.execute(
            select(Checkpoint)
            .where(
                Checkpoint.run_id == run_id,
                Checkpoint.checkpoint_version
                == latest_version,
            )
            .limit(1)
        )

        checkpoint = (
            result.scalar_one_or_none()
        )

        if checkpoint is None:
            return None

        return WorkflowState(
            run_id=checkpoint.run_id,
            status=checkpoint.status,
            current_node=checkpoint.current_node,
            data=checkpoint.state_data or {},
            outputs=checkpoint.outputs or [],
            errors=checkpoint.errors or [],
            retry_count=checkpoint.retry_count,
            pause_reason=checkpoint.pause_reason,
            human_approved=checkpoint.human_approved,
            checkpoint_version=checkpoint.checkpoint_version,
        )

    async def delete(
        self,
        run_id: str,
    ) -> None:
        """删除指定 run 的全部 Checkpoint。"""

        await self.session.execute(
            delete(Checkpoint).where(
                Checkpoint.run_id == run_id
            )
        )

        await self.session.flush()