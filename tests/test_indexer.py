"""DocumentIndexer 集成测试。"""

from app.project_analysis.project_indexer import DocumentIndexer


def test_document_indexer():
    """测试文档是否能够完成 Chunk、Embedding 和 Qdrant 写入。"""

    indexer = DocumentIndexer(
        collection_name="aipi_indexer_test",
    )

    document = """# Introduction

This is an AI Agent platform.

# HITL

Human approval is required for sensitive operations.

# Workflow

The system supports workflow execution and task recovery.
"""

    chunk_count = indexer.index_document(
        document_id="test-repository-readme",
        text=document,
        metadata={
            "repository_id": 1,
            "repository_url": "https://github.com/example/project",
            "source": "README.md",
        },
    )

    assert chunk_count == 3