"""
FileReaderTool 测试。

读取策略（Phase 12 网络稳定性修复）：

    1. 优先 GitHub Contents API
       api.github.com/repos/{owner}/{name}/contents/{path}
    2. 失败时回退 raw.githubusercontent.com

原因：部分网络环境下 raw.githubusercontent.com
极不稳定（实测同一 README：
Contents API 0.88 秒成功、raw 20 秒后 ReadError），
而一个文件读取失败曾导致整个 5-Agent 计划 FAILED。

本文件覆盖：

1. Contents API 优先，成功时完全不碰 raw
2. Contents API 失败时回退 raw
3. 大文件（encoding != base64）回退 raw
4. 文件确实不存在时不浪费 raw 超时
5. 所有来源网络错误时抛 ToolError
6. main → master 分支回退
"""

import base64

import httpx
import pytest

from app.core.exceptions import ToolError
from app.tools.file_reader_tool import (
    FileReaderTool,
)


EXPECTED_MAIN = (
    "https://api.github.com/repos/openai/"
    "openai-python/contents/requirements.txt"
)

EXPECTED_MAIN_RAW = (
    "https://raw.githubusercontent.com/openai/"
    "openai-python/main/requirements.txt"
)


class FakeResponse:
    """最小可用的 httpx Response 替身。"""

    def __init__(
        self,
        status_code,
        text="",
        payload=None,
    ):

        self.status_code = status_code

        self.text = text

        self._payload = payload

    def json(self):

        if self._payload is None:
            raise ValueError("no json body")

        return self._payload


def contents_payload(text):
    """构造 Contents API 的 base64 响应体。"""

    return {
        "encoding": "base64",
        "content": base64.b64encode(
            text.encode("utf-8")
        ).decode("ascii"),
    }


class FakeAsyncClient:
    """
    按来源分派的假 httpx.AsyncClient。

    api / raw 都是 {branch: FakeResponse}。
    """

    def __init__(
        self,
        api=None,
        raw=None,
        api_error=None,
        raw_error=None,
    ):

        self.api = api or {}

        self.raw = raw or {}

        self.api_error = api_error

        self.raw_error = raw_error

        self.urls = []

    async def __aenter__(self):

        return self

    async def __aexit__(
        self,
        *exc_info,
    ):

        return False

    @staticmethod
    def _branch_from_url(url):
        """
        从 raw URL 的路径里取分支。

        raw 的 URL 形如
            raw.githubusercontent.com/{owner}/{name}/{branch}/{path}
        分支在路径里，不在 query 参数里。
        """

        tail = url.split(
            "raw.githubusercontent.com/",
            1,
        )[-1]

        parts = tail.split("/")

        if len(parts) > 2:
            return parts[2]

        return None

    async def get(
        self,
        url,
        params=None,
        headers=None,
        timeout=None,
    ):

        is_api = "api.github.com" in url

        if is_api:

            branch = (params or {}).get("ref")

        else:

            branch = self._branch_from_url(url)

        self.urls.append((url, branch))

        if is_api:

            if self.api_error is not None:
                raise self.api_error

            return self.api.get(
                branch,
                FakeResponse(404),
            )

        if self.raw_error is not None:
            raise self.raw_error

        return self.raw.get(
            branch,
            FakeResponse(404),
        )


def install_client(monkeypatch, client):
    """把假 Client 注入 FileReaderTool 使用的 httpx 模块。"""

    monkeypatch.setattr(
        httpx,
        "AsyncClient",
        lambda *args, **kwargs: client,
    )

    return client


def api_urls(client):
    return [
        url
        for url, _ in client.urls
        if "api.github.com" in url
    ]


def raw_urls(client):
    return [
        url
        for url, _ in client.urls
        if "raw.githubusercontent.com" in url
    ]


@pytest.mark.asyncio
async def test_contents_api_is_used_first(monkeypatch):
    """
    Contents API 成功时完全不请求 raw。

    这是网络稳定性的关键：
    raw.githubusercontent.com 不稳定时，
    读取不应该再受影响。
    """

    client = install_client(
        monkeypatch,
        FakeAsyncClient(
            api={
                "main": FakeResponse(
                    200,
                    payload=contents_payload(
                        "fastapi==0.1.0"
                    ),
                )
            }
        ),
    )

    result = await FileReaderTool().execute(
        owner="openai",
        name="openai-python",
        file_path="requirements.txt",
    )

    assert result == "fastapi==0.1.0"

    assert api_urls(client) == [EXPECTED_MAIN]

    # 关键断言：完全没有碰 raw
    assert raw_urls(client) == []


@pytest.mark.asyncio
async def test_falls_back_to_raw_when_api_fails(
    monkeypatch,
):
    """Contents API 网络出错时回退 raw。"""

    client = install_client(
        monkeypatch,
        FakeAsyncClient(
            raw={
                "main": FakeResponse(
                    200,
                    "fastapi==0.1.0",
                )
            },
            api_error=httpx.ReadTimeout(""),
        ),
    )

    result = await FileReaderTool().execute(
        owner="openai",
        name="openai-python",
        file_path="requirements.txt",
    )

    assert result == "fastapi==0.1.0"

    assert raw_urls(client) == [EXPECTED_MAIN_RAW]


@pytest.mark.asyncio
async def test_oversized_file_falls_back_to_raw(
    monkeypatch,
):
    """
    超过 1MB 的文件 Contents API 不返回内容
    （encoding != base64），此时回退 raw。
    """

    client = install_client(
        monkeypatch,
        FakeAsyncClient(
            api={
                "main": FakeResponse(
                    200,
                    payload={
                        "encoding": "none",
                        "content": "",
                        "size": 5_000_000,
                    },
                )
            },
            raw={
                "main": FakeResponse(
                    200,
                    "big file",
                )
            },
        ),
    )

    result = await FileReaderTool().execute(
        owner="openai",
        name="openai-python",
        file_path="requirements.txt",
    )

    assert result == "big file"

    assert raw_urls(client) == [EXPECTED_MAIN_RAW]


@pytest.mark.asyncio
async def test_missing_file_does_not_waste_raw_timeout(
    monkeypatch,
):
    """
    文件确实不存在时，不再去 raw 白等超时。

    修复前：Contents API 404 后仍尝试 raw，
    main + master 两个超时合计 51 秒。
    """

    client = install_client(
        monkeypatch,
        FakeAsyncClient(),
    )

    result = await FileReaderTool().execute(
        owner="openai",
        name="openai-python",
        file_path="requirements.txt",
    )

    assert result == ""

    # 两个分支都问过 Contents API
    assert len(api_urls(client)) == 2

    # 但一次 raw 都没请求
    assert raw_urls(client) == []


@pytest.mark.asyncio
async def test_all_sources_network_error_raises(
    monkeypatch,
):
    """所有来源都是网络错误时抛 ToolError，而不是伪装成文件不存在。"""

    install_client(
        monkeypatch,
        FakeAsyncClient(
            api_error=httpx.ReadTimeout(""),
            raw_error=httpx.ReadTimeout(""),
        ),
    )

    with pytest.raises(ToolError) as excinfo:

        await FileReaderTool().execute(
            owner="openai",
            name="openai-python",
            file_path="requirements.txt",
        )

    message = str(excinfo.value)

    assert "timeout" in message.lower()

    assert "openai-python" in message


@pytest.mark.asyncio
async def test_branch_fallback_main_to_master(
    monkeypatch,
):
    """main 没有该文件时回退 master。"""

    client = install_client(
        monkeypatch,
        FakeAsyncClient(
            api={
                "master": FakeResponse(
                    200,
                    payload=contents_payload(
                        "old-style"
                    ),
                )
            }
        ),
    )

    result = await FileReaderTool().execute(
        owner="openai",
        name="openai-python",
        file_path="requirements.txt",
    )

    assert result == "old-style"

    assert [
        branch for _, branch in client.urls
    ] == ["main", "master"]


@pytest.mark.asyncio
async def test_non_main_branch_does_not_fallback(
    monkeypatch,
):
    """显式指定 master 时不再回退。"""

    client = install_client(
        monkeypatch,
        FakeAsyncClient(),
    )

    result = await FileReaderTool().execute(
        owner="openai",
        name="openai-python",
        file_path="requirements.txt",
        branch="master",
    )

    assert result == ""

    assert [
        branch for _, branch in client.urls
    ] == ["master"]
