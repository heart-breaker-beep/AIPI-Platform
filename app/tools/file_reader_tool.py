"""
File Reader Tool。

负责:
    - 从 GitHub raw 地址读取项目文件
"""


import httpx

from app.core.exceptions import ToolError
from app.tools.base import BaseTool



class FileReaderTool(BaseTool):


    """
    GitHub 文件读取工具。
    当前支持:
        - README.md
    后续可以扩展:
        - .py
        - requirements.txt
        - pyproject.toml
    """


    name = "file_reader"


    async def execute(
        self,
        owner: str,
        name: str,
        file_path: str = "README.md",
        branch: str = "main",
    ) -> str:


        return await self.read_file(
            owner,
            name,
            file_path,
            branch,
        )

    async def read_file(
        self,
        owner: str,
        name: str,
        file_path: str,
        branch: str = "main",
    ) -> str:


        url = (
            "https://raw.githubusercontent.com/"
            f"{owner}/{name}/"
            f"{branch}/{file_path}"
        )

        # httpx 的超时异常（例如 ReadTimeout）
        # 其 str() 可能是空字符串，
        # 直接向上抛出会丢失 URL 和异常语义，
        # 因此统一转换成带上下文的 ToolError。
        try:

            async with httpx.AsyncClient() as client:

                response = await client.get(
                    url,
                    timeout=10,
                )

        except httpx.TimeoutException as error:

            raise ToolError(
                f"Read timeout: {url}"
            ) from error

        except httpx.HTTPError as error:

            raise ToolError(
                f"Read failed: {url}: {error}"
            ) from error

        # 非 200 视为“文件不存在”，
        # 保持原有语义：不抛异常。
        if response.status_code != 200:

            # main不存在时尝试master

            if branch == "main":

                return await self.read_file(
                    owner,
                    name,
                    file_path,
                    "master",
                )

            return ""

        return response.text