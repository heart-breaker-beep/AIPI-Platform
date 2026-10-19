"""
Evidence 数据访问层。
"""


from sqlalchemy import select

from app.persistence.models.evidence import Evidence
from app.persistence.repositories.base import BaseRepository


class EvidenceRepository(BaseRepository[Evidence]):
    """
    Evidence 表的数据访问对象。
    """

    model = Evidence

    async def update_verification_status(self, evidence: Evidence, status: str) -> Evidence:
        evidence.verification_status = status
        await self.session.flush()
        return evidence

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

        return await super().create(
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
