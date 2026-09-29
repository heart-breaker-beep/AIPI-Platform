"""
File Reader Tool。

负责:

    - 读取 GitHub 项目文件内容

读取策略
========

优先 GitHub Contents API
（api.github.com/repos/{owner}/{name}/contents/{path}）

失败时回退
（raw.githubusercontent.com）

原因：

部分网络环境下 raw.githubusercontent.com 极不稳定，
实测同一个 README：

    api.github.com/contents   -> 200，0.88 秒
    raw.githubusercontent.com -> 20 秒后 ReadError

而一个文件读取失败曾经导致
整个 5-Agent 分析计划直接 FAILED。

因此把稳定的域名放在前面，
raw 只作为回退（它支持 >1MB 的大文件，
Contents API 对超过 1MB 的文件不返回内容）。
"""


import base64
import httpx

from app.core.config import get_settings
from app.core.exceptions import ToolError
from app.tools.base import BaseTool



class FileReaderTool(BaseTool):


    """
    GitHub 文件读取工具。
    """


    name = "file_reader"


    # 单次读取超时（秒）。
    TIMEOUT_SECONDS = 30


    API_BASE = "https://api.github.com"


    RAW_BASE = (
        "https://raw.githubusercontent.com"
    )


    # 内部标记：
    # Contents API 无法提供内容
    # （网络出错 / 目录 / 超过 1MB），
    # 但「文件不存在」不属于这种情况。
    _USE_FALLBACK = object()


    @staticmethod
    def _headers() -> dict:
        """GitHub 请求头（配置了 token 就带上）。"""

        headers = {
            "Accept": (
                "application/vnd.github+json"
            ),
        }

        token = get_settings().GITHUB_TOKEN

        if token:

            headers["Authorization"] = (
                f"Bearer {token}"
            )

        return headers


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
        """
        读取文件内容。

        返回空字符串表示「文件不存在」
        （非 200 / 404），保持既有语义。

        回退策略是「按分支决策」而不是
        「按来源整体回退」：

            Contents API 明确回答 404
                → 该分支上文件确实不存在
                → 不再去 raw 白等几十秒超时

            Contents API 网络出错 / 文件超过 1MB
                → 该分支回退 raw

        否则一个不存在的文件要等
        两个 raw 超时（实测 51 秒）。
        """

        branches = [branch]

        # main 不存在时尝试 master
        if branch == "main":

            branches.append("master")

        errors = []

        completed = 0

        for candidate in branches:

            try:

                result = (
                    await self._read_via_contents_api(
                        owner,
                        name,
                        file_path,
                        candidate,
                    )
                )

            except ToolError as error:

                errors.append(str(error))

                result = self._USE_FALLBACK

            else:

                completed += 1

            if isinstance(result, str):

                return result

            # 文件确实不存在（404）：
            # 换下一个分支，不必回退 raw。
            if result is None:

                continue

            # 需要回退 raw：
            # Contents API 出错或缺内容。
            try:

                content = await self._read_via_raw(
                    owner,
                    name,
                    file_path,
                    candidate,
                )

            except ToolError as error:

                errors.append(str(error))

                continue

            completed += 1

            if content is not None:

                return content

        # 所有来源都是网络错误：
        # 抛出以便定位，而不是伪装成「文件不存在」。
        if completed == 0 and errors:

            raise ToolError(errors[0])

        return ""


    async def _read_via_contents_api(
        self,
        owner: str,
        name: str,
        file_path: str,
        branch: str,
    ) -> str | None:
        """
        GitHub Contents API。

        返回值语义（调用方据此决定是否回退 raw）：

            str           读到内容
            None          文件在该分支上不存在
            _USE_FALLBACK 拿不到内容（目录 / >1MB），
                          需要回退 raw
        """

        url = (
            f"{self.API_BASE}"
            f"/repos/{owner}/{name}"
            f"/contents/{file_path}"
        )

        try:

            async with httpx.AsyncClient() as client:

                response = await client.get(
                    url,
                    params={"ref": branch},
                    headers=self._headers(),
                    timeout=self.TIMEOUT_SECONDS,
                )

        except httpx.TimeoutException as error:

            raise ToolError(
                f"Contents API timeout: {url}"
            ) from error

        except httpx.HTTPError as error:

            raise ToolError(
                f"Contents API failed: {url}: {error}"
            ) from error

        if response.status_code != 200:

            return None

        payload = response.json()

        if not isinstance(payload, dict):

            return None

        encoded = payload.get("content")

        if (
            payload.get("encoding") != "base64"
            or not encoded
        ):

            # 目录或超过 1MB 的文件：
            # 这是「该来源拿不到」，
            # 不是「文件不存在」，
            # 因此需要回退 raw。
            return self._USE_FALLBACK

        try:

            return base64.b64decode(
                encoded
            ).decode(
                "utf-8",
                errors="replace",
            )

        except Exception:

            return None


    async def _read_via_raw(
        self,
        owner: str,
        name: str,
        file_path: str,
        branch: str,
    ) -> str | None:
        """
        raw.githubusercontent.com 回退。

        返回 None 表示非 200（文件不存在）。
        """

        url = (
            f"{self.RAW_BASE}/"
            f"{owner}/{name}/"
            f"{branch}/{file_path}"
        )

        try:

            async with httpx.AsyncClient() as client:

                response = await client.get(
                    url,
                    timeout=self.TIMEOUT_SECONDS,
                )

        except httpx.TimeoutException as error:

            raise ToolError(
                f"Read timeout: {url}"
            ) from error

        except httpx.HTTPError as error:

            raise ToolError(
                f"Read failed: {url}: {error}"
            ) from error

        if response.status_code != 200:

            return None

        return response.text
