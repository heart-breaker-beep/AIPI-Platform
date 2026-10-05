"""
向量检索的仓库隔离测试。

需要 Ollama 与 Qdrant 在线；
两者任一不可用时整体跳过，
而不是让测试套件变红 ——
现行 test_indexer / test_retrieval 那几个集成测试
没有这层守卫，服务不在线时会直接失败。

为什么值得单独锁一条
====================

所有仓库共用 `github_projects` 一个集合。
一旦过滤失效，检索会返回**别的仓库**的源码，
而且片段本身完全合理 ——
分析 A 项目、引用 B 项目的代码当证据，
报告里看不出任何异常。
这比"没有检索结果"更危险，所以用测试钉死。
"""

import pytest
from qdrant_client import QdrantClient

from app.core.config import get_settings
from app.vector_store.qdrant import QdrantVectorStore


def _services_available() -> bool:
    """Ollama 与 Qdrant 是否都能连上。"""

    settings = get_settings()

    try:
        client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
            timeout=3,
            trust_env=False,
        )
        client.get_collections()
    except Exception:  # noqa: BLE001
        return False

    try:
        from ollama import Client

        Client(
            host=settings.OLLAMA_BASE_URL,
            trust_env=False,
        ).list()
    except Exception:  # noqa: BLE001
        return False

    return True


pytestmark = pytest.mark.skipif(
    not _services_available(),
    reason="需要 Ollama 与 Qdrant 在线",
)


COLLECTION = "aipi_isolation_test"

REPO_A_CODE = """
class AuthMiddleware:
    def verify(self, token):
        return token == self.secret
"""

REPO_B_CODE = """
class PaymentGateway:
    def charge(self, amount):
        return {"charged": amount}
"""


def _fixtures():
    from app.embeddings.ollama import OllamaEmbedding
    from app.project_analysis.code_chunker import (
        PythonCodeChunker,
    )

    return OllamaEmbedding(), PythonCodeChunker()


@pytest.fixture
def store():
    vector_store = QdrantVectorStore(
        collection_name=COLLECTION
    )

    vector_store.create_collection(vector_size=1024)
    vector_store.delete_by_repository(1)
    vector_store.delete_by_repository(2)

    embedding, chunker = _fixtures()

    for repository_id, path, code in [
        (1, "app/auth.py", REPO_A_CODE),
        (2, "app/billing.py", REPO_B_CODE),
    ]:

        chunks = chunker.split(code, path)

        vectors = embedding.embed_batch(
            [chunk["text"] for chunk in chunks]
        )

        vector_store.upsert_many(
            [
                {
                    "id": abs(hash(f"{repository_id}:{path}:{i}"))
                    % (2**63 - 1),
                    "vector": vector,
                    "payload": {
                        "repository_id": repository_id,
                        "source_type": "github",
                        "file_path": path,
                        "line_start": chunk["line_start"],
                        "line_end": chunk["line_end"],
                        "text": chunk["text"],
                    },
                }
                for i, (chunk, vector) in enumerate(
                    zip(chunks, vectors)
                )
            ]
        )

    yield vector_store

    vector_store.delete_by_repository(1)
    vector_store.delete_by_repository(2)


def test_search_does_not_leak_across_repositories(store):
    """检索结果必须只来自指定仓库。"""

    embedding, _ = _fixtures()

    vector = embedding.embed("鉴权校验")

    hits = store.search(
        vector,
        limit=5,
        repository_id=1,
    )

    assert hits, "应当命中"

    assert {
        hit.payload["file_path"] for hit in hits
    } == {"app/auth.py"}


def test_search_without_repository_id_spans_all(store):
    """
    不过滤时会跨仓库 —— 用来证明过滤确实在起作用。

    如果这条也只剩一个仓库，说明压根没写进去两个，
    上一条测试就成了假阳性。
    """

    embedding, _ = _fixtures()

    vector = embedding.embed("校验")

    hits = store.search(vector, limit=20)

    assert len({
        hit.payload["repository_id"] for hit in hits
    }) == 2


def test_retrieval_tool_refuses_without_repository_id(store):
    """缺 repository_id 必须返回空，不能退化成全库检索。"""

    import asyncio

    from app.tools.rag_retrieval_tool import (
        RagRetrievalTool,
    )

    embedding, _ = _fixtures()

    tool = RagRetrievalTool(
        embedding=embedding,
        vector_store=store,
    )

    result = asyncio.run(
        tool.execute(
            question="随便问问",
            dimensions=["agents"],
            repository_id=None,
        )
    )

    assert result == []
