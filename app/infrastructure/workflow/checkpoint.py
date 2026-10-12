"""
Workflow Checkpoint Manager。

负责：
- 管理 Checkpoint 的保存和加载
- 在保存前调用 StateManager 瘦身 state.data
- 深拷贝 state 避免修改运行时状态
"""

from copy import deepcopy
from typing import Any

from app.infrastructure.workflow.state_manager import StateManager


class CheckpointManager:
    """Workflow Checkpoint 管理器。"""

    def __init__(
        self,
        repository=None,
    ) -> None:
        self.repository = repository
        self._store: dict[str, Any] = {}

    async def save(
        self,
        state,
    ) -> str:
        """
        保存 WorkflowState 快照。

        流程：
        1. 递增版本号
        2. 深拷贝 state（避免修改运行时状态）
        3. 瘦身 state.data（通过 StateManager）
        4. 保存到 Repository
        """
        # 先递增原状态版本
        state.checkpoint_version += 1

        # 深拷贝，避免瘦身影响运行时状态
        snapshot = deepcopy(state)

        # 瘦身 state.data
        if snapshot.data:
            trimmed_data, trims = StateManager.prepare_for_persistence(snapshot.data)
            snapshot.data = StateManager.add_trim_metadata(trimmed_data, trims)

        if self.repository is not None:
            await self.repository.save(snapshot)
        else:
            self._store[snapshot.run_id] = snapshot

        return snapshot.run_id

    async def load(
        self,
        run_id: str,
    ):
        """读取最近一次 Checkpoint。"""

        if self.repository is not None:

            state = (
                await self.repository.get_latest(
                    run_id
                )
            )

            if state is None:
                return None

            return deepcopy(
                state
            )

        state = self._store.get(
            run_id
        )

        if state is None:
            return None

        return deepcopy(
            state
        )

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