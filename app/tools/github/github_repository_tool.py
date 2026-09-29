"""
GitHub Repository Tool。
"""

import httpx

from app.core.config import get_settings
from app.core.exceptions import ToolError
from app.tools.base import BaseTool

class GitHubRepositoryTool(BaseTool):

    """
    GitHub Repository 查询工具。

    负责:
        - 调用 GitHub REST API
        - 获取仓库基础信息
        - 获取仓库完整文件树（Git Trees API）
    """

    name = "github_repository"

    BASE_URL = "https://api.github.com"

    def _headers(self) -> dict:
        """构造 GitHub 请求头。

        未认证时的速率限制很低，
        因此配置了 token 就带上。
        """

        headers = {
            "Accept": "application/vnd.github+json",
        }

        token = get_settings().GITHUB_TOKEN

        if token:
            headers["Authorization"] = f"Bearer {token}"

        return headers

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
                url,
                headers=self._headers(),
            )
            response.raise_for_status()
            return response.json()

    async def get_tree(
        self,
        owner: str,
        name: str,
        branch: str = "main",
    ) -> list[dict]:
        """
        获取仓库完整文件树。

        使用 Git Trees API（recursive=1）。

        GitHub Code Search 的 repo: 限定符
        对多数仓库返回 0 条结果，
        因此目录结构必须用 Trees API，
        不能用 Code Search 替代。

        取不到时返回空列表而不是抛异常：
        目录结构属于增强信息，
        不应因此中断整个分析流程。
        """

        for candidate in (
            branch,
            "master",
        ):

            url = (
                f"{self.BASE_URL}"
                f"/repos/{owner}/{name}"
                f"/git/trees/{candidate}"
            )

            try:

                async with httpx.AsyncClient() as client:

                    response = await client.get(
                        url,
                        params={"recursive": "1"},
                        headers=self._headers(),
                    )

            except httpx.TimeoutException as error:

                raise ToolError(
                    f"Tree timeout: {url}"
                ) from error

            except httpx.HTTPError as error:

                raise ToolError(
                    f"Tree failed: {url}: {error}"
                ) from error

            if response.status_code == 200:

                tree = response.json().get(
                    "tree",
                    [],
                )

                if isinstance(tree, list):
                    return tree

        return []