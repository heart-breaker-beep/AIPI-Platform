"""
EvidenceAnalysisAgent 测试。
"""

import pytest

from app.analysis.agents.generic_skill_agent import (
    GenericSkillAgent,
)


class FakeSkill:

    async def execute(
        self,
        context,
        input_data,
    ):

        return {
            "evidence": [
                {
                    "content":
                        "class BaseAgent:"
                }
            ],
            "count": 1,
        }


class FakeSkillRegistry:

    def get(
        self,
        name,
    ):

        assert (
            name
            == "evidence_analysis"
        )

        return FakeSkill()


class FakeContext:

    tools = {}


@pytest.mark.asyncio
async def test_evidence_analysis_agent():

    agent = GenericSkillAgent(
        FakeSkillRegistry(),
        "evidence_analysis_agent",
        "evidence_analysis",
    )

    result = await agent.execute(
        FakeContext(),
        {},
    )

    assert (
        result["count"]
        == 1
    )

    assert (
        result["evidence"][0]["content"]
        == "class BaseAgent:"
    )