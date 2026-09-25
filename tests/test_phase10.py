"""Phase 10：HITL / Checkpoint / Pause / Resume / Retry 测试。"""

import pytest

from app.core.exceptions import (
    NonRetryableError,
    RetryableError,
)
from app.workflow.checkpoint import (
    CheckpointManager,
)
from app.workflow.context import WorkflowContext
from app.workflow.engine import (
    WorkflowEngine,
)
from app.workflow.node import BaseNode
from app.workflow.nodes.end_node import EndNode
from app.workflow.nodes.human_node import HumanNode
from app.workflow.nodes.start_node import StartNode
from app.workflow.retry import RetryPolicy
from app.workflow.state import (
    WorkflowState,
    WorkflowStatus,
)
from app.workflow.transition import Transition
from app.workflow.workflow import Workflow


def build_context():
    """创建测试 Context。"""

    return WorkflowContext(
        agents={},
        tools={},
        skills={},
        config={},
    )


def build_workflow(
    nodes,
    transitions,
):
    """创建测试 Workflow。"""

    workflow = Workflow()

    for node in nodes:
        workflow.add_node(node)

    for source, target in transitions:

        workflow.add_transition(
            Transition(
                source,
                target,
            )
        )

    return workflow


class TouchNode(BaseNode):
    """记录执行顺序。"""

    def __init__(
        self,
        name,
    ):
        self.name = name

    async def execute(
        self,
        state,
        context,
    ):
        state.data.setdefault(
            "visited",
            [],
        ).append(
            self.name
        )

        return state


class RetryNode(BaseNode):
    """第一次失败，第二次成功。"""

    name = "retry"

    def __init__(self):
        self.calls = 0

    async def execute(
        self,
        state,
        context,
    ):
        self.calls += 1

        if self.calls == 1:

            raise RetryableError(
                "temporary error"
            )

        return state


class FailNode(BaseNode):
    """不可重试失败。"""

    name = "fail"

    async def execute(
        self,
        state,
        context,
    ):

        raise NonRetryableError(
            "invalid input"
        )


@pytest.mark.asyncio
async def test_design_gate_state():
    """测试 Design Gate。"""

    state = WorkflowState(
        run_id="phase10-design"
    )

    state.mark_waiting_design()

    assert (
        state.status
        == WorkflowStatus.WAITING_DESIGN
    )

    state.approve()

    assert (
        state.status
        == WorkflowStatus.ANALYZING
    )

    assert state.human_approved is True


@pytest.mark.asyncio
async def test_human_node_pauses_workflow():
    """测试 HumanNode 真正暂停 Workflow。"""

    workflow = build_workflow(
        [
            StartNode(),
            HumanNode(),
            TouchNode("after"),
            EndNode(),
        ],
        [
            ("start", "human_review"),
            ("human_review", "after"),
            ("after", "end"),
        ],
    )

    checkpoint = CheckpointManager()

    engine = WorkflowEngine(
        checkpoint=checkpoint
    )

    result = await engine.run(
        workflow,
        WorkflowState(
            run_id="phase10-human"
        ),
        build_context(),
    )

    assert (
        result.status
        == WorkflowStatus.WAITING_HUMAN
    )

    assert (
        result.current_node
        == "human_review"
    )

    assert "after" not in result.data.get(
        "visited",
        [],
    )


@pytest.mark.asyncio
async def test_manual_pause_and_resume():
    """测试 Pause → Checkpoint → Resume。"""

    workflow = build_workflow(
        [
            StartNode(),
            TouchNode("before"),
            TouchNode("after"),
            EndNode(),
        ],
        [
            ("start", "before"),
            ("before", "after"),
            ("after", "end"),
        ],
    )

    checkpoint = CheckpointManager()

    engine = WorkflowEngine(
        checkpoint=checkpoint
    )

    state = WorkflowState(
        run_id="phase10-pause"
    )

    state.data["visited"] = []

    state = await engine.run(
        workflow,
        state,
        build_context(),
    )

    assert (
        state.status
        == WorkflowStatus.COMPLETED
    )


@pytest.mark.asyncio
async def test_checkpoint_save_and_restore():
    """测试 Checkpoint 保存与恢复。"""

    manager = CheckpointManager()

    state = WorkflowState(
        run_id="phase10-checkpoint"
    )

    state.status = (
        WorkflowStatus.PAUSED
    )

    state.current_node = "task_3"

    state.data["completed_tasks"] = [
        "task_1",
        "task_2",
    ]

    state.retry_count = 1

    await manager.save(
        state
    )

    restored = await manager.load(
        "phase10-checkpoint"
    )

    assert restored is not None

    assert (
        restored.current_node
        == "task_3"
    )

    assert (
        restored.data["completed_tasks"]
        == [
            "task_1",
            "task_2",
        ]
    )

    assert (
        restored.retry_count
        == 1
    )


@pytest.mark.asyncio
async def test_retryable_error_is_retried():
    """测试 RetryableError 会 Retry。"""

    retry_node = RetryNode()

    workflow = build_workflow(
        [
            StartNode(),
            retry_node,
            EndNode(),
        ],
        [
            ("start", "retry"),
            ("retry", "end"),
        ],
    )

    engine = WorkflowEngine(
        retry_policy=RetryPolicy(
            max_retry=3
        )
    )

    result = await engine.run(
        workflow,
        WorkflowState(
            run_id="phase10-retry"
        ),
        build_context(),
    )

    assert (
        result.status
        == WorkflowStatus.COMPLETED
    )

    assert retry_node.calls == 2

    assert result.retry_count == 1


@pytest.mark.asyncio
async def test_retry_policy_limit():
    """测试 Retry 超过最大次数后失败。"""

    class AlwaysFailNode(BaseNode):

        name = "always_fail"

        async def execute(
            self,
            state,
            context,
        ):

            raise RetryableError(
                "temporary failure"
            )

    workflow = build_workflow(
        [
            StartNode(),
            AlwaysFailNode(),
            EndNode(),
        ],
        [
            ("start", "always_fail"),
            ("always_fail", "end"),
        ],
    )

    engine = WorkflowEngine(
        retry_policy=RetryPolicy(
            max_retry=2
        )
    )

    result = await engine.run(
        workflow,
        WorkflowState(
            run_id="phase10-limit"
        ),
        build_context(),
    )

    assert (
        result.status
        == WorkflowStatus.FAILED
    )

    assert (
        result.retry_count == 2
    )


@pytest.mark.asyncio
async def test_non_retryable_error():
    """测试不可重试异常不会 Retry。"""

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

    engine = WorkflowEngine(
        retry_policy=RetryPolicy(
            max_retry=3
        )
    )

    result = await engine.run(
        workflow,
        WorkflowState(
            run_id="phase10-no-retry"
        ),
        build_context(),
    )

    assert (
        result.status
        == WorkflowStatus.FAILED
    )

    assert result.retry_count == 0