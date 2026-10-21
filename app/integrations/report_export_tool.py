"""
Report Export Tool。

负责:
    - 导出分析报告
    - 支持 Markdown / JSON 文件
"""

import asyncio
import json
from pathlib import Path

from app.core.trace import traced
from app.integrations.base import BaseTool


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

    @traced("tool")
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

        # 写盘是阻塞调用：报告可能有几百 KB，
        # 在协程里直接写会卡住事件循环。丢到线程里。
        await asyncio.to_thread(
            file_path.write_text,
            markdown,
            encoding="utf-8",
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

        # 大文档的 json.dumps 同样是 CPU/IO 混合的阻塞操作，
        # 一起放进线程里做。
        await asyncio.to_thread(
            self._write_json,
            file_path,
            document,
        )

        return {
            "path": str(file_path),
            "format": "json",
        }

    @staticmethod
    def _write_json(
        file_path: Path,
        document: dict,
    ) -> None:
        """序列化并写盘（在线程里执行）。"""

        file_path.write_text(
            json.dumps(
                document,
                ensure_ascii=False,
                indent=2,
                default=str,
            ),
            encoding="utf-8",
        )

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
