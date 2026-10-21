"""组合根：组装分析工作流、运行上下文、存储和外部服务。"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.analysis.agents.agent_registry import create_agent_registry
from app.analysis.context.manager import ContextManager
from app.analysis.evidence.store import EvidenceStore
from app.analysis.memory.manager import MemoryManager
from app.analysis.skills.registry import create_skill_registry
from app.analysis.tools.dependency_analyzer_tool import DependencyAnalyzerTool
from app.analysis.workflow import AnalysisWorkflowOrchestrator, build_analysis_workflow
from app.integrations.github.file_reader_tool import FileReaderTool
from app.integrations.github.github_code_search_tool import GitHubCodeSearchTool
from app.integrations.github.github_repository_tool import GitHubRepositoryTool
from app.integrations.llm.chat_tool import LLMChatTool
from app.integrations.report_export_tool import ReportExportTool
from app.persistence.repositories.checkpoint import CheckpointRepository
from app.persistence.repositories.project_memory import ProjectMemoryRepository
from app.workflow.checkpoint import CheckpointManager
from app.workflow.context import WorkflowContext
from app.workflow.engine import WorkflowEngine


class WorkflowContextFactory:
    """
    WorkflowContext 工厂。

    职责：
    - 创建请求作用域的 WorkflowContext
    - 依赖注入（Skill/Agent/Tool）
    - 为分析组件注入证据存储和历史记忆查询
    """

    def __init__(self, session):
        """
        Args:
            session: 数据库会话
        """
        self.session = session

    def create(self, repository_id: int) -> WorkflowContext:
        """
        创建 WorkflowContext。

        刻意不做缓存。

        原来这里有一个 self._context_cache，
        但工厂本身是按请求创建的
        （见 app/services/analysis_service.py 的 _get_workflow），
        所以这个缓存永远命中不了 ——
        只留下「以为复用了、其实每次都重建」的错觉，
        以及一个会把 Context（连带 request 级 session）
        留到工厂实例生命结束的引用。

        也不改成全局单例：Context 持有请求级 session，
        跨请求复用会把不同请求的会话串在一起。

        Args:
            repository_id: Repository ID

        Returns:
            WorkflowContext
        """
        return self._build_context(repository_id)

    def _build_context(self, repository_id: int) -> WorkflowContext:
        """
        实际创建 WorkflowContext。

        Context 及其存储组件与当前请求的 Session 共享生命周期。

        Args:
            repository_id: Repository ID

        Returns:
            WorkflowContext
        """
        # 创建 Skill Registry
        skill_registry = create_skill_registry()

        # 创建 Agent Registry
        agent_registry = create_agent_registry(skill_registry)

        # 创建 Tools
        tools = {
            "github_repository": GitHubRepositoryTool(),
            "github_code_search": GitHubCodeSearchTool(),
            "file_reader": FileReaderTool(),
            "dependency_analyzer": DependencyAnalyzerTool(),
            "report_export": ReportExportTool(),
            "llm_chat": LLMChatTool(),
        }

        # 创建 Memory 和 Context Manager
        memory_manager = MemoryManager(ProjectMemoryRepository(self.session))

        # 通过数据库中的项目记录组装跨 run 历史记忆。
        context_manager = ContextManager(memory_manager)

        return WorkflowContext(
            agents=agent_registry.agents,
            tools=tools,
            skills=skill_registry.skills,
            config={
                "repository_id": repository_id,
            },
            evidence_store=EvidenceStore(self.session),
            memory_manager=memory_manager,
            context_manager=context_manager,
        )


def create_analysis_workflow(session: AsyncSession) -> AnalysisWorkflowOrchestrator:
    """为本次业务操作组装工作流，共享同一数据库 Session。"""
    # 节点完成后提交同一 Session 中的证据和检查点，保留中断恢复语义。
    checkpoint = CheckpointManager(CheckpointRepository(session), commit=session.commit)
    return AnalysisWorkflowOrchestrator(
        engine=WorkflowEngine(checkpoint=checkpoint),
        context_factory=WorkflowContextFactory(session),
        checkpoint_manager=checkpoint,
        workflow_builder=build_analysis_workflow,
    )
