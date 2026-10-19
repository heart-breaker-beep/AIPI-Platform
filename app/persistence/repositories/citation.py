"""
Citation 数据访问层。
"""


from sqlalchemy import select

from app.persistence.models.citation import Citation
from app.persistence.repositories.base import BaseRepository


class CitationRepository(BaseRepository[Citation]):
    """
    Citation 表的数据访问对象。
    """

    model = Citation

    async def create(
        self,
        *,
        citation_id: str,
        claim_id: str,
        evidence_id: str,
    ) -> Citation:

        return await super().create(
            id=citation_id,
            claim_id=claim_id,
            evidence_id=evidence_id,
        )

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
