"""
GitHub Repository Tool。
"""

import httpx
from app.tools.base import BaseTool

class GitHubRepositoryTool(BaseTool):

    """
    GitHub Repository 查询工具。

    负责:
        - 调用 GitHub REST API
        - 获取仓库基础信息
    """

    name = "github_repository"

    BASE_URL = "https://api.github.com"

    async def execute(
        self,
        owner: str,
        name: str,
    ) -> dict:
        """
        Tool统一入口。

        Agent调用:
            github_repository(owner, name)
        """
        return await self.get_repository(
            owner,
            name,
        )
    async def get_repository(
        self,
        owner: str,
        name: str,
    ) -> dict:

        url = (
            f"{self.BASE_URL}"
            f"/repos/{owner}/{name}"
        )
        async with httpx.AsyncClient() as client:

            response = await client.get(
                url
            )
            response.raise_for_status()
            return response.json()