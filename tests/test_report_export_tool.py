import pytest

from app.tools.report_export_tool import (
    ReportExportTool
)

@pytest.mark.asyncio
async def test_report_export():

    tool = ReportExportTool(
        "test_reports"
    )
    result = await tool.execute(
        title="Test Report",
        content="hello agent",
        filename="test.md"
    )

    assert (
        result["format"]
        ==
        "markdown"
    )