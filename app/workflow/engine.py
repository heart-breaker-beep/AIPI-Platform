"""
Workflow 执行引擎。

Phase 12：
    - 顺序执行
    - Checkpoint
    - Pause
    - Resume
    - Retry
    - Human Gate
"""


from app.core.exceptions import (
    NonRetryableError,
    RetryableError,
)
from app.workflow.retry import RetryPolicy
from app.workflow.state import WorkflowStatus


class WorkflowEngine:
    """自研 Workflow 执行引擎。"""

    PAUSE_STATUSES = {
        WorkflowStatus.PAUSED,
        WorkflowStatus.WAITING_HUMAN,
        WorkflowStatus.WAITING_DESIGN,
    }

    def __init__(
        self,
        checkpoint=None,
        retry_policy=None,
    ) -> None:

        self.checkpoint = checkpoint

        self.retry_policy = (
            retry_policy
            or RetryPolicy()
        )

    async def run(
        self,
        workflow,
        state,
        context,
        resume_from=None,
    ):
        """
        执行 Workflow。

        resume_from：
            从 Checkpoint 恢复，并执行当前节点的下一个节点。

        state：
            如果 state 本身已经存在 current_node，
            则用于 Retry 当前节点。
        """

        if resume_from is not None:

            state = await self._restore(
                resume_from
            )

            if state is None:
                raise ValueError(
                    f"Checkpoint not found: {resume_from}"
                )

            current_node = (
                self._get_next_node(
                    workflow,
                    state,
                    state.current_node,
                )
            )

            state.resume()

        elif (
            state is not None
            and state.current_node
        ):

            # Retry：
            # 从失败节点重新执行。
            current_node = (
                state.current_node
            )

        else:

            current_node = "start"

        while current_node:

            node = workflow.nodes.get(
                current_node
            )

            if node is None:

                state.errors.append(
                    f"Node not found: {current_node}"
                )

                state.status = (
                    WorkflowStatus.FAILED
                )

                await self._save(state)

                return state

            state.current_node = (
                current_node
            )

            try:

                state = await self._execute_node(
                    node,
                    state,
                    context,
                )

            except Exception as error:

                state.errors.append(
                    str(error)
                )

                state.status = (
                    WorkflowStatus.FAILED
                )

                await self._save(state)

                return state

            if state.status in self.PAUSE_STATUSES:

                await self._save(state)

                return state

            await self._save(state)


            current_node = (
                self._get_next_node(
                    workflow,
                    state,
                    current_node,
                )
            )

        state.status = (
            WorkflowStatus.COMPLETED
        )

        await self._save(state)

        return state

    async def _execute_node(
        self,
        node,
        state,
        context,
    ):

        while True:

            try:

                return await node.execute(
                    state,
                    context,
                )

            except NonRetryableError:

                raise

            except RetryableError as error:

                if not self.retry_policy.should_retry(
                    error,
                    state.retry_count,
                ):
                    raise

                state.increase_retry()
                state.start_retry()

                await self._save(state)

                state.status = (
                    WorkflowStatus.ANALYZING
                )

    async def pause(
        self,
        state,
        reason: str = "manual_pause",
    ):

        state.pause(
            reason=reason
        )

        await self._save(state)

        return state

    async def approve(
        self,
        state,
    ):

        state.approve()

        await self._save(state)

        return state

    async def resume(
        self,
        workflow,
        context,
        run_id: str,
    ):

        return await self.run(
            workflow,
            None,
            context,
            resume_from=run_id,
        )

    async def retry(
        self,
        workflow,
        context,
        run_id: str,
    ):

        state = await self._restore(
            run_id
        )

        if state is None:
            raise ValueError(
                f"Checkpoint not found: {run_id}"
            )

        state.status = (
            WorkflowStatus.RETRYING
        )

        state.errors = []

        await self._save(state)

        return await self.run(
            workflow,
            state,
            context,
        )

    async def _save(
        self,
        state,
    ):

        if self.checkpoint is None:
            return

        await self.checkpoint.save(
            state
        )

    async def _restore(
        self,
        run_id: str,
    ):

        if self.checkpoint is None:
            raise ValueError(
                "Checkpoint manager is required"
            )

        return await self.checkpoint.load(
            run_id
        )

    def _get_next_node(
        self,
        workflow,
        state,
        current,
    ):

        for transition in workflow.transitions:

            if transition.source != current:
                continue

            if transition.condition:

                if not transition.condition(
                    state
                ):
                    continue

            return transition.target

        return None