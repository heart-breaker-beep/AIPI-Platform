"""Phase 11 Context Manager 测试。"""

import pytest

from app.infrastructure.enrichment.context.manager import (
    ContextManager,
)


class FakeHistoryMemory:
    """假的 MemoryManager，只实现 get_project_memory。"""

    def __init__(self, memories=None):
        self.memories = (
            memories
            if memories is not None
            else [
                {
                    "run_id": "old-run",
                    "question": "Agent怎么实现？",
                    "status": "COMPLETED",
                    "created_at": "2026-01-01T00:00:00",
                    "tasks": [
                        {
                            "task_type": "architecture",
                            "status": "COMPLETED",
                            # 任务 output 原文可能几十 KB，
                            # 绝不能进 prompt。
                            "output": "x" * 5000,
                        }
                    ],
                }
            ]
        )

    async def get_project_memory(
        self,
        repository_id,
        **kwargs,
    ):
        return self.memories


# ----------------------------------------------------------------
# 文本组装
# ----------------------------------------------------------------


@pytest.mark.asyncio
async def test_build_history_is_compact_and_drops_task_output():
    """历史块必须小而稳，且绝不带上任务 output 原文。"""

    manager = ContextManager(FakeHistoryMemory())

    text = await manager.build_history(
        run_id="run-1",
        repository_id=10,
    )

    assert text.startswith("<history>")

    assert text.endswith("</history>")

    assert "Agent怎么实现？" in text

    assert "architecture:COMPLETED" in text

    # output 原文不进 prompt。
    assert "x" * 100 not in text

    assert len(text) <= ContextManager.HISTORY_MAX_CHARS


@pytest.mark.asyncio
async def test_build_history_empty_without_history():
    """没有历史 run 时返回空串，调用方据此不占位。"""

    manager = ContextManager(
        FakeHistoryMemory(memories=[])
    )

    assert (
        await manager.build_history(
            run_id="run-1",
            repository_id=10,
        )
        == ""
    )
