"""
分析服务的组合根（composition root）。

为什么在 services 层而不是 domain 层：
本模块要 new 出一整串基础设施实现
（Repository / CheckpointManager / WorkflowEngine / ContextFactory），
而 domain 层的规则是**只依赖自己定义的接口**。
把组合根留在 app/domain/analysis/factory.py 里，
等于让 domain 目录反向 import infrastructure，
分层守卫测试会当场失败。

依赖方向：api → services → domain → infrastructure
组合根天然要同时认识 domain 与 infrastructure，因此它属于 services。
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
