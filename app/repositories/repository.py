"""Repository 数据访问层。"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.repository import Repository


class RepositoryRepository:
    """负责 repositories 表的数据库操作。"""

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

    async def get_by_id(
        self,
        repository_id: int,
    ) -> Repository | None:
        """根据 Repository ID 查询项目。"""

        result = await self.session.execute(
            select(Repository).where(
                Repository.id == repository_id
            )
        )

        return result.scalar_one_or_none()

    async def create(
        self,
        *,
        url: str,
        owner: str,
        name: str,
        description: str | None = None,
        default_branch: str | None = None,
        language: str | None = None,
        stars: int = 0,
        forks: int = 0,
    ) -> Repository:
        """创建一个 Repository 记录。"""

        repository = Repository(
            url=url,
            owner=owner,
            name=name,
            description=description,
            default_branch=default_branch,
            language=language,
            stars=stars,
            forks=forks,
        )

        self.session.add(repository)

        await self.session.commit()
        await self.session.refresh(repository)

        return repository