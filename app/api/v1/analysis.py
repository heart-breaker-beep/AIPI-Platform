"""Analysis API 路由。"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.analysis import (
    AnalysisCreateRequest,
    AnalysisReportResponse,
    AnalysisResponse,
)
from app.services.analysis_service import (
    analysis_service,
)


router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"],
)


@router.post(
    "",
    response_model=AnalysisResponse,
)
async def create_analysis(
    request: AnalysisCreateRequest,
    session: AsyncSession = Depends(get_db),
) -> AnalysisResponse:
    """创建并启动 GitHub 项目分析 Workflow。"""

    return await analysis_service.create_analysis(
        session,
        request,
    )


@router.get(
    "/{run_id}",
    response_model=AnalysisResponse,
)
async def get_analysis(
    run_id: str,
    session: AsyncSession = Depends(get_db),
) -> AnalysisResponse:
    """查询分析任务。"""

    return await analysis_service.get_analysis(
        session,
        run_id,
    )


@router.post(
    "/{run_id}/approve",
    response_model=AnalysisResponse,
)
async def approve_analysis(
    run_id: str,
    session: AsyncSession = Depends(get_db),
) -> AnalysisResponse:
    """批准 Design Gate 或 Human Review。"""

    return await analysis_service.approve_analysis(
        session,
        run_id,
    )


@router.post(
    "/{run_id}/pause",
    response_model=AnalysisResponse,
)
async def pause_analysis(
    run_id: str,
    session: AsyncSession = Depends(get_db),
) -> AnalysisResponse:
    """暂停 Workflow。"""

    return await analysis_service.pause_analysis(
        session,
        run_id,
    )


@router.post(
    "/{run_id}/resume",
    response_model=AnalysisResponse,
)
async def resume_analysis(
    run_id: str,
    session: AsyncSession = Depends(get_db),
) -> AnalysisResponse:
    """恢复 PAUSED Workflow。"""

    return await analysis_service.resume_analysis(
        session,
        run_id,
    )


@router.post(
    "/{run_id}/retry",
    response_model=AnalysisResponse,
)
async def retry_analysis(
    run_id: str,
    session: AsyncSession = Depends(get_db),
) -> AnalysisResponse:
    """重试失败 Workflow。"""

    return await analysis_service.retry_analysis(
        session,
        run_id,
    )


@router.get(
    "/{run_id}/report",
    response_model=AnalysisReportResponse,
)
async def get_analysis_report(
    run_id: str,
    session: AsyncSession = Depends(get_db),
) -> AnalysisReportResponse:
    """获取最终项目智能分析报告。"""

    return await analysis_service.get_report(
        session,
        run_id,
    )