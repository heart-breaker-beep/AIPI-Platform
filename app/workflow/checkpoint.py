"""
Workflow状态保存。
"""

from copy import deepcopy


class CheckpointManager:
    """
    保存和恢复Workflow状态。

    当前为内存实现，按 run_id 保存 WorkflowState 快照。
    持久化到 MySQL 属于后续阶段。
    """

    def __init__(self):

        # run_id -> WorkflowState 快照
        self._store = {}

    async def save(
        self,
        state
    ):

        # 深拷贝，避免后续修改影响已保存的快照
        self._store[
            state.run_id
        ] = deepcopy(state)

        return state.run_id

    async def load(
        self,
        run_id
    ):

        state = self._store.get(
            run_id
        )

        if state is None:

            return None

        return deepcopy(state)