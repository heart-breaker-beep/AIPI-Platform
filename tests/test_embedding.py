"""Embedding Provider 测试。"""

from app.embeddings.ollama import OllamaEmbedding


def test_ollama_embedding():
    """测试 Ollama 是否可以生成 BGE-M3 向量。"""

    provider = OllamaEmbedding()

    vector = provider.embed(
        "Multi-Agent workflow platform"
    )

    assert isinstance(vector, list)
    assert len(vector) > 0