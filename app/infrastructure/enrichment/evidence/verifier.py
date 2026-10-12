"""
Evidence Verification。

负责验证 Evidence / Claim 的状态。
"""

from app.infrastructure.enrichment.evidence.store import (
    EvidenceStore,
)


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

        self.session = session

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

        evidence.verification_status = (
            self.validate_status(status)
        )

        await self.session.flush()

        return evidence

    async def verify_claim(
        self,
        claim,
        status: str,
    ):

        claim.verification_status = (
            self.validate_status(status)
        )

        await self.session.flush()

        return claim
