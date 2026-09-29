"""Comparison API 路由。"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.comparison import (
    ComparisonCreateRequest,
    ComparisonResponse,
)
from app.services.comparison_service import (
    comparison_service,
)


router = APIRouter(
    prefix="/comparison",
    tags=["Comparison"],
)


@router.post(
    "",
    response_model=ComparisonResponse,
)
async def create_comparison(
    request: ComparisonCreateRequest,
    session: AsyncSession = Depends(
        get_db
    ),
) -> ComparisonResponse:
    """
    比较两个已经完成的项目分析结果。
    """

    return await (
        comparison_service.create_comparison(
            session,
            request,
        )
    )