"""
Evidence Verification。

负责验证 Evidence / Claim 的状态。
"""

from app.analysis.evidence.store import (
    EvidenceStore,
)
from app.persistence.repositories.claim import ClaimRepository
from app.persistence.repositories.evidence import EvidenceRepository


class EvidenceVerifier:
    """
    Evidence / Claim 验证器。

    状态：

    VERIFIED
    UNVERIFIED
    CONFLICT
    """

    def __init__(
        self,
        session,
    ) -> None:

        self.evidence_repository = EvidenceRepository(session)
        self.claim_repository = ClaimRepository(session)

    @staticmethod
    def validate_status(
        status: str,
    ) -> str:
        """
        校验并规范化状态。

        实现只有一份（EvidenceStore.validate_status）：
        两处同名校验并存时，
        改了一处、忘了另一处，就会出现
        「store 拒收、verifier 放行」这种不一致。
        """

        return EvidenceStore.validate_status(status)

    async def verify_evidence(
        self,
        evidence,
        status: str,
    ):

        return await self.evidence_repository.update_verification_status(
            evidence, self.validate_status(status)
        )

    async def verify_claim(
        self,
        claim,
        status: str,
    ):

        return await self.claim_repository.update_verification_status(
            claim, self.validate_status(status)
        )
