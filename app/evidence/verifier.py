"""
Evidence Verification。

负责验证 Evidence / Claim 的状态。
"""

from app.core.exceptions import ValidationError
from app.evidence.store import (
    VERIFICATION_STATUSES,
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

        normalized = status.upper()

        if normalized not in VERIFICATION_STATUSES:
            raise ValidationError(
                f"Unsupported verification status: "
                f"{normalized}"
            )

        return normalized

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