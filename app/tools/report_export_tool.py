"""
Report Export Tool。

负责:
    - 导出分析报告
    - 支持 Markdown / JSON 文件
"""

import json
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

    async def export_json(
        self,
        document: dict,
        filename: str = "report.json",
    ):
        """
        导出结构化报告（JSON）。

        与 markdown 的差别不只是格式：
        markdown 是给人读的排版结果，
        JSON 是给程序消费的结构化数据
        （见 ReportService 的 schema）。

        ensure_ascii=False：
        报告里有大量中文，
        转义成 \\uXXXX 会让文件膨胀一倍且不可读。
        """

        file_path = (
            self.output_dir
            /
            filename
        )

        file_path.write_text(
            json.dumps(
                document,
                ensure_ascii=False,
                indent=2,
                default=str,
            ),
            encoding="utf-8",
        )

        return {
            "path": str(file_path),
            "format": "json",
        }

    async def export(
        self,
        *,
        title: str,
        content: str,
        filename: str,
        document: dict | None = None,
        fmt: str = "markdown",
    ):
        """
        按格式导出。

        fmt=json 时必须提供 document。
        """

        if fmt == "json":

            if not isinstance(document, dict):
                raise ValueError(
                    "JSON export requires a document."
                )

            return await self.export_json(
                document,
                filename,
            )

        return await self.export_markdown(
            title,
            content,
            filename,
        )