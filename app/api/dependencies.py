"""HTTP 请求作用域的数据库会话与业务服务依赖。"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.persistence.session import AsyncSessionLocal
from app.services.analysis_service import AnalysisService, analysis_service
from app.services.report_service import ReportService, report_service


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """在请求结束时关闭 Session；提交边界由业务操作明确控制。"""
    async with AsyncSessionLocal() as session:
        yield session


def get_analysis_service() -> AnalysisService:
    return analysis_service


def get_report_service() -> ReportService:
    return report_service
