"""基于 Ollama 的本地 Embedding Provider。"""

from ollama import Client

from app.core.config import get_settings
from app.embeddings.base import EmbeddingProvider


class OllamaEmbedding(EmbeddingProvider):
    """使用 Ollama 本地模型生成文本向量。"""

    def __init__(
        self,
        model: str | None = None,
    ) -> None:
        settings = get_settings()

        self.model = model or settings.EMBEDDING_MODEL

        self.client = Client(
            host=settings.OLLAMA_BASE_URL,
            trust_env=False,
        )

    def embed(self, text: str) -> list[float]:
        """将单段文本转换为 Embedding 向量。"""

        response = self.client.embed(
            model=self.model,
            input=text,
        )

        return response["embeddings"][0]

    def embed_batch(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """批量生成 Embedding 向量。"""

        response = self.client.embed(
            model=self.model,
            input=texts,
        )

        return response["embeddings"]