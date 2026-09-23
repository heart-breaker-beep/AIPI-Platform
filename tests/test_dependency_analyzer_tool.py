import pytest

from app.tools.dependency_analyzer_tool import (
    DependencyAnalyzerTool
)



@pytest.mark.asyncio
async def test_dependency_analyzer():


    tool = DependencyAnalyzerTool()


    result = await tool.execute(
        "."
    )


    assert isinstance(
        result,
        dict
    )


    assert (
        "frameworks"
        in result
    )