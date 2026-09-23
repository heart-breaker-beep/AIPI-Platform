"""
Workflow执行引擎。
"""

from app.core.exceptions import (
    NonRetryableError,
    RetryableError,
)
from app.workflow.retry import RetryPolicy


class WorkflowEngine:

    # 暂停状态标识
    PAUSED_STATUS = "PAUSED"

    def __init__(
        self,
        checkpoint=None,
        retry_policy=None,
    ):

        # 检查点管理器，可选
        self.checkpoint = checkpoint

        # 节点重试策略
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
        执行Workflow。
        """

        if resume_from is not None:

            state = await self._restore(
                resume_from
            )

            # 当前节点已执行过，从它的下一节点继续
            current_node = self._get_next_node(
                workflow,
                state,
                state.current_node
            )

        else:

            current_node = "start"

        while current_node:


            # 获取节点
            node = workflow.nodes[
                current_node
            ]


            # 更新状态
            state.current_node = (
                current_node
            )

            try:

                # 执行节点
                state = await self._execute_node(
                    node,
                    state,
                    context
                )
            except Exception as e:

                state.errors.append(
                    str(e)
                )

                state.status = (
                    "FAILED"
                )

                return state

            # 暂停：保存检查点后退出，等待 Resume
            if state.status == self.PAUSED_STATUS:

                await self._save(state)

                return state

            # 每执行完一个节点保存一次检查点
            await self._save(state)

            # 查找下一节点
            current_node = (
                self._get_next_node(
                    workflow,
                    state,
                    current_node
                )
            )



        state.status = (
            "COMPLETED"
        )


        return state



    async def _execute_node(
        self,
        node,
        state,
        context
    ):
        """
        执行节点。

        可重试异常按 RetryPolicy 重试，
        不可重试异常直接抛出。
        """

        while True:

            try:

                return await node.execute(
                    state,
                    context
                )

            except NonRetryableError:

                raise

            except RetryableError as e:

                if not self.retry_policy.can_retry(
                    state.retry_count
                ):

                    raise e

                state.retry_count += 1



    async def _save(
        self,
        state
    ):
        """
        保存检查点，未配置时跳过。
        """

        if self.checkpoint is None:

            return

        await self.checkpoint.save(
            state
        )



    async def _restore(
        self,
        run_id
    ):
        """
        从检查点恢复状态。
        """

        if self.checkpoint is None:

            raise ValueError(
                "resume_from requires a checkpoint manager"
            )

        state = await self.checkpoint.load(
            run_id
        )

        if state is None:

            raise ValueError(
                f"Checkpoint not found: {run_id}"
            )

        # 恢复后重新进入运行态
        state.status = "RUNNING"

        return state



    def _get_next_node(
        self,
        workflow,
        state,
        current
    ):
        """
        获取下一执行节点。
        """
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
