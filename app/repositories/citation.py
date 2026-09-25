"""
Citation 数据访问层。
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.citation import Citation


class CitationRepository:
    """
    Citation 表的数据访问对象。
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

    async def create(
        self,
        *,
        citation_id: str,
        claim_id: str,
        evidence_id: str,
    ) -> Citation:

        citation = Citation(
            id=citation_id,
            claim_id=claim_id,
            evidence_id=evidence_id,
        )

        self.session.add(citation)

        await self.session.flush()

        return citation

    async def get_by_id(
        self,
        citation_id: str,
    ) -> Citation | None:

        result = await self.session.execute(
            select(Citation).where(
                Citation.id == citation_id
            )
        )

        return result.scalar_one_or_none()

    async def get_by_claim(
        self,
        claim_id: str,
    ) -> list[Citation]:

        result = await self.session.execute(
            select(Citation)
            .where(
                Citation.claim_id == claim_id
            )
            .order_by(Citation.created_at)
        )

        return list(result.scalars().all())

    async def exists(
        self,
        *,
        claim_id: str,
        evidence_id: str,
    ) -> bool:

        result = await self.session.execute(
            select(Citation.id).where(
                Citation.claim_id == claim_id,
                Citation.evidence_id == evidence_id,
            )
        )

        return result.scalar_one_or_none() is not None