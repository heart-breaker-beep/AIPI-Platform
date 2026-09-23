"""GitHub Code Search Tool 测试。"""

import pytest

from app.tools.github import github_code_search_tool as module
from app.tools.github.github_code_search_tool import (
    GitHubCodeSearchTool
)


class FakeResponse:
    """模拟 httpx 响应。"""

    def raise_for_status(self):
        pass

    def json(self):
        return {
            "items": [
                {"path": "app/workflow/engine.py"}
            ]
        }


class FakeAsyncClient:
    """模拟 httpx.AsyncClient，记录请求参数。"""

    captured = {}

    def __init__(self, *args, **kwargs):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc_info):
        return False

    async def get(self, url, params=None, headers=None):
        FakeAsyncClient.captured = {
            "url": url,
            "params": params,
            "headers": headers,
        }
        return FakeResponse()


class FakeSettings:
    """模拟配置对象。"""

    GITHUB_TOKEN = "fake-token"


@pytest.mark.asyncio
async def test_github_code_search(monkeypatch):
    """测试关键词搜索返回结果。"""

    monkeypatch.setattr(
        module.httpx,
        "AsyncClient",
        FakeAsyncClient,
    )

    tool = GitHubCodeSearchTool()

    result = await tool.execute(
        keyword="StateGraph",
        repo="langchain-ai/langchain",
    )

    assert result[0]["path"] == (
        "app/workflow/engine.py"
    )

    assert FakeAsyncClient.captured["url"].endswith(
        "/search/code"
    )

    assert "repo:langchain-ai/langchain" in (
        FakeAsyncClient.captured["params"]["q"]
    )


@pytest.mark.asyncio
async def test_github_code_search_sends_token(monkeypatch):
    """测试配置了 token 时带上认证头。"""

    monkeypatch.setattr(
        module.httpx,
        "AsyncClient",
        FakeAsyncClient,
    )

    monkeypatch.setattr(
        module,
        "get_settings",
        lambda: FakeSettings(),
    )

    tool = GitHubCodeSearchTool()

    await tool.execute(
        keyword="workflow",
        repo="openai/openai-python",
    )

    assert FakeAsyncClient.captured[
        "headers"
    ]["Authorization"] == "Bearer fake-token"
