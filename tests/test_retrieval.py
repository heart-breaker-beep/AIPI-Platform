"""向量检索测试。"""

from app.embeddings.ollama import OllamaEmbedding
from app.project_analysis.project_indexer import DocumentIndexer
from app.vector_store.qdrant import QdrantVectorStore


def test_semantic_retrieval():
    """测试建立索引后能否通过语义问题找到相关 Chunk。"""

    indexer = DocumentIndexer(
        collection_name="aipi_retrieval_test",
    )

    document = """# Introduction

This is an AI Agent platform.

# HITL

Human approval is required for sensitive operations.

# Workflow

The system supports workflow execution and task recovery.
"""

    indexer.index_document(
        document_id="test-repository-readme",
        text=document,
        metadata={
            "repository_id": 1,
            "source": "README.md",
        },
    )

    embedding = OllamaEmbedding()

    vector_store = QdrantVectorStore(
        collection_name="aipi_retrieval_test",
    )

    query = "Does the system support human approval?"

    query_vector = embedding.embed(query)

    results = vector_store.search(
        query_vector=query_vector,
        limit=3,
    )

    assert len(results) > 0

    print("\nRetrieval Results:")

    for result in results:
        print(
            f"score={result.score}",
            result.payload,
        )

    assert "Human approval" in results[0].payload["text"]
