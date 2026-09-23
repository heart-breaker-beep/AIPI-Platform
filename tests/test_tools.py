import pytest

from app.tools.github.github_repository_tool import (
    GitHubRepositoryTool
)


from app.tools.file_reader_tool import (
    FileReaderTool
)



@pytest.mark.asyncio
async def test_github_repository_tool():

    tool = GitHubRepositoryTool()


    result = await tool.execute(
        owner="openai",
        name="openai-python"
    )


    assert result is not None



@pytest.mark.asyncio
async def test_file_reader_tool():

    tool = FileReaderTool()


    result = await tool.execute(
        owner="openai",
        name="openai-python",
        file_path="README.md"
    )


    assert isinstance(
        result,
        str
    )