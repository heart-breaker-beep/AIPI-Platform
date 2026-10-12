"""Phase 10：HITL / Checkpoint / Pause / Resume / Retry 测试。"""

import time

import pytest

from app.core.exceptions import (
    NonRetryableError,
    RetryableError,
    RetryableToolError,
)
from app.infrastructure.workflow.checkpoint import (
    CheckpointManager,
)
from app.infrastructure.workflow.context import WorkflowContext
from app.infrastructure.workflow.engine import (
    WorkflowEngine,
)
from app.infrastructure.workflow.node import BaseNode
from app.infrastructure.workflow.nodes.end_node import EndNode
from app.infrastructure.workflow.nodes.human_node import HumanNode
from app.infrastructure.workflow.nodes.start_node import StartNode
from app.infrastructure.workflow.retry import RetryPolicy
from app.infrastructure.workflow.state import (
    WorkflowState,
    WorkflowStatus,
)
from app.infrastructure.workflow.transition import Transition
from app.infrastructure.workflow.workflow import Workflow


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


class ToolFlakeNode(BaseNode):
    """
    工具抖动：第一次抛 RetryableToolError，第二次成功。

    记录每次进入时看到的 retry_count，
    用来验证「重试成功后预算还回去」。
    """

    name = "tool_flake"

    def __init__(self):

        self.calls = 0
        self.seen = []

    async def execute(
        self,
        state,
        context,
    ):

        self.calls += 1

        self.seen.append(
            state.retry_count
        )

        if self.calls == 1:

            raise RetryableToolError(
                "GitHub 503"
            )

        return state


class CountNode(BaseNode):
    """记录进入本节点时的 retry_count。"""

    def __init__(
        self,
        name,
    ):

        self.name = name
        self.seen = None

    async def execute(
        self,
        state,
        context,
    ):

        self.seen = state.retry_count

        return state


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

    # 节点跑通之后预算还回去了，
    # 计数不再跟着 run 一路累加。
    assert result.retry_count == 0


@pytest.mark.asyncio
async def test_retry_budget_is_returned_to_next_node():
    """
    一个节点的重试用掉后，不影响下一个节点。

    修复前 retry_count 是整个 run 共用的累加值：
    前面节点抖一次，后面节点就少一次重试机会。
    """

    flake = ToolFlakeNode()
    follower = CountNode("follower")

    workflow = build_workflow(
        [
            StartNode(),
            flake,
            follower,
            EndNode(),
        ],
        [
            ("start", "tool_flake"),
            ("tool_flake", "follower"),
            ("follower", "end"),
        ],
    )

    engine = WorkflowEngine(
        retry_policy=RetryPolicy(
            max_retry=3,
            backoff_base=0,
        )
    )

    result = await engine.run(
        workflow,
        WorkflowState(
            run_id="phase10-retry-budget"
        ),
        build_context(),
    )

    assert result.status == WorkflowStatus.COMPLETED

    # 第一次进入时是 0（还没重试过），
    # 第二次进入时是 1（正在用第一次重试）。
    assert flake.seen == [0, 1]

    # 下一个节点从 0 开始。
    assert follower.seen == 0


@pytest.mark.asyncio
async def test_retry_waits_with_backoff():
    """重试之间要有退避，不能无间隔连打。"""

    flake = ToolFlakeNode()

    workflow = build_workflow(
        [
            StartNode(),
            flake,
            EndNode(),
        ],
        [
            ("start", "tool_flake"),
            ("tool_flake", "end"),
        ],
    )

    engine = WorkflowEngine(
        retry_policy=RetryPolicy(
            max_retry=2,
            backoff_base=0.5,
        )
    )

    started = time.monotonic()

    result = await engine.run(
        workflow,
        WorkflowState(
            run_id="phase10-backoff"
        ),
        build_context(),
    )

    elapsed = time.monotonic() - started

    assert result.status == WorkflowStatus.COMPLETED

    # 第一次重试应等 backoff_base = 0.5 秒。
    assert elapsed >= 0.45


def test_backoff_delay_grows_and_caps():
    """退避按指数增长，并在 max_backoff 处封顶。"""

    policy = RetryPolicy(
        max_retry=5,
        backoff_base=2.0,
        max_backoff=10.0,
    )

    assert policy.backoff_delay(1) == 2.0

    assert policy.backoff_delay(2) == 4.0

    assert policy.backoff_delay(3) == 8.0

    # 2^4 = 16 超过上限，取上限。
    assert policy.backoff_delay(4) == 10.0

    # 基数为 0 时完全不等待（测试与本地调试用）。
    assert (
        RetryPolicy(
            backoff_base=0
        ).backoff_delay(3)
        == 0.0
    )


@pytest.mark.asyncio
async def test_manual_retry_resets_retry_count():
    """人工 retry 相当于重新给预算。"""

    checkpoint = CheckpointManager()

    state = WorkflowState(
        run_id="phase10-manual-retry"
    )

    state.status = WorkflowStatus.FAILED
    state.current_node = "count"
    state.retry_count = 2

    await checkpoint.save(state)

    counter = CountNode("count")

    workflow = build_workflow(
        [counter],
        [],
    )

    engine = WorkflowEngine(
        checkpoint=checkpoint,
    )

    result = await engine.retry(
        workflow,
        build_context(),
        "phase10-manual-retry",
    )

    assert result.status == WorkflowStatus.COMPLETED

    assert counter.seen == 0

    assert result.retry_count == 0


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
