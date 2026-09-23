"""
Qdrant Search Tool。

提供 Agent 语义检索能力。
"""


from app.tools.base import BaseTool

from app.vector_store.qdrant import (
    QdrantVectorStore
)

class QdrantSearchTool(BaseTool):

    name = "qdrant_search"

    def __init__(
        self,
        vector_store=None
    ):
        self.vector_store = (
            vector_store
            or QdrantVectorStore()
        )

    async def execute(
        self,
        query_vector: list[float],
        limit: int = 5,
    ):

        return self.search(
            query_vector,
            limit
        )

    def search(
        self,
        query_vector: list[float],
        limit: int = 5,
    ):

        points = (
            self.vector_store.search(
                query_vector,
                limit
            )
        )
        return [

            point.payload

            for point in points

        ]