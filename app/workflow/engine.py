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
from app.core.logging import get_logger
from app.workflow.retry import RetryPolicy
from app.workflow.state import WorkflowStatus


logger = get_logger(__name__)


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

            if state.status == WorkflowStatus.FAILED:

                # FAILED 表示当前节点没有执行完成，
                # 因此必须重新执行该节点，
                # 不能像 Pause / Human Gate 那样跳到下一个节点。
                current_node = state.current_node

            else:

                # PAUSED / WAITING_DESIGN / WAITING_HUMAN：
                # 当前节点已经执行完成，
                # 从下一个节点继续。
                current_node = (
                    self._get_next_node(
                        workflow,
                        state,
                        state.current_node,
                    )
                )

            state.resume()

            # 重新执行意味着重新开始，
            # 上一轮失败留下的错误不再保留。
            state.errors = []

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

                # 记录完整 traceback。
                #
                # 部分异常（例如 httpx.ReadTimeout）
                # 的 str() 为空字符串，
                # 只记录 str(error) 会导致
                # errors == [""] 而无法排查。
                logger.exception(
                    "Workflow node failed: %s",
                    current_node,
                )

                state.errors.append(
                    str(error)
                    or type(error).__name__
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