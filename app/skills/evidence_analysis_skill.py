"""
Evidence Analysis Skill。

Phase 9：

Qdrant Retrieval
        ↓
Evidence Normalization
        ↓
Evidence Store

负责：

- 检索候选证据
- 标准化 Evidence
- 保存 Evidence
- 保留 Source / File / Line 信息
"""

from app.skills.base import BaseSkill


class EvidenceAnalysisSkill(
    BaseSkill
):

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

        # 获取 Qdrant 检索工具
        qdrant_tool = context.tools[
            "qdrant_search"
        ]

        # 执行语义检索
        results = await qdrant_tool.execute(
            **input_data
        )

        evidence = []

        for item in results:

            # 当前 Qdrant payload 中：
            #
            # text
            # source
            # document_id
            # chunk_index
            #
            # 可能存在，但不能假设一定存在。

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
                    ""
                ),
                "metadata": item,
            }

            # 不伪造源码行号。
            #
            # 当前索引器没有可靠保存
            # line_start / line_end，
            # 所以没有数据时保持 None。

            evidence.append(
                normalized
            )

        return {
            "evidence": evidence,
            "count": len(evidence),
        }