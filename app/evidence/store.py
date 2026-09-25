"""
Evidence Store。

负责：

Evidence
Claim
Citation

三类对象的领域级管理。
"""

from app.core.exceptions import ValidationError
from app.repositories.claim import ClaimRepository
from app.repositories.citation import CitationRepository
from app.repositories.evidence import EvidenceRepository


VERIFICATION_STATUSES = {
    "VERIFIED",
    "UNVERIFIED",
    "CONFLICT",
}


class EvidenceStore:
    """
    Evidence 领域存储。

    注意：

    Store 不直接执行 SQL。

    调用链：

        Evidence Store
              ↓
        Repository
              ↓
           SQLAlchemy
              ↓
             MySQL
    """

    def __init__(
        self,
        session,
    ) -> None:

        self.evidence_repository = (
            EvidenceRepository(session)
        )

        self.claim_repository = (
            ClaimRepository(session)
        )

        self.citation_repository = (
            CitationRepository(session)
        )

    @staticmethod
    def validate_status(
        status: str,
    ) -> str:

        normalized = status.upper()

        if normalized not in VERIFICATION_STATUSES:
            raise ValidationError(
                f"Unsupported verification status: "
                f"{normalized}"
            )

        return normalized

    async def create_evidence(
        self,
        *,
        evidence_id: str,
        repository_id: int,
        source_type: str,
        content: str,
        source_url: str | None = None,
        file_path: str | None = None,
        line_start: int | None = None,
        line_end: int | None = None,
        verification_status: str = "UNVERIFIED",
    ):

        if not content.strip():
            raise ValidationError(
                "Evidence content cannot be empty."
            )

        if (
            line_start is not None
            and line_end is not None
            and line_end < line_start
        ):
            raise ValidationError(
                "line_end cannot be smaller "
                "than line_start."
            )

        status = self.validate_status(
            verification_status
        )

        return await self.evidence_repository.create(
            evidence_id=evidence_id,
            repository_id=repository_id,
            source_type=source_type,
            source_url=source_url,
            file_path=file_path,
            line_start=line_start,
            line_end=line_end,
            content=content,
            verification_status=status,
        )

    async def create_claim(
        self,
        *,
        claim_id: str,
        run_id: str,
        claim_text: str,
        verification_status: str = "UNVERIFIED",
    ):

        if not claim_text.strip():
            raise ValidationError(
                "Claim text cannot be empty."
            )

        status = self.validate_status(
            verification_status
        )

        return await self.claim_repository.create(
            claim_id=claim_id,
            run_id=run_id,
            claim_text=claim_text,
            verification_status=status,
        )

    async def create_citation(
        self,
        *,
        citation_id: str,
        claim_id: str,
        evidence_id: str,
    ):

        claim = await self.claim_repository.get_by_id(
            claim_id
        )

        if claim is None:
            raise ValidationError(
                f"Claim not found: {claim_id}"
            )

        evidence = (
            await self.evidence_repository.get_by_id(
                evidence_id
            )
        )

        if evidence is None:
            raise ValidationError(
                f"Evidence not found: {evidence_id}"
            )

        exists = await (
            self.citation_repository.exists(
                claim_id=claim_id,
                evidence_id=evidence_id,
            )
        )

        if exists:
            raise ValidationError(
                "The Claim is already cited "
                "by this Evidence."
            )

        return await self.citation_repository.create(
            citation_id=citation_id,
            claim_id=claim_id,
            evidence_id=evidence_id,
        )