"""
Claim → Citation → Evidence 可追溯测试。
"""

import pytest

from app.evidence.traceability import (
    TraceabilityService,
)


class FakeClaim:

    id = "claim-1"

    claim_text = (
        "The project contains multiple agents."
    )


class FakeCitation:

    def __init__(
        self,
        evidence_id,
    ):
        self.evidence_id = evidence_id


class FakeEvidence:

    def __init__(
        self,
        evidence_id,
    ):
        self.id = evidence_id
        self.file_path = (
            "app/agents/base.py"
        )
        self.line_start = 1
        self.line_end = 20
        self.content = (
            "class BaseAgent:"
        )


@pytest.mark.asyncio
async def test_claim_traceability():

    service = TraceabilityService(
        session=None
    )

    async def get_claim(
        claim_id
    ):
        return FakeClaim()

    async def get_citations(
        claim_id
    ):
        return [
            FakeCitation(
                "evidence-1"
            )
        ]

    async def get_evidence(
        evidence_id
    ):
        return FakeEvidence(
            evidence_id
        )

    service.claims.get_by_id = (
        get_claim
    )

    service.citations.get_by_claim = (
        get_citations
    )

    service.evidences.get_by_id = (
        get_evidence
    )

    result = await (
        service.get_claim_trace(
            "claim-1"
        )
    )

    assert (
        result["claim"].id
        == "claim-1"
    )

    assert len(
        result["citations"]
    ) == 1

    assert len(
        result["evidences"]
    ) == 1

    evidence = (
        result["evidences"][0]
    )

    assert (
        evidence.file_path
        == "app/agents/base.py"
    )

    assert (
        evidence.line_start
        == 1
    )

    assert (
        evidence.line_end
        == 20
    )