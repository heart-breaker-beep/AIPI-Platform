"""
Retry / Approve / Resume 恢复流程的身份字段补齐测试。

背景
====

真实缺陷：一个 run 跑到最后阶段时失败，错误是

    ValueError: Repository analysis requires 'owner' and 'repo'.

点 Retry 之后仍然失败，问题出在恢复流程的时序：

    orchestrator.retry_workflow()
      |-- load checkpoint（缺 owner / repo）
      |-- 把字段补进内存里的 state，但没有落盘
      `-- engine.retry()
            `-- _restore() 重新从 checkpoint 读一份
                  `-- 内存里补的字段丢了
                        `-- 同一个节点原样再失败一次

所以身份字段必须满足两件事：

1. 从权威来源取（repositories 表的 owner / name），
   而不是从 repo_url 反解 —— 反解失败时旧实现会静默跳过，
   等于什么都没补
2. 在把状态交给 engine 之前落盘，
   否则 engine 重新加载 checkpoint 时这次补齐就白做了

这组测试盯住的就是这两点。
"""

import copy

import pytest

from app.analysis.workflow import (
    AnalysisWorkflowOrchestrator,
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
from app.analysis.nodes.end_node import EndNode
from app.workflow.state import (
    WorkflowState,
    WorkflowStatus,
)
from app.workflow.transition import Transition
from app.workflow.workflow import Workflow


RUN_ID = "retry-identity"


class NeedsRepoNode(BaseNode):
    """
    模拟 repository_analysis_skill 的前置校验。

    缺 owner / repo 时抛的就是线上那一条 ValueError，
    这样测试失败时的信息跟真实事故一致。
    """

    name = "plan_executor"

    async def execute(
        self,
        state,
        context,
    ):

        owner = state.data.get("owner")
        repo = state.data.get("repo")

        if not owner or not repo:
            raise ValueError(
                "Repository analysis requires "
                "'owner' and 'repo'."
            )

        # 记下这一节点实际拿到了什么，
        # 用于断言补字段确实被下游看见。
        state.data["plan_executor"] = {
            "owner": owner,
            "repo": repo,
        }

        return state


class RecordingCheckpoint(CheckpointManager):
    """
    记录每次落盘的 data。

    落盘顺序是这次修复的关键：
    补写的字段必须出现在 engine 自己那次保存之前。
    """

    def __init__(self):

        super().__init__()

        self.saved = []

    async def save(
        self,
        state,
    ):

        run_id = await super().save(state)

        self.saved.append(
            copy.deepcopy(state.data)
        )

        return run_id


def build_workflow():
    """设计闸门 -> 计划执行 -> 结束。"""

    workflow = Workflow()

    workflow.add_node(
        NeedsRepoNode()
    )

    workflow.add_node(
        EndNode()
    )

    workflow.add_transition(
        Transition("design_gate", "plan_executor")
    )

    workflow.add_transition(
        Transition("plan_executor", "end")
    )

    return workflow


def build_orchestrator(checkpoint):
    """用真实的 Engine / CheckpointManager 组装编排器。"""

    return AnalysisWorkflowOrchestrator(
        engine=WorkflowEngine(checkpoint=checkpoint),
        context_factory=ContextFactory(),
        checkpoint_manager=checkpoint,
        workflow_builder=lambda context: build_workflow(),
    )


class ContextFactory:
    """
    只提供 repository_id 的 Context 工厂。

    这条链路（编排器 -> 引擎 -> 节点）不碰数据库，
    所以不需要真实的 WorkflowContext。
    """

    def create(
        self,
        repository_id,
    ):

        return WorkflowContext(
            agents={},
            tools={},
            skills={},
            config={"repository_id": repository_id},
        )


async def seed_checkpoint(
    checkpoint,
    status,
    current_node,
    data=None,
):
    """
    造一个缺身份字段的 checkpoint。

    刻意连 repo_url 都不给：
    旧实现是「从 state.data["repo_url"] 反解」，
    没有 repo_url 就什么都补不出来 ——
    这正是线上 Retry 一直失败的形态。
    """

    state = WorkflowState(run_id=RUN_ID)

    state.data = copy.deepcopy(
        data
        if data is not None
        else {"question": "分析这个项目"}
    )

    state.status = status
    state.current_node = current_node

    await checkpoint.save(state)

    # 种子数据不算「恢复流程的写入」，
    # 否则 saved[0] 就不是被测代码写的那一笔。
    checkpoint.saved.clear()

    return state


def identity():
    """Application 层从 Repository 行构造的身份字段。"""

    return {
        "run_id": RUN_ID,
        "repository_id": 7,
        "repo_url": "https://github.com/demo/proj",
        "owner": "demo",
        "repo": "proj",
    }


# ----------------------------------------------------------------
# 反证：不落盘就一定会原地再失败
# ----------------------------------------------------------------


@pytest.mark.asyncio
async def test_in_memory_backfill_is_lost_after_engine_reload():
    """
    只在内存里补字段，engine 重新加载后会丢。

    这条测试复现的是修复前的时序，
    用来证明上面那些断言不是空转：
    没有落盘时，节点确实会因为缺字段再失败一次。
    """

    checkpoint = RecordingCheckpoint()

    await seed_checkpoint(
        checkpoint,
        WorkflowStatus.FAILED,
        "plan_executor",
    )

    # 模拟「只有内存里补了字段」的旧逻辑。
    state = await checkpoint.load(RUN_ID)

    state.data["owner"] = "demo"
    state.data["repo"] = "proj"

    result = await WorkflowEngine(
        checkpoint=checkpoint
    ).retry(
        build_workflow(),
        ContextFactory().create(7),
        RUN_ID,
    )

    assert result.status == WorkflowStatus.FAILED

    assert "owner" in result.errors[-1]


# ----------------------------------------------------------------
# Retry
# ----------------------------------------------------------------


@pytest.mark.asyncio
async def test_retry_backfills_identity_and_persists_it():
    """Retry 时补全身份字段并落盘，失败节点能重新跑通。"""

    checkpoint = RecordingCheckpoint()

    await seed_checkpoint(
        checkpoint,
        WorkflowStatus.FAILED,
        "plan_executor",
    )

    result = await build_orchestrator(
        checkpoint
    ).retry_workflow(
        RUN_ID,
        7,
        identity=identity(),
    )

    assert result.status == WorkflowStatus.COMPLETED

    assert result.data["plan_executor"] == {
        "owner": "demo",
        "repo": "proj",
    }

    # 关键断言：第一笔写入就带着身份字段，
    # 说明补齐发生在 engine 重新加载 checkpoint 之前。
    assert checkpoint.saved[0]["owner"] == "demo"

    assert checkpoint.saved[0]["repo"] == "proj"


@pytest.mark.asyncio
async def test_retry_without_identity_does_not_fake_success():
    """
    拿不到身份字段时保持原行为。

    修复不该靠猜把 run 推成成功：
    没有仓库坐标就还是以原来的错误失败。
    """

    checkpoint = RecordingCheckpoint()

    await seed_checkpoint(
        checkpoint,
        WorkflowStatus.FAILED,
        "plan_executor",
    )

    result = await build_orchestrator(
        checkpoint
    ).retry_workflow(
        RUN_ID,
        7,
    )

    assert result.status == WorkflowStatus.FAILED

    assert "owner" in result.errors[-1]


# ----------------------------------------------------------------
# Resume / Approve
# ----------------------------------------------------------------


@pytest.mark.asyncio
async def test_resume_backfills_identity_before_reload():
    """Resume 从 PAUSED checkpoint 恢复时同样先补字段再落盘。"""

    checkpoint = RecordingCheckpoint()

    await seed_checkpoint(
        checkpoint,
        WorkflowStatus.PAUSED,
        "design_gate",
    )

    result = await build_orchestrator(
        checkpoint
    ).resume_workflow(
        RUN_ID,
        7,
        identity=identity(),
    )

    assert result.status == WorkflowStatus.COMPLETED

    assert result.data["plan_executor"] is not None

    assert checkpoint.saved[0]["owner"] == "demo"


@pytest.mark.asyncio
async def test_approve_backfills_identity():
    """Approve 通过设计闸门后继续执行时也要带上身份字段。"""

    checkpoint = RecordingCheckpoint()

    await seed_checkpoint(
        checkpoint,
        WorkflowStatus.WAITING_DESIGN,
        "design_gate",
    )

    result = await build_orchestrator(
        checkpoint
    ).approve_workflow(
        RUN_ID,
        7,
        identity=identity(),
    )

    assert result.status == WorkflowStatus.COMPLETED

    assert result.data["plan_executor"] is not None

    assert checkpoint.saved[0]["repo"] == "proj"


# ----------------------------------------------------------------
# 身份字段补齐本身
# ----------------------------------------------------------------


def test_apply_identity_reports_whether_it_wrote():
    """没有变化就不落盘，有变化才要求调用方保存。"""

    complete = WorkflowState(run_id=RUN_ID)

    complete.data = identity()

    assert (
        AnalysisWorkflowOrchestrator._apply_identity(
            complete,
            identity(),
        )
        is False
    )

    empty = WorkflowState(run_id=RUN_ID)

    empty.data = {"question": "分析这个项目"}

    assert (
        AnalysisWorkflowOrchestrator._apply_identity(
            empty,
            identity(),
        )
        is True
    )

    assert empty.data["owner"] == "demo"

    assert empty.data["repo_url"] == "https://github.com/demo/proj"


def test_apply_identity_ignores_none_argument():
    """identity 为 None 时不能写入 None 覆盖已有值。"""

    state = WorkflowState(run_id=RUN_ID)

    state.data = {"owner": "demo", "repo": "proj"}

    assert (
        AnalysisWorkflowOrchestrator._apply_identity(
            state,
            None,
        )
        is False
    )

    assert state.data["owner"] == "demo"


def test_identity_data_takes_owner_from_repository_row():
    """
    身份字段来自 repositories 表，不是从 URL 反解。

    反解只在 URL 规范时才成立，
    而且解析失败时旧实现会静默 pass ——
    等于把「补不齐」伪装成「不用补」。
    """

    # 放在函数内导入：这个模块会拉起 FastAPI / Skills 整条依赖链，
    # 只有这一条测试需要它。
    from app.services.analysis_service import (
        AnalysisService,
    )

    class Run:

        id = RUN_ID
        repository_id = 7

    class Repository:

        url = "https://github.com/demo/renamed-project"
        owner = "demo"
        name = "renamed-project"

    data = AnalysisService._identity_data(
        Run(),
        Repository(),
    )

    assert data == {
        "run_id": RUN_ID,
        "repository_id": 7,
        "repo_url": "https://github.com/demo/renamed-project",
        "owner": "demo",
        "repo": "renamed-project",
    }


@pytest.mark.asyncio
async def test_replan_replaces_previous_plan_and_returns_to_design_gate():
    """重新规划由分析组件重置旧产物，并通过真实引擎回到审批节点。"""
    from app.analysis.nodes.design_gate_node import DesignGateNode

    class PlannerNode(BaseNode):
        name = "planner_agent"

        async def execute(self, state, context):
            assert "research_plan" not in state.data
            assert "planner_agent" not in state.data
            state.data["planner_agent"] = {
                "research_plan": {"question": state.data["question"]}
            }
            return state

    checkpoint = RecordingCheckpoint()
    await seed_checkpoint(
        checkpoint,
        WorkflowStatus.WAITING_DESIGN,
        "design_gate",
        data={
            **identity(),
            "question": "旧问题",
            "research_plan": {"question": "旧问题"},
            "planner_agent": {"research_plan": {"question": "旧问题"}},
            "executed_tasks": ["old-task"],
            "count": 4,
        },
    )
    workflow = Workflow()
    workflow.add_node(PlannerNode())
    workflow.add_node(DesignGateNode())
    workflow.add_transition(Transition("planner_agent", "design_gate"))
    orchestrator = AnalysisWorkflowOrchestrator(
        engine=WorkflowEngine(checkpoint=checkpoint),
        context_factory=ContextFactory(),
        checkpoint_manager=checkpoint,
        workflow_builder=lambda context: workflow,
    )
    result = await orchestrator.replan_workflow(RUN_ID, 7, "新问题")
    assert result.status == WorkflowStatus.WAITING_DESIGN
    assert result.current_node == "design_gate"
    assert result.data["research_plan"] == {"question": "新问题"}
    assert result.data["owner"] == "demo"
    assert "executed_tasks" not in result.data
    assert "count" not in result.data
