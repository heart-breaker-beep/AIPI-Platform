"""
Evidence 数据访问层。
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.evidence import Evidence


class EvidenceRepository:
    """
    Evidence 表的数据访问对象。
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

    async def create(
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
    ) -> Evidence:

        evidence = Evidence(
            id=evidence_id,
            repository_id=repository_id,
            source_type=source_type,
            source_url=source_url,
            file_path=file_path,
            line_start=line_start,
            line_end=line_end,
            content=content,
            verification_status=verification_status,
        )

        self.session.add(evidence)

        await self.session.flush()

        return evidence

    async def get_by_id(
        self,
        evidence_id: str,
    ) -> Evidence | None:

        result = await self.session.execute(
            select(Evidence).where(
                Evidence.id == evidence_id
            )
        )

        return result.scalar_one_or_none()

    async def list_by_repository(
        self,
        repository_id: int,
    ) -> list[Evidence]:

        result = await self.session.execute(
            select(Evidence)
            .where(
                Evidence.repository_id == repository_id
            )
            .order_by(Evidence.created_at)
        )

        return list(result.scalars().all())