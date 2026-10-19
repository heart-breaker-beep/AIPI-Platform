"""Phase 11 Memory 测试。"""

from types import SimpleNamespace

from unittest.mock import AsyncMock

import pytest

from app.persistence.repositories.project_memory import ProjectMemoryRepository

from app.analysis.memory.project_memory import (
    ProjectMemory,
)


class FakeScalarsResult:
    """模拟 SQLAlchemy scalars 查询结果。"""

    def __init__(self, values):
        self.values = values

    def scalars(self):
        return self

    def all(self):
        return self.values


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
        ProjectMemoryRepository(session)
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
