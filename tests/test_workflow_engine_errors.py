"""
WorkflowEngine 失败语义测试。

覆盖：

1. 空异常消息不会丢失异常类型
2. FAILED Checkpoint 恢复时重新执行失败节点
3. 不破坏 PAUSED / WAITING_* 的原有 resume 语义
"""

import httpx
import pytest

from app.core.exceptions import (
    NonRetryableError,
)
from app.workflow.checkpoint import (
    CheckpointManager,
)
from app.workflow.context import (
    WorkflowContext,
)
from app.workflow.engine import (
    WorkflowEngine,
)
from app.workflow.node import BaseNode
from app.workflow.nodes.end_node import (
    EndNode,
)
from app.workflow.nodes.start_node import (
    StartNode,
)
from app.workflow.state import (
    WorkflowState,
    WorkflowStatus,
)
from app.workflow.transition import (
    Transition,
)
from app.workflow.workflow import (
    Workflow,
)


class EmptyMessageNode(BaseNode):
    """
    抛出 str() 为空的异常。

    httpx.ReadTimeout('') 就是这种情况：
    str(error) == ''，args == ('',)。
    """

    name = "empty_error"

    async def execute(
        self,
        state,
        context,
    ):

        raise httpx.ReadTimeout("")


class MessageNode(BaseNode):
    """抛出带消息的异常。"""

    name = "message_error"

    async def execute(
        self,
        state,
        context,
    ):

        raise ValueError("planner result missing")


class FailOnceNode(BaseNode):
    """第一次失败，之后成功（模拟瞬时网络故障）。"""

    name = "plan_executor"

    def __init__(
        self,
        name="plan_executor",
    ):

        self.name = name

    async def execute(
        self,
        state,
        context,
    ):

        state.data["attempts"] = (
            state.data.get("attempts", 0) + 1
        )

        if state.data["attempts"] == 1:

            raise NonRetryableError("boom")

        state.data.setdefault(
            "visited",
            [],
        ).append(self.name)

        return state


class RecordNode(BaseNode):
    """记录执行顺序的节点。"""

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
        ).append(self.name)

        return state


class PauseGateNode(BaseNode):
    """模拟 Design Gate：主动进入 WAITING_DESIGN。"""

    name = "design_gate"

    async def execute(
        self,
        state,
        context,
    ):

        state.data["pause_count"] = (
            state.data.get("pause_count", 0) + 1
        )

        state.status = (
            WorkflowStatus.WAITING_DESIGN
        )

        return state


def build_workflow(
    nodes,
    transitions,
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
async def test_empty_error_message_keeps_exception_type():
    """
    空异常消息必须降级为异常类型名。

    修复前：errors == [""]
    修复后：errors == ["ReadTimeout"]
    """

    workflow = build_workflow(
        [
            StartNode(),
            EmptyMessageNode(),
            EndNode(),
        ],
        [
            ("start", "empty_error"),
            ("empty_error", "end"),
        ],
    )

    result = await WorkflowEngine().run(
        workflow,
        WorkflowState(run_id="wf-empty-error"),
        build_context(),
    )

    assert result.status == "FAILED"

    assert result.current_node == "empty_error"

    assert result.errors == ["ReadTimeout"]


@pytest.mark.asyncio
async def test_non_empty_error_message_is_preserved():
    """非空消息必须原样保留（保持既有格式）。"""

    workflow = build_workflow(
        [
            StartNode(),
            MessageNode(),
            EndNode(),
        ],
        [
            ("start", "message_error"),
            ("message_error", "end"),
        ],
    )

    result = await WorkflowEngine().run(
        workflow,
        WorkflowState(run_id="wf-message-error"),
        build_context(),
    )

    assert result.status == "FAILED"

    assert result.errors == [
        "planner result missing"
    ]


@pytest.mark.asyncio
async def test_failed_resume_reexecutes_failed_node():
    """
    FAILED 恢复必须重新执行失败节点，而不是跳到下一个节点。

    修复前：current_node=plan_executor 会直接跳到 human_review，
            5 个 Agent 一个都不会执行。
    修复后：重新执行 plan_executor。
    """

    workflow = build_workflow(
        [
            StartNode(),
            FailOnceNode(),
            RecordNode("human_review"),
            RecordNode("finalizer"),
            EndNode(),
        ],
        [
            ("start", "plan_executor"),
            ("plan_executor", "human_review"),
            ("human_review", "finalizer"),
            ("finalizer", "end"),
        ],
    )

    manager = CheckpointManager()

    engine = WorkflowEngine(
        checkpoint=manager
    )

    first = await engine.run(
        workflow,
        WorkflowState(run_id="wf-failed-resume"),
        build_context(),
    )

    assert first.status == "FAILED"

    assert first.current_node == "plan_executor"

    assert first.errors == ["boom"]

    assert first.data["attempts"] == 1

    assert first.data.get("visited", []) == []

    # 从 FAILED Checkpoint 恢复。
    restored = await engine.run(
        workflow,
        WorkflowState(run_id="wf-failed-resume"),
        build_context(),
        resume_from="wf-failed-resume",
    )

    # 失败节点被重新执行。
    assert restored.data["attempts"] == 2

    assert restored.data["visited"] == [
        "plan_executor",
        "human_review",
        "finalizer",
    ]

    # errors 被清空。
    assert restored.errors == []

    assert restored.status == "COMPLETED"


@pytest.mark.asyncio
async def test_pause_resume_still_skips_completed_node():
    """
    Pause / Human Gate 语义不能被破坏。

    WAITING_DESIGN 表示 design_gate 已完成，
    恢复时必须从下一个节点继续，而不是重跑 design_gate。
    """

    workflow = build_workflow(
        [
            StartNode(),
            PauseGateNode(),
            RecordNode("plan_executor"),
            EndNode(),
        ],
        [
            ("start", "design_gate"),
            ("design_gate", "plan_executor"),
            ("plan_executor", "end"),
        ],
    )

    manager = CheckpointManager()

    engine = WorkflowEngine(
        checkpoint=manager
    )

    paused = await engine.run(
        workflow,
        WorkflowState(run_id="wf-pause-gate"),
        build_context(),
    )

    assert paused.status == "WAITING_DESIGN"

    assert paused.current_node == "design_gate"

    assert paused.data["pause_count"] == 1

    resumed = await engine.run(
        workflow,
        WorkflowState(run_id="wf-pause-gate"),
        build_context(),
        resume_from="wf-pause-gate",
    )

    # design_gate 没有被重新执行。
    assert resumed.data["pause_count"] == 1

    assert resumed.data["visited"] == [
        "plan_executor"
    ]

    assert resumed.status == "COMPLETED"
