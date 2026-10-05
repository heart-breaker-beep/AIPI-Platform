"""Qdrant 向量存储层。"""

from typing import Any
import uuid


from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
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
        repository_id: int | None = None,
    ):
        """
        根据查询向量执行 Top-K 相似度搜索。

        repository_id 非空时只在**该仓库**的向量里检索。

        为什么必须能过滤
        ================
        所有仓库共用 `github_projects` 这一个集合。
        不过滤的话，检索会跨仓库返回代码 ——
        分析 A 项目却拿 B 项目的源码当证据，
        而且片段看起来完全合理，无从察觉。
        这比"没有检索结果"更糟，所以过滤不是优化而是正确性要求。
        """

        return self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit,
            with_payload=True,
            query_filter=self._repository_filter(
                repository_id
            ),
        ).points

    @staticmethod
    def _repository_filter(
        repository_id: int | None,
    ) -> Filter | None:
        """构造按仓库过滤的条件；为 None 时不加过滤。"""

        if repository_id is None:
            return None

        return Filter(
            must=[
                FieldCondition(
                    key="repository_id",
                    match=MatchValue(
                        value=repository_id
                    ),
                )
            ]
        )

    def upsert_many(
        self,
        points: list[dict],
    ) -> None:
        """
        批量写入。

        points: [{"id": int, "vector": [...], "payload": {...}}, ...]

        一批一次请求，而不是每个点单独 upsert ——
        索引一个仓库会产生数百个 chunk，
        逐点写入会把大部分时间花在 HTTP 往返上。
        """

        if not points:
            return

        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=item["id"],
                    vector=item["vector"],
                    payload=item["payload"],
                )
                for item in points
            ],
        )

    def delete_by_repository(
        self,
        repository_id: int,
    ) -> None:
        """
        删除某个仓库的全部向量。

        重新索引前先清一次，避免同一文件被改了之后
        新旧两份 chunk 同时留在库里 ——
        那样检索会返回已经不存在的代码。

        集合不存在时直接返回：
        首次索引时它本来就还没建，
        这里抛 404 会把「清理」这个可选动作
        变成整个索引流程的失败原因。
        """

        if not self.client.collection_exists(
            self.collection_name
        ):
            return

        self.client.delete(
            collection_name=self.collection_name,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="repository_id",
                        match=MatchValue(
                            value=repository_id
                        ),
                    )
                ]
            ),
        )

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