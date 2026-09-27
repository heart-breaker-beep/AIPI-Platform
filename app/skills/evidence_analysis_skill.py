"""
Evidence Analysis Skill。

负责：

    Query Vector
        ↓
    Qdrant Search
        ↓
    Evidence Normalization
"""

from app.skills.base import BaseSkill


class EvidenceAnalysisSkill(
    BaseSkill
):
    """
    从 Qdrant 检索结果中提取可追踪 Evidence。
    """

    name = "evidence_analysis"

    description = (
        "Extract traceable evidence "
        "from repository search results"
    )

    async def execute(
        self,
        context,
        input_data,
    ):
        qdrant_tool = context.tools.get(
            "qdrant_search"
        )

        if qdrant_tool is None:
            raise RuntimeError(
                "Tool not found: qdrant_search"
            )

        query_vector = input_data.get(
            "query_vector"
        )

        if query_vector is None:
            raise ValueError(
                "Evidence analysis requires "
                "'query_vector'."
            )

        limit = input_data.get(
            "limit",
            5,
        )

        results = await qdrant_tool.execute(
            query_vector=query_vector,
            limit=limit,
        )

        evidence = []

        for item in results:

            normalized = {
                "source_type": item.get(
                    "source_type",
                    "repository",
                ),
                "source_url": item.get(
                    "source_url"
                ),
                "file_path": item.get(
                    "file_path"
                ),
                "line_start": item.get(
                    "line_start"
                ),
                "line_end": item.get(
                    "line_end"
                ),
                "content": item.get(
                    "text",
                    "",
                ),
                "metadata": item,
            }

            evidence.append(
                normalized
            )

        return {
            "evidence": evidence,
            "count": len(evidence),
        }