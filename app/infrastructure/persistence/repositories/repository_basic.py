"""
GitHub Repository 数据访问层。

Repository 层只负责：

- 查询
- 创建
- Flush

事务提交由上层 Service 控制。
"""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.persistence.models.repository import Repository
from app.infrastructure.persistence.repositories.base import BaseRepository


class RepositoryRepository(BaseRepository[Repository]):
    """
    repositories 表的数据访问对象。

    事务边界：

        Service
          ↓
        Repository
          ↓
        SQLAlchemy

    Repository 本身不负责 commit。
    """

    model = Repository

    async def get_by_url(
        self,
        url: str,
    ) -> Optional[Repository]:
        """
        根据 GitHub URL 查询 Repository。
        """

        result = await self.session.execute(
            select(Repository).where(
                Repository.url == url
            )
        )

        return result.scalar_one_or_none()

    async def get_by_id(
        self,
        repository_id: int,
    ) -> Optional[Repository]:
        """
        根据 Repository ID 查询 Repository。
        """
        return await super().get_by_id(repository_id)

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
        """
        创建 Repository。

        注意：

        这里使用 flush() 而不是 commit()。

        最终事务由 Service 统一提交。
        """

        return await super().create(
            url=url,
            owner=owner,
            name=name,
            description=description,
            default_branch=default_branch,
            language=language,
            stars=stars,
            forks=forks,
        )