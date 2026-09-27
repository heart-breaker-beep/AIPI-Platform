"""Phase 12：单项目完整业务闭环测试。"""

import pytest

from app.workflow.analysis_workflow import (
    build_analysis_workflow,
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
from app.workflow.state import (
    WorkflowState,
    WorkflowStatus,
)


class FakeAgent:

    def __init__(
        self,
        name,
        result,
    ):
        self.name = name
        self.result = result
        self.calls = []

    async def execute(
        self,
        context,
        input_data,
    ):
        self.calls.append(
            dict(input_data)
        )

        return self.result


class FakeReportSkill:

    name = "report_generation"

    async def execute(
        self,
        context,
        input_data,
    ):
        return {
            "report": {
                "format": "markdown",
                "content": (
                    "# Project Intelligence Report"
                ),
            }
        }


def build_context():

    agents = {
        "planner_agent": FakeAgent(
            "planner_agent",
            {
                "tasks": [
                    "repository_analysis_agent",
                    "architecture_analysis_agent",
                    "technology_analysis_agent",
                    "evidence_analysis_agent",
                    "critic_agent",
                ],
                "research_plan": {
                    "plan_version": 1,
                    "tasks": [
                        "repository_analysis_agent",
                        "architecture_analysis_agent",
                        "technology_analysis_agent",
                        "evidence_analysis_agent",
                        "critic_agent",
                    ],
                },
            },
        ),

        "repository_analysis_agent": FakeAgent(
            "repository_analysis_agent",
            {
                "repository": {
                    "name": "demo",
                },
                "readme": "# Demo",
            },
        ),

        "architecture_analysis_agent": FakeAgent(
            "architecture_analysis_agent",
            {
                "architecture": {
                    "modules": [
                        {
                            "file_path":
                                "app/main.py",
                            "content":
                                "print('demo')",
                        }
                    ]
                }
            },
        ),

        "technology_analysis_agent": FakeAgent(
            "technology_analysis_agent",
            {
                "technology_stack": {
                    "frameworks": [
                        "FastAPI"
                    ]
                }
            },
        ),

        "evidence_analysis_agent": FakeAgent(
            "evidence_analysis_agent",
            {
                "evidence": [
                    {
                        "file_path":
                            "app/main.py",
                        "line_start": 1,
                        "line_end": 1,
                        "content":
                            "print('demo')",
                    }
                ]
            },
        ),

        "critic_agent": FakeAgent(
            "critic_agent",
            {
                "passed": True,
                "errors": [],
            },
        ),
    }

    return WorkflowContext(
        agents=agents,
        tools={},
        skills={
            "report_generation":
                FakeReportSkill(),
        },
        config={},
    )


@pytest.mark.asyncio
async def test_phase12_full_business_loop():

    context = build_context()

    workflow = build_analysis_workflow(
        context
    )

    checkpoint = CheckpointManager()

    engine = WorkflowEngine(
        checkpoint=checkpoint
    )

    state = WorkflowState(
        run_id="phase12-full-loop"
    )

    state.data = {
        "repository_id": 1,
        "owner": "demo",
        "repo": "demo-project",
        "repo_url":
            "https://github.com/demo/demo-project",
        "question":
            "分析 Multi-Agent Workflow",
    }

    # -------------------------------------------------
    # 1. Start -> Planner -> Design Gate
    # -------------------------------------------------

    result = await engine.run(
        workflow,
        state,
        context,
    )

    assert (
        result.status
        == WorkflowStatus.WAITING_DESIGN
    )

    assert (
        result.current_node
        == "design_gate"
    )

    assert (
        "research_plan"
        in result.data
    )

    # -------------------------------------------------
    # 2. Human Approve -> Multi-Agent
    # -------------------------------------------------

    result.approve()

    await checkpoint.save(
        result
    )

    result = await engine.resume(
        workflow,
        context,
        result.run_id,
    )

    assert (
        result.status
        == WorkflowStatus.WAITING_HUMAN
    )

    assert (
        result.current_node
        == "human_review"
    )

    assert (
        result.data[
            "executed_tasks"
        ]
        == [
            "repository_analysis_agent",
            "architecture_analysis_agent",
            "technology_analysis_agent",
            "evidence_analysis_agent",
            "critic_agent",
        ]
    )

    assert (
        result.data[
            "critic_agent"
        ]["passed"]
        is True
    )

    # -------------------------------------------------
    # 3. Human Review Approve -> Finalizer
    # -------------------------------------------------

    result.approve()

    await checkpoint.save(
        result
    )

    result = await engine.resume(
        workflow,
        context,
        result.run_id,
    )

    assert (
        result.status
        == WorkflowStatus.COMPLETED
    )

    assert (
        result.current_node
        == "end"
    )

    assert (
        "final_report"
        in result.data
    )

    assert (
        result.data[
            "final_report"
        ]["report"]["format"]
        == "markdown"
    )


@pytest.mark.asyncio
async def test_phase12_checkpoint_survives_design_gate():

    context = build_context()

    workflow = build_analysis_workflow(
        context
    )

    checkpoint = CheckpointManager()

    engine = WorkflowEngine(
        checkpoint=checkpoint
    )

    state = WorkflowState(
        run_id="phase12-checkpoint"
    )

    state.data = {
        "repository_id": 1,
        "owner": "demo",
        "repo": "demo",
        "question": "test",
    }

    result = await engine.run(
        workflow,
        state,
        context,
    )

    assert (
        result.status
        == WorkflowStatus.WAITING_DESIGN
    )

    restored = await checkpoint.load(
        "phase12-checkpoint"
    )

    assert restored is not None

    assert (
        restored.current_node
        == "design_gate"
    )

    assert (
        restored.data[
            "research_plan"
        ]["plan_version"]
        == 1
    )