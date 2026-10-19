"""Embedding Provider 抽象接口。"""

from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    """定义统一的文本向量化接口。"""

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        """将单段文本转换为向量。"""
        raise NotImplementedError

    @abstractmethod
    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """批量将文本转换为向量。"""
        raise NotImplementedError