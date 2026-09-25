"""Context 语义检索适配器。"""

from typing import Any


class QdrantContextRetriever:
    """
    把现有 Embedding + QdrantSearchTool
    适配成 Context Retriever。

    不修改现有 Tool / Vector Store。
    """

    def __init__(
        self,
        embedding_provider,
        search_tool,
        *,
        limit: int = 5,
    ) -> None:

        self.embedding_provider = (
            embedding_provider
        )

        self.search_tool = search_tool

        self.limit = limit

    async def __call__(
        self,
        query: str,
    ) -> list[dict[str, Any]]:
        """
        将自然语言问题转换为向量，
        然后调用 Qdrant Search Tool。
        """

        query_vector = (
            self.embedding_provider.embed(
                query
            )
        )

        results = await (
            self.search_tool.execute(
                query_vector=query_vector,
                limit=self.limit,
            )
        )

        return [
            (
                result
                if isinstance(
                    result,
                    dict,
                )
                else {
                    "content": result
                }
            )
            for result in results
        ]