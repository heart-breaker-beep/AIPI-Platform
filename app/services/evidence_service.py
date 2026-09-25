"""
Evidence 业务服务。

Phase 9：

Service
 ↓
Evidence Store
 ↓
Verifier
 ↓
Traceability
 ↓
Repository
 ↓
MySQL
"""

from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ValidationError
from app.evidence.store import EvidenceStore
from app.evidence.traceability import (
    TraceabilityService,
)
from app.evidence.verifier import EvidenceVerifier


class EvidenceService:
    """
    Evidence 业务服务。

    对上层提供统一接口：

    - create_evidence
    - create_claim
    - cite
    - verify_evidence
    - verify_claim
    - get_claim_traceability
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:

        self.session = session

        self.store = EvidenceStore(
            session
        )

        self.verifier = EvidenceVerifier(
            session
        )

        self.traceability = (
            TraceabilityService(
                session
            )
        )

    async def create_evidence(
        self,
        *,
        repository_id: int,
        source_type: str,
        content: str,
        source_url: str | None = None,
        file_path: str | None = None,
        line_start: int | None = None,
        line_end: int | None = None,
        verification_status: str = "UNVERIFIED",
    ):

        return await self.store.create_evidence(
            evidence_id=str(uuid4()),
            repository_id=repository_id,
            source_type=source_type,
            content=content,
            source_url=source_url,
            file_path=file_path,
            line_start=line_start,
            line_end=line_end,
            verification_status=verification_status,
        )

    async def create_claim(
        self,
        *,
        run_id: str,
        claim_text: str,
        verification_status: str = "UNVERIFIED",
    ):

        return await self.store.create_claim(
            claim_id=str(uuid4()),
            run_id=run_id,
            claim_text=claim_text,
            verification_status=verification_status,
        )

    async def cite(
        self,
        *,
        claim_id: str,
        evidence_id: str,
    ):

        return await self.store.create_citation(
            citation_id=str(uuid4()),
            claim_id=claim_id,
            evidence_id=evidence_id,
        )

    async def verify_evidence(
        self,
        *,
        evidence_id: str,
        status: str,
    ):

        evidence = await (
            self.store.evidence_repository
            .get_by_id(evidence_id)
        )

        if evidence is None:
            raise ValidationError(
                f"Evidence not found: {evidence_id}"
            )

        return await self.verifier.verify_evidence(
            evidence,
            status,
        )

    async def verify_claim(
        self,
        *,
        claim_id: str,
        status: str,
    ):

        claim = await (
            self.store.claim_repository
            .get_by_id(claim_id)
        )

        if claim is None:
            raise ValidationError(
                f"Claim not found: {claim_id}"
            )

        return await self.verifier.verify_claim(
            claim,
            status,
        )

    async def get_claim_traceability(
        self,
        *,
        claim_id: str,
    ):

        return await (
            self.traceability
            .get_claim_trace(claim_id)
        )

    async def commit(self) -> None:
        """
        提交 Phase 9 数据。
        """

        await self.session.commit()