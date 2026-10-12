"""
Domain Service 工厂 - 负责创建 Domain Service 实例。

职责：
- 组装 Domain Service 的依赖
- 依赖注入
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.analysis.service import AnalysisService
from app.domain.analysis.workflow import AnalysisWorkflowOrchestrator
from app.infrastructure.persistence.repositories.analysis_run import (
    AnalysisRunRepository,
)
from app.infrastructure.persistence.repositories.checkpoint import CheckpointRepository
from app.infrastructure.workflow.analysis_workflow import build_analysis_workflow
from app.infrastructure.workflow.checkpoint import CheckpointManager
from app.infrastructure.workflow.context_factory import WorkflowContextFactory
from app.infrastructure.workflow.engine import WorkflowEngine


def create_analysis_service(session: AsyncSession) -> AnalysisService:
    """
    创建 AnalysisService 实例。

    Args:
        session: 数据库会话

    Returns:
        AnalysisService 实例
    """
    # 创建 Infrastructure 层依赖
    checkpoint_repo = CheckpointRepository(session)
    checkpoint_manager = CheckpointManager(checkpoint_repo)
    engine = WorkflowEngine(checkpoint=checkpoint_manager)
    context_factory = WorkflowContextFactory(session)

    # 创建 Domain 层 Orchestrator
    orchestrator = AnalysisWorkflowOrchestrator(
        engine=engine,
        context_factory=context_factory,
        checkpoint_manager=checkpoint_manager,
        workflow_builder=build_analysis_workflow,
    )

    # 创建 Repository
    run_repo = AnalysisRunRepository(session)

    # 创建 Domain Service
    return AnalysisService(
        workflow_orchestrator=orchestrator,
        run_repository=run_repo,
        checkpoint_repository=checkpoint_repo,
    )
