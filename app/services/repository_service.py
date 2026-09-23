"""
Repository 业务服务。
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.repository import Repository
from app.repositories.repository import RepositoryRepository

from app.tools.github.github_repository_tool import (
    GitHubRepositoryTool
)
from app.tools.github.parser import (
    parse_github_url
)

class RepositoryService:
    """
    Repository 业务服务。

    负责:
        - Repository 查询
        - Repository 创建
        - GitHub数据同步
    不负责:
        - GitHub API细节
    """
    def __init__(
        self,
        session: AsyncSession,
    ):


        self.repository_repository = (
            RepositoryRepository(session)
        )


        self.github_tool = (
            GitHubRepositoryTool()
        )

    async def get_or_create(
        self,
        url: str,
    ) -> Repository:
        """
        获取 Repository。

        存在:
            返回数据库数据

        不存在:
            GitHub获取信息
            保存数据库
        """
        owner, name = (
            parse_github_url(url)
        )

        repository = await (
            self.repository_repository
            .get_by_url(url)
        )

        if repository:
            return repository



        github_data = await (
            self.github_tool
            .get_repository(
                owner,
                name,
            )
        )

        repository = await (
            self.repository_repository
            .create(

                url=url,

                owner=owner,

                name=name,

                description=
                github_data.get(
                    "description"
                ),

                default_branch=
                github_data.get(
                    "default_branch"
                ),

                language=
                github_data.get(
                    "language"
                ),

                stars=
                github_data.get(
                    "stargazers_count",
                    0,
                ),

                forks=
                github_data.get(
                    "forks_count",
                    0,
                ),
            )
        )
        return repository