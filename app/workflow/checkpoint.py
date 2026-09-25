"""
Workflow Checkpoint Manager。

Phase 10：
WorkflowState
    ↓
CheckpointManager
    ↓
Checkpoint Repository / MySQL

当前 Manager 负责状态序列化与恢复。
具体 MySQL 持久化由 Repository 完成。
"""

from copy import deepcopy
from typing import Any


class CheckpointManager:
    """
    Workflow Checkpoint 管理器。

    repository 可以是：
    - MySQL CheckpointRepository
    - 测试环境下的 MemoryCheckpointRepository
    """

    def __init__(
        self,
        repository=None,
    ) -> None:

        self.repository = repository

        # 测试 / 本地 fallback
        self._store: dict[str, Any] = {}

    async def save(
        self,
        state,
    ) -> str:
        """
        保存 WorkflowState。

        如果配置 Repository：
            保存到 MySQL

        否则：
            保存到内存
        """

        snapshot = deepcopy(state)

        snapshot.checkpoint_version += 1

        if self.repository is not None:

            await self.repository.save(
                snapshot
            )

        else:

            self._store[
                snapshot.run_id
            ] = snapshot

        return snapshot.run_id

    async def load(
        self,
        run_id: str,
    ):
        """
        根据 run_id 恢复最近一次 Checkpoint。
        """

        if self.repository is not None:

            state = await self.repository.get_latest(
                run_id
            )

            if state is None:
                return None

            return deepcopy(state)

        state = self._store.get(
            run_id
        )

        if state is None:
            return None

        return deepcopy(state)

    async def delete(
        self,
        run_id: str,
    ) -> None:
        """删除 Checkpoint。"""

        if self.repository is not None:

            await self.repository.delete(
                run_id
            )

        else:

            self._store.pop(
                run_id,
                None,
            )