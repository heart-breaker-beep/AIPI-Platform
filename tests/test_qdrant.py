"""Qdrant 向量存储测试。"""

from app.vector_store.qdrant import QdrantVectorStore


def test_qdrant_vector_search():
    """测试 Collection 创建、向量写入和相似度搜索。"""

    store = QdrantVectorStore(
        collection_name="aipi_test",
    )

    store.create_collection(
        vector_size=3,
    )

    store.upsert(
        point_id=1,
        vector=[1.0, 0.0, 0.0],
        payload={
            "repo": "project-a",
            "text": "Multi-Agent workflow platform",
        },
    )

    store.upsert(
        point_id=2,
        vector=[0.0, 1.0, 0.0],
        payload={
            "repo": "project-b",
            "text": "FastAPI backend service",
        },
    )

    store.upsert(
        point_id=3,
        vector=[0.9, 0.1, 0.0],
        payload={
            "repo": "project-c",
            "text": "Agent workflow engine",
        },
    )

    results = store.search(
        query_vector=[1.0, 0.0, 0.0],
        limit=2,
    )

    assert len(results) == 2
    assert results[0].payload["repo"] == "project-a"
