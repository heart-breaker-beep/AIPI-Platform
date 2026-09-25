"""Phase 11 Context Retriever 测试。"""

import pytest

from app.context.retriever import (
    QdrantContextRetriever,
)


class FakeEmbedding:
    """模拟 Embedding Provider。"""

    def embed(
        self,
        text,
    ):
        assert text == "Workflow"

        return [
            0.1,
            0.2,
        ]


class FakeSearchTool:
    """模拟 Qdrant Search Tool。"""

    async def execute(
        self,
        *,
        query_vector,
        limit,
    ):
        assert query_vector == [
            0.1,
            0.2,
        ]

        assert limit == 3

        return [
            {
                "text": "workflow.py",
                "source": "code",
            }
        ]


@pytest.mark.asyncio
async def test_qdrant_context_retriever():
    """测试自然语言 → Embedding → Qdrant Tool。"""

    retriever = QdrantContextRetriever(
        FakeEmbedding(),
        FakeSearchTool(),
        limit=3,
    )

    result = await retriever(
        "Workflow"
    )

    assert result == [
        {
            "text": "workflow.py",
            "source": "code",
        }
    ]