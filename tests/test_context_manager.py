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