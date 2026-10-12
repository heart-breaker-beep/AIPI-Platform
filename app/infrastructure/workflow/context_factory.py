"""
WorkflowContext 工厂 - 负责创建 WorkflowContext。

职责：
- 创建 Skill/Agent/Tool 实例
- 依赖注入
"""

from app.core.logging import get_logger
from app.embeddings.ollama import OllamaEmbedding
from app.infrastructure.agents.agent_registry import create_agent_registry
from app.infrastructure.enrichment.context.manager import ContextManager
from app.infrastructure.enrichment.memory.manager import MemoryManager
from app.infrastructure.skills.registry import create_skill_registry
from app.infrastructure.tools.dependency_analyzer_tool import DependencyAnalyzerTool
from app.infrastructure.tools.file_reader_tool import FileReaderTool
from app.infrastructure.tools.github.github_code_search_tool import GitHubCodeSearchTool
from app.infrastructure.tools.github.github_repository_tool import GitHubRepositoryTool
from app.infrastructure.tools.llm_chat_tool import LLMChatTool
from app.infrastructure.tools.mysql_query_tool import MySQLQueryTool
from app.infrastructure.tools.qdrant_search_tool import QdrantSearchTool
from app.infrastructure.tools.rag_retrieval_tool import RagRetrievalTool
from app.infrastructure.tools.report_export_tool import ReportExportTool
from app.infrastructure.workflow.context import WorkflowContext
from app.vector_store.qdrant import QdrantVectorStore

logger = get_logger(__name__)


class WorkflowContextFactory:
    """
    WorkflowContext 工厂。

    职责：
    - 创建和缓存 WorkflowContext
    - 依赖注入（Skill/Agent/Tool）
    - 避免重复创建
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
        （见 app/services/analysis_service.py 的 _get_domain_service），
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

        Context 中的 Skill/Agent/Tool 都是无状态服务，
        每次重建的代价只是一批对象构造；
        真正贵的客户端（LLM、向量库）都是惰性连接，
        不会因为重建而多开连接。

        Args:
            repository_id: Repository ID

        Returns:
            WorkflowContext
        """
        # 创建 Skill Registry（单例）
        skill_registry = create_skill_registry()

        # 创建 Agent Registry（单例）
        agent_registry = create_agent_registry(skill_registry)

        # 创建 Tools（单例）
        tools = {
            "github_repository": GitHubRepositoryTool(),
            "github_code_search": GitHubCodeSearchTool(),
            "file_reader": FileReaderTool(),
            "dependency_analyzer": DependencyAnalyzerTool(),
            "qdrant_search": QdrantSearchTool(),
            "mysql_query": MySQLQueryTool(self.session),
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
        # 构造开销可以忽略：OllamaEmbedding 与 QdrantVectorStore
        # 都是惰性客户端，只记地址、不建连接。
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
        memory_manager = MemoryManager(self.session)

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
                "session": self.session,
                "repository_id": repository_id,
            },
            memory_manager=memory_manager,
            context_manager=context_manager,
        )
