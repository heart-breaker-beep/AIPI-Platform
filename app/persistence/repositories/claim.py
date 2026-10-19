"""
Claim 数据访问层。
"""


from sqlalchemy import select

from app.persistence.models.claim import Claim
from app.persistence.repositories.base import BaseRepository


class ClaimRepository(BaseRepository[Claim]):
    """
    Claim 表的数据访问对象。
    """

    model = Claim

    async def update_verification_status(self, claim: Claim, status: str) -> Claim:
        claim.verification_status = status
        await self.session.flush()
        return claim

    async def create(
        self,
        *,
        claim_id: str,
        run_id: str,
        claim_text: str,
        verification_status: str = "UNVERIFIED",
    ) -> Claim:

        return await super().create(
            id=claim_id,
            run_id=run_id,
            claim_text=claim_text,
            verification_status=verification_status,
        )

    async def list_by_run(
        self,
        run_id: str,
    ) -> list[Claim]:

        result = await self.session.execute(
            select(Claim)
            .where(
                Claim.run_id == run_id
            )
            .order_by(Claim.created_at)
        )

        return list(result.scalars().all())
