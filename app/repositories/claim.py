"""
Claim 数据访问层。
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.claim import Claim


class ClaimRepository:
    """
    Claim 表的数据访问对象。
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

    async def create(
        self,
        *,
        claim_id: str,
        run_id: str,
        claim_text: str,
        verification_status: str = "UNVERIFIED",
    ) -> Claim:

        claim = Claim(
            id=claim_id,
            run_id=run_id,
            claim_text=claim_text,
            verification_status=verification_status,
        )

        self.session.add(claim)

        await self.session.flush()

        return claim

    async def get_by_id(
        self,
        claim_id: str,
    ) -> Claim | None:

        result = await self.session.execute(
            select(Claim).where(
                Claim.id == claim_id
            )
        )

        return result.scalar_one_or_none()

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