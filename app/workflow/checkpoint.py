"""
Workflow Checkpoint Manager。
"""

from copy import deepcopy
from typing import Any


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
        """保存 WorkflowState 快照。"""

        # 先递增原状态版本。
        state.checkpoint_version += 1

        snapshot = deepcopy(
            state
        )

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