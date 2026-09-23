"""Qdrant 向量存储层。"""

from typing import Any
import uuid


from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)

from app.core.config import get_settings


class QdrantVectorStore:
    """负责 Collection 管理、向量写入和相似度检索。"""

    def __init__(
            self,
            collection_name: str = "github_projects",
    ) -> None:
        settings = get_settings()

        self.collection_name = collection_name

        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
            trust_env=False,
        )

    def create_collection(
        self,
        vector_size: int,
    ) -> None:
        """创建向量 Collection。"""

        if self.client.collection_exists(
            self.collection_name
        ):
            return

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE,
            ),
        )

    def upsert(
        self,
        point_id: int,
        vector: list[float],
        payload: dict[str, Any],
    ) -> None:
        """向 Collection 写入一个向量及其业务元数据。"""

        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=payload,
                )
            ],
        )

    def search(
        self,
        query_vector: list[float],
        limit: int = 5,
    ):
        """根据查询向量执行 Top-K 相似度搜索。"""

        return self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit,
            with_payload=True,
        ).points

    def insert(
        self,
        vector,
        payload,
    ):

        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload=payload,
        )


        self.client.upsert(
            collection_name=
            self.collection_name,

            points=[
                point
            ],
        )