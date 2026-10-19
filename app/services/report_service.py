"""报告查询、文件回读与结构化报告重建。"""

import json
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ValidationError
from app.core.logging import get_logger
from app.persistence.repositories.analysis_run import AnalysisRunRepository
from app.persistence.repositories.checkpoint import CheckpointRepository
from app.schemas.analysis import AnalysisJsonReportResponse, AnalysisReportResponse

logger = get_logger(__name__)


class ReportService:
    """读取分析报告，在文件缺失时从检查点重建 JSON 文档。"""

    @staticmethod
    async def _get_state(session: AsyncSession, run_id: str):
        try:
            return await CheckpointRepository(session).get_latest(run_id)
        except Exception as error:
            logger.warning(
                "checkpoint load failed | run_id=%s | %s: %s",
                run_id,
                type(error).__name__,
                error,
            )
            return None

    async def get_report_json(
        self,
        session: AsyncSession,
        run_id: str,
    ) -> AnalysisJsonReportResponse:
        """
        获取结构化报告（Phase 14.2）。

        两条路：

        1. 读 Finalizer 落盘的 .json（正常路径）
        2. 文件不在了就用 ReportDocumentBuilder
           从 checkpoint 现场重建

        第 2 条不只是兜底：
        早期 run 没产出过 JSON，
        现场重建让它们也能拿到结构化报告。
        """

        run_repo = AnalysisRunRepository(session)

        run = await run_repo.get_by_id(run_id)

        if run is None:
            raise ValidationError(f"Analysis run not found: {run_id}")

        # 加载 checkpoint
        state = await self._get_state(session, run_id)

        data = state.data if state is not None else {}

        # 1. 尝试从磁盘读取 JSON 报告
        json_path = self.get_json_report_path(run_id, data)

        if json_path:
            try:
                document = json.loads(Path(json_path).read_text(encoding="utf-8"))

                return AnalysisJsonReportResponse(
                    run_id=run_id,
                    status=run.status,
                    document=document,
                )
            except (OSError, ValueError):
                pass

        # 2. 从 checkpoint 现场重建
        if data:
            from app.analysis.reporting.report_document import ReportDocumentBuilder

            document = ReportDocumentBuilder.build_document(
                data,
                run_id=run_id,
            )

            return AnalysisJsonReportResponse(
                run_id=run_id,
                status=run.status,
                document=document,
            )

        return AnalysisJsonReportResponse(
            run_id=run_id,
            status=run.status,
            document=None,
        )

    async def get_report(
        self,
        session: AsyncSession,
        run_id: str,
    ) -> AnalysisReportResponse:
        """获取最终分析报告。"""

        run_repo = AnalysisRunRepository(session)

        run = await run_repo.get_by_id(run_id)

        if run is None:
            raise ValidationError(f"Analysis run not found: {run_id}")

        # 加载 checkpoint
        state = await self._get_state(session, run_id)

        report = None

        if state is not None:
            report = state.data.get("final_report")

        # 从磁盘读取报告内容
        report = self.get_report_from_disk(run_id, report)

        return AnalysisReportResponse(
            run_id=run.id,
            status=run.status,
            report=report,
        )

    @staticmethod
    def get_report_from_disk(run_id: str, report: dict | None) -> dict | None:
        """
        用磁盘上的报告文件补齐 report。

        两种情况都走这里：
        - report 完全没有（checkpoint 读不出来）
        - report 有路径但没有正文（state 瘦身时丢掉了 content）

        Args:
            run_id: Analysis Run ID
            report: 从 state.data 读到的 final_report

        Returns:
            补齐后的 report
        """
        directory = Path("reports")
        path = None

        if isinstance(report, dict):
            inner = report.get("report")
            if isinstance(inner, dict):
                path = inner.get("path")

        candidates = []

        if path:
            candidates.append(Path(path))

        candidates.append(directory / f"{run_id}_analysis.md")

        for candidate in candidates:
            if not candidate.is_file():
                continue

            try:
                content = candidate.read_text(encoding="utf-8")
            except OSError:
                continue

            # 如果已经有 content 就不覆盖
            if isinstance(report, dict) and report.get("content"):
                return report

            return {
                "report": {
                    "path": str(candidate),
                    "format": "markdown",
                },
                "content": content,
            }

        return report

    @staticmethod
    def get_json_report_path(run_id: str, data: dict) -> str | None:
        """
        找出 JSON 报告文件路径。

        Args:
            run_id: Analysis Run ID
            data: state.data

        Returns:
            JSON 报告文件路径或 None
        """
        final_report = data.get("final_report") if isinstance(data, dict) else None

        if isinstance(final_report, dict):
            json_report = final_report.get("json_report")

            if isinstance(json_report, dict):
                candidate = json_report.get("path")

                if candidate and Path(candidate).is_file():
                    return candidate

        # 早期 run 没记录路径，按命名约定猜一下
        fallback = Path("reports") / f"{run_id}_analysis.json"

        if fallback.is_file():
            return str(fallback)

        return None


report_service = ReportService()
