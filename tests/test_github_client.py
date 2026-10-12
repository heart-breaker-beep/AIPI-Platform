"""GitHub Client 测试。"""

import httpx
import pytest

from app.core.exceptions import (
    RetryableToolError,
    ToolError,
)
from app.infrastructure.tools.github.github_repository_tool import GitHubRepositoryTool


@pytest.mark.asyncio
async def test_get_repository():

    client = GitHubRepositoryTool()

    data = await client.get_repository(
        "langchain-ai",
        "langchain",
    )

    assert data["name"] == "langchain"

    assert (
        data["owner"]["login"]
        ==
        "langchain-ai"
    )


# ----------------------------------------------------------------
# 瞬时故障 → 可重试
#
# 这组测试不出网：GitHub 一旦限流或超时，
# 工具应抛 RetryableToolError，
# 让 Workflow 引擎退避重试，而不是当场判死。
# ----------------------------------------------------------------


class FakeResponse:
    """最小可用的 httpx 响应替身。"""

    def __init__(
        self,
        status_code,
        payload=None,
    ):

        self.status_code = status_code
        self._payload = payload

    def json(self):

        return self._payload

    def raise_for_status(self):

        if self.status_code >= 400:

            raise httpx.HTTPStatusError(
                f"{self.status_code}",
                request=httpx.Request(
                    "GET",
                    "https://api.github.com",
                ),
                response=httpx.Response(
                    self.status_code
                ),
            )


class FakeAsyncClient:
    """按预设结果返回的假 httpx.AsyncClient。"""

    def __init__(
        self,
        response=None,
        error=None,
    ):

        self.response = response
        self.error = error
        self.calls = []

    async def __aenter__(self):

        return self

    async def __aexit__(
        self,
        *exc_info,
    ):

        return False

    async def get(
        self,
        url,
        params=None,
        headers=None,
        **kwargs,
    ):

        self.calls.append(url)

        if self.error is not None:

            raise self.error

        return self.response


def install_client(
    monkeypatch,
    response=None,
    error=None,
):
    """把假 Client 注入工具使用的 httpx 模块。"""

    client = FakeAsyncClient(
        response=response,
        error=error,
    )

    monkeypatch.setattr(
        httpx,
        "AsyncClient",
        lambda *args, **kwargs: client,
    )

    return client


@pytest.mark.asyncio
async def test_get_repository_timeout_is_retryable(
    monkeypatch,
):
    """超时属于瞬时故障，要能被引擎重试。"""

    install_client(
        monkeypatch,
        error=httpx.ConnectTimeout("slow"),
    )

    with pytest.raises(RetryableToolError):

        await GitHubRepositoryTool().get_repository(
            "demo",
            "proj",
        )


@pytest.mark.asyncio
async def test_get_repository_429_is_retryable(
    monkeypatch,
):
    """429 限流同样可重试。"""

    install_client(
        monkeypatch,
        response=FakeResponse(429),
    )

    with pytest.raises(RetryableToolError):

        await GitHubRepositoryTool().get_repository(
            "demo",
            "proj",
        )


@pytest.mark.asyncio
async def test_retryable_tool_error_is_still_tool_error(
    monkeypatch,
):
    """
    可重试异常必须仍是 ToolError 子类。

    工具层有一批 `except ToolError` 的降级契约
    （拿不到就返回空结果），
    换成新类型也不能把那些调用方漏掉。
    """

    install_client(
        monkeypatch,
        response=FakeResponse(503),
    )

    with pytest.raises(ToolError):

        await GitHubRepositoryTool().get_repository(
            "demo",
            "proj",
        )


@pytest.mark.asyncio
async def test_get_repository_returns_payload(
    monkeypatch,
):
    """正常响应照旧返回 JSON。"""

    install_client(
        monkeypatch,
        response=FakeResponse(
            200,
            {"name": "proj"},
        ),
    )

    data = await GitHubRepositoryTool().get_repository(
        "demo",
        "proj",
    )

    assert data == {"name": "proj"}


@pytest.mark.asyncio
async def test_get_repository_404_stays_http_error(
    monkeypatch,
):
    """
    404 是「东西不存在」，不是瞬时故障。

    不能顺手把它也变成可重试 ——
    重试三次不会让仓库出现，只会浪费预算。
    """

    install_client(
        monkeypatch,
        response=FakeResponse(404),
    )

    with pytest.raises(httpx.HTTPStatusError):

        await GitHubRepositoryTool().get_repository(
            "demo",
            "missing",
        )


@pytest.mark.asyncio
async def test_get_tree_503_is_retryable(
    monkeypatch,
):
    """文件树接口的上游故障同样可重试。"""

    install_client(
        monkeypatch,
        response=FakeResponse(503),
    )

    with pytest.raises(RetryableToolError):

        await GitHubRepositoryTool().get_tree(
            "demo",
            "proj",
        )


@pytest.mark.asyncio
async def test_get_tree_missing_branch_returns_empty(
    monkeypatch,
):
    """分支不存在时仍返回空列表，不抛异常。"""

    install_client(
        monkeypatch,
        response=FakeResponse(404),
    )

    tree = await GitHubRepositoryTool().get_tree(
        "demo",
        "proj",
    )

    assert tree == []
