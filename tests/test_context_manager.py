"""Phase 11 Context Manager 测试。"""

import pytest

from app.context.manager import (
    ContextItem,
    ContextManager,
)


class FakeMemoryManager:
    """模拟 Memory Manager。"""

    async def retrieve(
        self,
        **kwargs,
    ):
        return {
            "run_memory": {
                "question": (
                    "Workflow怎么实现？"
                ),
                "research_plan": {
                    "tasks": [
                        "workflow"
                    ]
                },
                "agent_outputs": [
                    {
                        "agent": "architecture",
                        "result": (
                            "使用自研 Workflow"
                        ),
                    }
                ],
                "evidences": [
                    {
                        "id": "ev-1",
                        "file_path": (
                            "app/workflow/engine.py"
                        ),
                        "line_start": 1,
                        "line_end": 20,
                        "content": (
                            "class WorkflowEngine"
                        ),
                    }
                ],
            },
            "project_memory": [
                {
                    "run_id": "old-run",
                    "question": (
                        "Agent怎么实现？"
                    ),
                    "status": "COMPLETED",
                }
            ],
        }


@pytest.mark.asyncio
async def test_context_manager_retrieval_filter_and_assembly():
    """Context Manager 应完成 Retrieve / Filter / Assembly。"""

    async def retriever(query):
        return [
            {
                "content": (
                    "WorkflowEngine "
                    "executes workflow nodes"
                ),
                "score": 0.9,
                "file_path": (
                    "app/workflow/engine.py"
                ),
            },
            {
                "content": (
                    "irrelevant database text"
                ),
                "score": 0.1,
            },
        ]

    manager = ContextManager(
        FakeMemoryManager(),
        retriever=retriever,
        max_items=5,
        max_chars=5000,
    )

    result = await manager.build(
        run_id="run-1",
        repository_id=10,
        query="Workflow怎么实现？",
        workflow_state={
            "status": "ANALYZING",
            "current_node": "workflow",
        },
    )

    assert (
        "Current Question"
        in result["text"]
    )

    assert (
        "WorkflowEngine"
        in result["text"]
    )

    assert result["items"]

    assert all(
        item["content"].strip()
        for item in result["items"]
    )


def test_context_manager_deduplicates_and_limits():
    """Context Manager 应去重并限制 Context 数量。"""

    manager = ContextManager(
        FakeMemoryManager(),
        max_items=2,
    )

    items = manager.filter_and_rank(
        [
            ContextItem(
                source="test",
                content="workflow engine",
                score=1.0,
            ),
            ContextItem(
                source="test",
                content="workflow engine",
                score=0.5,
            ),
            ContextItem(
                source="test",
                content="database",
                score=0.2,
            ),
        ],
        "workflow",
    )

    assert len(items) == 2

    assert (
        items[0].content
        == "workflow engine"
    )


# ----------------------------------------------------------------
# 跨 run 记忆的保底名额
# ----------------------------------------------------------------


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


def test_select_reserves_project_memory_slots():
    """
    run 内高分条目占满名额时，跨 run 记忆仍须有保底名额。

    这正是修复的那个 bug：project_memory 权重只有 2.0，
    而 evidence 是 4.0 且一次最多 6 条，纯按分数截断时
    历史记忆永远进不来 —— 而它恰恰是 Context 唯一
    不可替代的内容。
    """

    manager = ContextManager(
        FakeMemoryManager(),
        max_items=5,
    )

    items = [
        ContextItem(
            source="run_memory.evidence",
            content=f"ev-{index}",
            score=4.0,
        )
        for index in range(10)
    ] + [
        ContextItem(
            source=ContextManager.PROJECT_MEMORY_SOURCE,
            content=f"hist-{index}",
            score=2.0,
        )
        for index in range(4)
    ]

    # 旧的纯截断行为会把历史全部挤掉。
    ranked = manager.filter_and_rank(
        items,
        "",
    )

    assert not [
        item
        for item in ranked
        if item.source
        == ContextManager.PROJECT_MEMORY_SOURCE
    ]

    # select 保底后历史必然在。
    picked = manager.select(items, "")

    assert len(picked) == 5

    assert (
        len(
            [
                item
                for item in picked
                if item.source
                == ContextManager.PROJECT_MEMORY_SOURCE
            ]
        )
        == ContextManager.RESERVED_PROJECT_MEMORY
    )


# ----------------------------------------------------------------
# 文本组装
# ----------------------------------------------------------------


def test_assemble_deduplicates_identical_instruction():
    """question 与 user_instruction 相同时不重复输出小节。"""

    manager = ContextManager(FakeMemoryManager())

    text = manager.assemble(
        query="分析 workflow",
        items=[],
        user_instruction="分析 workflow",
    )

    assert text.count("## Current Question") == 1

    assert "## User Instruction" not in text


def test_assemble_keeps_retrieved_context_under_large_state():
    """
    state 再大也不能把 Retrieved Context 挤掉。

    原实现把整个 state 序列化后排在 Retrieved Context 之前，
    再全局尾截断 —— state 一到几十 KB，有内容的小节就整段消失。
    """

    manager = ContextManager(
        FakeMemoryManager(),
        max_chars=5000,
    )

    text = manager.assemble(
        query="分析 workflow",
        items=[
            ContextItem(
                source=ContextManager.PROJECT_MEMORY_SOURCE,
                content="历史记忆内容",
                score=2.0,
            )
        ],
        workflow_state={"blob": "x" * 200_000},
    )

    assert "## Retrieved Context" in text

    assert "历史记忆内容" in text

    # 200KB 的 state 被限长，而不是把历史挤出去。
    assert len(text) < 10_000


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