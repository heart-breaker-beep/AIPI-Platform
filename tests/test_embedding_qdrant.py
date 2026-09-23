"""Embedding 与 Qdrant 集成测试。"""

from app.embeddings.ollama import OllamaEmbedding
from app.vector_store.qdrant import QdrantVectorStore


def test_embedding_to_qdrant():
    """测试文本向量化后写入 Qdrant，并执行语义检索。"""

    embedding = OllamaEmbedding()

    vector_store = QdrantVectorStore(
        collection_name="github_projects",
    )

    vector_store.create_collection(
        vector_size=1024,
    )

    documents = [
        {
            "id": 1,
            "text": "Multi-Agent workflow orchestration platform",
            "repo": "project-agents-workflow",
        },
        {
            "id": 2,
            "text": "FastAPI backend service for REST APIs",
            "repo": "project-fastapi",
        },
        {
            "id": 3,
            "text": "RAG knowledge retrieval system with vector database",
            "repo": "project-rag",
        },
    ]

    for document in documents:
        vector = embedding.embed(
            document["text"],
        )

        vector_store.upsert(
            point_id=document["id"],
            vector=vector,
            payload={
                "repo": document["repo"],
                "text": document["text"],
            },
        )

    query = "AI Agent workflow system"

    query_vector = embedding.embed(query)

    results = vector_store.search(
        query_vector=query_vector,
        limit=3,
    )

    assert len(results) == 3

    print("\nSemantic Search Results:")

    for result in results:
        print(
            result.score,
            result.payload,
        )