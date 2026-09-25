"""
Evidence Verification 测试。
"""

import pytest

from app.core.exceptions import ValidationError
from app.evidence.verifier import (
    EvidenceVerifier,
)


class FakeSession:

    async def flush(self):
        pass


class FakeEvidence:

    verification_status = "UNVERIFIED"


@pytest.mark.asyncio
async def test_verify_evidence():

    verifier = EvidenceVerifier(
        FakeSession()
    )

    evidence = FakeEvidence()

    result = await verifier.verify_evidence(
        evidence,
        "verified",
    )

    assert (
        result.verification_status
        == "VERIFIED"
    )


@pytest.mark.asyncio
async def test_invalid_status():

    verifier = EvidenceVerifier(
        FakeSession()
    )

    evidence = FakeEvidence()

    with pytest.raises(
        ValidationError
    ):

        await verifier.verify_evidence(
            evidence,
            "invalid",
        )