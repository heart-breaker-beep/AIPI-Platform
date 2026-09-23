"""GitHub Repository 数据访问层。"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.repository import Repository


class RepositoryRepository:
    """负责 repositories 表的数据访问。"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_url(
        self,
        url: str,
    ) -> Repository | None:
        """根据 GitHub URL 查询项目。"""

        result = await self.session.execute(
            select(Repository).where(
                Repository.url == url
            )
        )

        return result.scalar_one_or_none()

    async def create(
        self,
        *,
        url: str,
        owner: str,
        name: str,
    ) -> Repository:
        """创建 GitHub Repository 记录。"""

        repository = Repository(
            url=url,
            owner=owner,
            name=name,
        )

        self.session.add(repository)

        await self.session.flush()

        return repository