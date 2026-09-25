"""
EvidenceAnalysisSkill 测试。
"""

import pytest

from app.skills.evidence_analysis_skill import (
    EvidenceAnalysisSkill,
)


class FakeQdrantTool:

    async def execute(
        self,
        **kwargs,
    ):

        return [
            {
                "text": (
                    "class BaseAgent:"
                ),
                "document_id": (
                    "agent-base"
                ),
                "chunk_index": 0,
                "file_path": (
                    "app/agents/base.py"
                ),
            }
        ]


class FakeContext:

    tools = {
        "qdrant_search":
            FakeQdrantTool()
    }


@pytest.mark.asyncio
async def test_evidence_analysis_skill():

    skill = EvidenceAnalysisSkill()

    result = await skill.execute(
        FakeContext(),
        {
            "query_vector": [
                0.1,
                0.2,
            ],
            "limit": 5,
        },
    )

    assert (
        result["count"]
        == 1
    )

    evidence = (
        result["evidence"][0]
    )

    assert (
        evidence["content"]
        == "class BaseAgent:"
    )

    assert (
        evidence["file_path"]
        == "app/agents/base.py"
    )

    # 当前索引器没有可靠行号，
    # 所以不能伪造。
    assert (
        evidence["line_start"]
        is None
    )

    assert (
        evidence["line_end"]
        is None
    )