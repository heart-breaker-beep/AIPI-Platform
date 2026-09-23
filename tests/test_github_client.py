"""GitHub Client 测试。"""

import pytest

from app.tools.github.github_repository_tool import GitHubRepositoryTool


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