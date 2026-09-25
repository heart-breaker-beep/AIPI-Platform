"""Analysis API 路由。"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.analysis import (
    AnalysisCreateRequest,
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
    """创建 GitHub 项目分析任务。"""

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
    """根据 run_id 查询分析任务。"""

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
    """通过 Design Gate。"""

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
    """暂停分析任务。"""

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
    """恢复分析任务。"""

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
    """重试失败的分析任务。"""

    return await analysis_service.retry_analysis(
        session,
        run_id,
    )