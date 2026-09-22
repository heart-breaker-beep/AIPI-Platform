"""Analysis API 路由，负责接收请求并调用 Analysis Service。"""

from fastapi import APIRouter

from app.schemas.analysis import (
    AnalysisCreateRequest,
    AnalysisResponse,
)
from app.services.analysis_service import analysis_service


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
) -> AnalysisResponse:
    """创建一个新的 GitHub 项目分析任务。"""

    # Router 只负责 HTTP 层，
    # 具体业务逻辑交给 Service，避免 API 层越来越复杂。
    return analysis_service.create_analysis(request)


@router.get(
    "/{run_id}",
    response_model=AnalysisResponse,
)
async def get_analysis(
    run_id: str,
) -> AnalysisResponse:
    """根据 run_id 查询分析任务。"""

    return analysis_service.get_analysis(run_id)