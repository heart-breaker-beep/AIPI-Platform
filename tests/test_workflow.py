"""Workflow Engine 测试。"""

import pytest

from app.core.exceptions import (
    NonRetryableError,
    RetryableError,
)
from app.workflow.checkpoint import CheckpointManager
from app.workflow.context import WorkflowContext
from app.workflow.engine import WorkflowEngine
from app.workflow.node import BaseNode
from app.workflow.nodes.end_node import EndNode
from app.workflow.nodes.start_node import StartNode
from app.workflow.retry import RetryPolicy
from app.workflow.state import WorkflowState
from app.workflow.transition import Transition
from app.workflow.workflow import Workflow


class TouchNode(BaseNode):
    """记录执行顺序的测试节点。"""

    def __init__(self, name):

        self.name = name

    async def execute(
        self,
        state,
        context
    ):

        state.data.setdefault(
            "visited",
            []
        ).append(self.name)

        return state


class FailNode(BaseNode):
    """不可重试失败的测试节点。"""

    name = "fail"

    async def execute(
        self,
        state,
        context
    ):

        raise NonRetryableError("boom")


class FlakyNode(BaseNode):
    """第一次抛可重试异常，之后成功。"""

    name = "flaky"

    async def execute(
        self,
        state,
        context
    ):

        state.data["attempts"] = (
            state.data.get("attempts", 0) + 1
        )

        if state.data["attempts"] == 1:

            raise RetryableError(
                "temporary error"
            )

        return state


class PauseNode(BaseNode):
    """主动暂停的测试节点。"""

    name = "pause"

    async def execute(
        self,
        state,
        context
    ):

        state.status = "PAUSED"

        return state


def build_workflow(
    nodes,
    transitions
):
    """构建测试用 Workflow。"""

    workflow = Workflow()

    for node in nodes:

        workflow.add_node(node)

    for source, target in transitions:

        workflow.add_transition(
            Transition(source, target)
        )

    return workflow


def build_context():
    """构建测试用 Context。"""

    return WorkflowContext(
        agents={},
        tools={},
        skills={},
        config={},
    )


@pytest.mark.asyncio
async def test_workflow_runs_nodes_in_order():
    """测试 Workflow 按顺序执行 Node。"""

    workflow = build_workflow(
        [
            StartNode(),
            TouchNode("a"),
            TouchNode("b"),
            EndNode(),
        ],
        [
            ("start", "a"),
            ("a", "b"),
            ("b", "end"),
        ],
    )

    state = WorkflowState(run_id="wf-order")

    result = await WorkflowEngine().run(
        workflow,
        state,
        build_context(),
    )

    assert result.status == "COMPLETED"

    assert result.data["visited"] == ["a", "b"]

    assert result.current_node == "end"


@pytest.mark.asyncio
async def test_node_failure_is_captured():
    """测试 Node 失败被捕获。"""

    workflow = build_workflow(
        [
            StartNode(),
            FailNode(),
            EndNode(),
        ],
        [
            ("start", "fail"),
            ("fail", "end"),
        ],
    )

    state = WorkflowState(run_id="wf-fail")

    result = await WorkflowEngine().run(
        workflow,
        state,
        build_context(),
    )

    assert result.status == "FAILED"

    assert result.errors == ["boom"]

    assert result.current_node == "fail"


@pytest.mark.asyncio
async def test_retryable_error_is_retried():
    """测试可重试异常会按 RetryPolicy 重试。"""

    workflow = build_workflow(
        [
            StartNode(),
            FlakyNode(),
            EndNode(),
        ],
        [
            ("start", "flaky"),
            ("flaky", "end"),
        ],
    )

    state = WorkflowState(run_id="wf-retry")

    engine = WorkflowEngine(
        retry_policy=RetryPolicy(max_retry=3)
    )

    result = await engine.run(
        workflow,
        state,
        build_context(),
    )

    assert result.status == "COMPLETED"

    assert result.data["attempts"] == 2

    assert result.retry_count == 1


@pytest.mark.asyncio
async def test_non_retryable_error_is_not_retried():
    """测试不可重试异常不会重试。"""

    workflow = build_workflow(
        [
            StartNode(),
            FailNode(),
            EndNode(),
        ],
        [
            ("start", "fail"),
            ("fail", "end"),
        ],
    )

    state = WorkflowState(run_id="wf-no-retry")

    result = await WorkflowEngine().run(
        workflow,
        state,
        build_context(),
    )

    assert result.status == "FAILED"

    assert result.retry_count == 0


@pytest.mark.asyncio
async def test_checkpoint_save_and_load():
    """测试检查点保存和恢复。"""

    manager = CheckpointManager()

    state = WorkflowState(run_id="cp-1")

    state.data["key"] = "value"

    await manager.save(state)

    # 修改原状态，验证快照相互隔离
    state.data["key"] = "changed"

    restored = await manager.load("cp-1")

    assert restored.data["key"] == "value"

    assert await manager.load("not-exist") is None


@pytest.mark.asyncio
async def test_pause_and_resume():
    """测试暂停后可以从检查点恢复。"""

    workflow = build_workflow(
        [
            StartNode(),
            PauseNode(),
            TouchNode("after"),
            EndNode(),
        ],
        [
            ("start", "pause"),
            ("pause", "after"),
            ("after", "end"),
        ],
    )

    manager = CheckpointManager()

    engine = WorkflowEngine(
        checkpoint=manager
    )

    paused = await engine.run(
        workflow,
        WorkflowState(run_id="wf-pause"),
        build_context(),
    )

    assert paused.status == "PAUSED"

    assert paused.current_node == "pause"

    assert "after" not in paused.data.get(
        "visited",
        []
    )

    resumed = await engine.run(
        workflow,
        WorkflowState(run_id="wf-pause"),
        build_context(),
        resume_from="wf-pause",
    )

    assert resumed.status == "COMPLETED"

    assert resumed.data["visited"] == ["after"]
