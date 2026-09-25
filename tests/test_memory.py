"""Phase 11 Memory 测试。"""

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.memory.run_memory import (
    RunMemory,
)

from app.memory.project_memory import (
    ProjectMemory,
)


class FakeScalarResult:
    """模拟 SQLAlchemy scalar 查询结果。"""

    def __init__(self, value):
        self.value = value

    def scalar_one_or_none(self):
        return self.value


class FakeScalarsResult:
    """模拟 SQLAlchemy scalars 查询结果。"""

    def __init__(self, values):
        self.values = values

    def scalars(self):
        return self

    def all(self):
        return self.values


@pytest.mark.asyncio
async def test_run_memory_loads_run_and_checkpoint():
    """Run Memory 应能够组合 Run / Task / Checkpoint / Evidence。"""

    session = AsyncMock()

    run = SimpleNamespace(
        id="run-1",
        repository_id=10,
        question="Workflow怎么实现？",
        status="ANALYZING",
        current_node="workflow",
    )

    repository = SimpleNamespace(
        id=10,
        url="https://github.com/demo/repo",
        owner="demo",
        name="repo",
        description="demo",
        language="Python",
    )

    task = SimpleNamespace(
        id=1,
        task_type="architecture",
        status="completed",
        input={},
        output={
            "result": "workflow"
        },
        error=None,
        retry_count=0,
        created_at=None,
    )

    evidence = SimpleNamespace(
        id="ev-1",
        source_type="code",
        file_path="app/workflow.py",
        line_start=10,
        line_end=20,
        content="class WorkflowEngine",
        verification_status="VERIFIED",
    )

    checkpoint = SimpleNamespace(
        data={
            "research_plan": {
                "tasks": [
                    "architecture"
                ]
            }
        },
        outputs=[
            {
                "agent": "architecture"
            }
        ],
        status="ANALYZING",
        current_node="workflow",
        errors=[],
        retry_count=0,
        pause_reason=None,
        human_approved=True,
        checkpoint_version=2,
    )

    session.execute.side_effect = [
        FakeScalarResult(run),
        FakeScalarsResult([task]),
    ]

    session.get.return_value = repository

    memory = RunMemory(
        session
    )

    memory.checkpoint_repository.get_latest = (
        AsyncMock(
            return_value=checkpoint
        )
    )

    memory.evidence_repository.list_by_repository = (
        AsyncMock(
            return_value=[evidence]
        )
    )

    result = await memory.load(
        "run-1"
    )

    assert (
        result["question"]
        == "Workflow怎么实现？"
    )

    assert (
        result["research_plan"]["tasks"]
        == ["architecture"]
    )

    assert (
        result["agent_outputs"]
        == [
            {
                "agent": "architecture"
            }
        ]
    )

    assert (
        result["evidences"][0]["file_path"]
        == "app/workflow.py"
    )


@pytest.mark.asyncio
async def test_project_memory_filters_current_run():
    """Project Memory 不应该把当前 Run 再作为历史 Memory 返回。"""

    session = AsyncMock()

    run1 = SimpleNamespace(
        id="run-1",
        question="Workflow",
        status="COMPLETED",
        current_node="end",
        created_at=SimpleNamespace(
            isoformat=lambda:
            "2026-09-25T00:00:00"
        ),
    )

    run2 = SimpleNamespace(
        id="run-2",
        question="Agent",
        status="COMPLETED",
        current_node="end",
        created_at=SimpleNamespace(
            isoformat=lambda:
            "2026-09-24T00:00:00"
        ),
    )

    task = SimpleNamespace(
        run_id="run-2",
        task_type="agent",
        status="completed",
        output={
            "agent": "planner"
        },
        error=None,
    )

    session.execute.side_effect = [
        FakeScalarsResult(
            [
                run1,
                run2,
            ]
        ),
        FakeScalarsResult(
            [
                task
            ]
        ),
    ]

    memory = ProjectMemory(
        session
    )

    result = await memory.load(
        10,
        exclude_run_id="run-1",
    )

    assert len(result) == 1

    assert (
        result[0]["run_id"]
        == "run-2"
    )

    assert (
        result[0]["tasks"][0][
            "task_type"
        ]
        == "agent"
    )