"""
Report Export Tool。

负责:
    - 导出分析报告
    - 支持 Markdown 文件
"""

from pathlib import Path

from app.tools.base import BaseTool

class ReportExportTool(BaseTool):

    name = "report_export"

    def __init__(
        self,
        output_dir: str = "reports"
    ):

        self.output_dir = Path(
            output_dir
        )

        self.output_dir.mkdir(
            exist_ok=True
        )

    async def execute(
        self,
        title: str,
        content: str,
        filename: str = "report.md",
    ):

        return await self.export_markdown(
            title,
            content,
            filename,
        )

    async def export_markdown(
        self,
        title: str,
        content: str,
        filename: str,
    ):

        file_path = (
            self.output_dir
            /
            filename
        )

        markdown = (
            f"# {title}\n\n"
            f"{content}"
        )

        file_path.write_text(
            markdown,
            encoding="utf-8"
        )

        return {

            "path":
            str(file_path),

            "format":
            "markdown"

        }