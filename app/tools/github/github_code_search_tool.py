"""
GitHub Code Search Tool。

负责:
    - 搜索 GitHub 项目源码
    - 查找关键代码位置
"""


import httpx


from app.core.config import get_settings
from app.tools.base import BaseTool

class GitHubCodeSearchTool(BaseTool):


    """
    GitHub源码搜索工具。
    """

    name = "github_code_search"
    BASE_URL = "https://api.github.com"



    async def execute(
        self,
        keyword: str,
        repo: str,
    ) -> list:


        """
        Tool统一入口。
        Args:

            keyword:
                搜索关键词

            repo:
                owner/name
        Example:

            langgraph

            openai/openai-python

        """
        return await self.search_code(
            keyword,
            repo,
        )

    async def search_code(
        self,
        keyword: str,
        repo: str,
    ) -> list:

        """
        调用GitHub Code Search API。
        """

        url = (
            f"{self.BASE_URL}"
            "/search/code"
        )

        params = {

            "q":
            f"{keyword}+repo:{repo}"

        }

        headers = {
            "Accept":
            "application/vnd.github+json"
        }

        # GitHub Code Search API 必须认证，
        # 未配置 token 时会返回 401。
        token = get_settings().GITHUB_TOKEN

        if token:

            headers["Authorization"] = (
                f"Bearer {token}"
            )

        async with httpx.AsyncClient() as client:


            response = await client.get(
                url,
                params=params,
                headers=headers
            )


            response.raise_for_status()


            data = response.json()


            return data.get(
                "items",
                []
            )