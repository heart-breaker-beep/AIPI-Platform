"""
RagRetrievalTool 的非联网行为测试。

放在单独的文件里（而不是 test_rag_isolation.py）：
后者的整个模块在 Ollama / Qdrant 不在线时会 skip，
而这里的用例全部使用假客户端，不需要任何服务。
"""

import asyncio

import pytest

from app.infrastructure.tools import (
    rag_retrieval_tool as module,
)
from app.infrastructure.tools.rag_retrieval_tool import (
    RagRetrievalTool,
)


def test_retrieval_runs_sync_clients_in_threads(monkeypatch):
    """
    embedding 与 Qdrant 客户端都是同步库。

    直接在协程里调用会占住事件循环整个检索期间 ——
    6 个维度各一次嵌入 + 一次检索，
    期间同一个 run 的其它 await 全被卡住。
    这里断言两个调用都经过 asyncio.to_thread。
    """

    threaded = []

    class FakeEmbedding:

        def embed(self, text):

            return [0.1, 0.2]

    class FakeStore:

        def search(
            self,
            query_vector,
            limit,
            repository_id,
        ):

            return []

    async def fake_to_thread(func, *args, **kwargs):

        threaded.append(
            getattr(func, "__name__", "?")
        )

        return func(*args, **kwargs)

    monkeypatch.setattr(
        module.asyncio,
        "to_thread",
        fake_to_thread,
    )

    tool = RagRetrievalTool(
        embedding=FakeEmbedding(),
        vector_store=FakeStore(),
    )

    result = asyncio.run(
        tool.execute(
            question="agent 怎么编排",
            dimensions=["agents"],
            repository_id=3,
        )
    )

    assert result == []

    assert "embed" in threaded

    assert "search" in threaded


@pytest.mark.asyncio
async def test_retrieval_returns_empty_without_repository_id():
    """缺 repository_id 时必须返回空，不能退化成全库检索。"""

    class FakeEmbedding:

        def embed(self, text):

            raise AssertionError(
                "不该在没有 repository_id 时检索"
            )

    tool = RagRetrievalTool(
        embedding=FakeEmbedding(),
        vector_store=object(),
    )

    assert (
        await tool.execute(
            question="随便问问",
            dimensions=["agents"],
            repository_id=None,
        )
        == []
    )
