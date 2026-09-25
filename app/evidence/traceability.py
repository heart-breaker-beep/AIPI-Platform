"""
Source Traceability。

负责构建：

Claim
 ↓
Citation
 ↓
Evidence
 ↓
Source
 ↓
File
 ↓
Line
"""

from app.core.exceptions import ValidationError
from app.repositories.claim import ClaimRepository
from app.repositories.citation import CitationRepository
from app.repositories.evidence import EvidenceRepository


class TraceabilityService:
    """
    Claim → Evidence 可追溯服务。
    """

    def __init__(
        self,
        session,
    ) -> None:

        self.claims = ClaimRepository(
            session
        )

        self.citations = CitationRepository(
            session
        )

        self.evidences = EvidenceRepository(
            session
        )

    async def get_claim_trace(
        self,
        claim_id: str,
    ) -> dict:

        claim = await self.claims.get_by_id(
            claim_id
        )

        if claim is None:
            raise ValidationError(
                f"Claim not found: {claim_id}"
            )

        citations = await (
            self.citations.get_by_claim(
                claim_id
            )
        )

        evidence_list = []

        for citation in citations:

            evidence = (
                await self.evidences.get_by_id(
                    citation.evidence_id
                )
            )

            if evidence is None:
                continue

            evidence_list.append(
                evidence
            )

        return {
            "claim": claim,
            "citations": citations,
            "evidences": evidence_list,
        }