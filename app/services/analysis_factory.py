"""组合根：组装分析工作流、运行上下文、存储和外部服务。"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.analysis.agents.agent_registry import create_agent_registry
from app.analysis.context.manager import ContextManager
from app.analysis.evidence.store import EvidenceStore
from app.analysis.memory.manager import MemoryManager
from app.analysis.skills.registry import create_skill_registry
from app.analysis.tools.dependency_analyzer_tool import DependencyAnalyzerTool
from app.analysis.tools.rag_retrieval_tool import RagRetrievalTool
from app.analysis.workflow import AnalysisWorkflowOrchestrator, build_analysis_workflow
from app.integrations.embeddings.ollama import OllamaEmbedding
from app.integrations.github.file_reader_tool import FileReaderTool
from app.integrations.github.github_code_search_tool import GitHubCodeSearchTool
from app.integrations.github.github_repository_tool import GitHubRepositoryTool
from app.integrations.llm.chat_tool import LLMChatTool
from app.integrations.report_export_tool import ReportExportTool
from app.integrations.vector_store.qdrant import QdrantVectorStore
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

        # RAG 检索工具常驻注册。
        #
        # 原因：RAG 现在可以**按次开启**（请求里的 enable_rag），
        # 而 build_context 不知道这一次的开关状态 ——
        # 若按全局 RAG_ENABLED 决定是否注册，
        # 全局关、单次开的组合就会拿不到这个工具，
        # 开关看起来"点了没反应"。
        #
        # 真正的启用判断在 EvidenceAnalysisSkill._from_rag 里。
        #
        # 这两个对象也是「索引」与「检索」共用的那一份：
        # EvidenceAnalysisSkill 建索引时直接取它们，
        # 不再各建一套。
        tools["rag_retrieval"] = RagRetrievalTool(
            embedding=OllamaEmbedding(),
            vector_store=QdrantVectorStore(),
        )

        # 创建 Memory 和 Context Manager
        memory_manager = MemoryManager(ProjectMemoryRepository(self.session))

        # 刻意不传语义检索。
        #
        # 本项目的 RAG 通路是独立且已可用的：
        # EvidenceAnalysisSkill → RagRetrievalTool → evidence
        # （由 RAG_ENABLED / enable_rag 按次开关）。
        # 若在这里再接语义检索，就会对同一份语料
        # 做第二次检索 —— 重复且多付一次 Ollama 嵌入 + Qdrant 往返。
        #
        # ContextManager 的职责是「跨 run 历史记忆」，
        # 不是「语义召回」。
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
