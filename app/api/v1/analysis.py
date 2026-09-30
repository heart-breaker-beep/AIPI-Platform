"""Analysis API 路由。"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.analysis import (
    AnalysisCreateRequest,
    AnalysisDeepDiveResponse,
    AnalysisJsonReportResponse,
    AnalysisReportResponse,
    AnalysisResponse,
    LearningPathResponse,
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
    "",
    response_model=list[AnalysisResponse],
)
async def list_analyses(
    limit: int = Query(
        20,
        ge=1,
        le=100,
        description="最多返回多少条",
    ),
    session: AsyncSession = Depends(get_db),
) -> list[AnalysisResponse]:
    """
    列出最近的分析任务。

    给前端的历史列表用 ——
    没有这个接口时，页面关掉就找不回
    之前跑过的分析了。
    """

    return await analysis_service.list_analyses(
        session,
        limit,
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


@router.get(
    "/{run_id}/report/json",
    response_model=AnalysisJsonReportResponse,
)
async def get_analysis_json_report(
    run_id: str,
    session: AsyncSession = Depends(get_db),
) -> AnalysisJsonReportResponse:
    """
    获取结构化报告（JSON）。

    markdown 报告是给人读的排版结果；
    这一份是同一份数据的结构化形态，
    供程序消费。

    优先读落盘的 .json；
    读不到就用 ReportService 现场重建，
    因此早期 run 也能拿到。
    """

    return await analysis_service.get_report_json(
        session,
        run_id,
    )


@router.post(
    "/{run_id}/learning-path",
    response_model=LearningPathResponse,
)
async def learning_path(
    run_id: str,
    goal: str | None = Query(
        None,
        description=(
            "学习目标，留空则用该 run 的分析问题"
        ),
    ),
    session: AsyncSession = Depends(get_db),
) -> LearningPathResponse:
    """
    生成项目的学习路线（Phase 14.1）。

    基于该 run 已有的分析结果，
    不重新联网、不重新分析。

    产物：学习顺序 / 需要掌握的技术 /
    核心源码 / 推荐阅读路径 / 改造建议。

    该接口只读不写，不修改原报告。
    """

    return await analysis_service.learning_path(
        session,
        run_id,
        goal,
    )


@router.post(
    "/{run_id}/deep-dive",
    response_model=AnalysisDeepDiveResponse,
)
async def deep_dive_module(
    run_id: str,
    module: str = Query(
        ...,
        description=(
            "要深挖的模块：agents / workflow / "
            "skills / tools / rag / memory"
        ),
    ),
    session: AsyncSession = Depends(get_db),
) -> AnalysisDeepDiveResponse:
    """
    对已完成 run 的单个模块做深挖。

    默认报告每章只给要点与证据锚点；
    想看某个模块的实现细节
    （签名 / 调用链 / 关键常量 / 源码片段）时走这里。

    该接口只读不写：不修改原 run，
    产物是单独一份 markdown 报告。
    """

    return await analysis_service.deep_dive_module(
        session,
        run_id,
        module,
    )