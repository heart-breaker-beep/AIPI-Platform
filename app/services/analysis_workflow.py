"""
Analysis Workflow Runner。

负责把：

AnalysisRun
    ↓
Workflow
    ↓
WorkflowEngine
    ↓
Checkpoint
    ↓
AnalysisRun

真正连接起来。
"""

import json
from pathlib import Path

from app.agents.agent_registry import (
    create_agent_registry,
)
from app.context.manager import (
    ContextManager,
)
from app.core.config import (
    get_settings,
)
from app.core.logging import get_logger
from app.embeddings.ollama import (
    OllamaEmbedding,
)
from app.memory.manager import (
    MemoryManager,
)
from app.models.repository import Repository
from app.repositories.analysis_run import (
    AnalysisRunRepository,
)
from app.repositories.checkpoint import (
    CheckpointRepository,
)
from app.skills.registry import (
    create_skill_registry,
)
from app.tools.dependency_analyzer_tool import (
    DependencyAnalyzerTool,
)
from app.tools.file_reader_tool import (
    FileReaderTool,
)
from app.tools.github.github_code_search_tool import (
    GitHubCodeSearchTool,
)
from app.tools.github.github_repository_tool import (
    GitHubRepositoryTool,
)
from app.tools.llm_chat_tool import (
    LLMChatTool,
)
from app.tools.mysql_query_tool import (
    MySQLQueryTool,
)
from app.tools.qdrant_search_tool import (
    QdrantSearchTool,
)
from app.tools.rag_retrieval_tool import (
    RagRetrievalTool,
)
from app.tools.report_export_tool import (
    ReportExportTool,
)
from app.vector_store.qdrant import (
    QdrantVectorStore,
)
from app.workflow.analysis_workflow import (
    build_analysis_workflow,
)
from app.workflow.checkpoint import (
    CheckpointManager,
)
from app.workflow.context import (
    WorkflowContext,
)
from app.workflow.engine import (
    WorkflowEngine,
)
from app.workflow.state import (
    WorkflowState,
)

logger = get_logger(__name__)


class AnalysisWorkflowRunner:
    """Analysis Workflow 执行器。"""

    def __init__(
        self,
        session,
    ):
        self.session = session

        self.checkpoint_repository = (
            CheckpointRepository(
                session
            )
        )

        self.checkpoint = (
            CheckpointManager(
                self.checkpoint_repository
            )
        )

        self.engine = WorkflowEngine(
            checkpoint=self.checkpoint
        )

    def build_context(
        self,
        *,
        repository_id: int,
    ) -> WorkflowContext:
        """创建完整 WorkflowContext。"""

        skill_registry = (
            create_skill_registry()
        )

        agent_registry = (
            create_agent_registry(
                skill_registry
            )
        )

        tools = {
            "github_repository":
                GitHubRepositoryTool(),

            "github_code_search":
                GitHubCodeSearchTool(),

            "file_reader":
                FileReaderTool(),

            "dependency_analyzer":
                DependencyAnalyzerTool(),

            "qdrant_search":
                QdrantSearchTool(),

            "mysql_query":
                MySQLQueryTool(
                    self.session
                ),

            "report_export":
                ReportExportTool(),

            "llm_chat":
                LLMChatTool(),
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
        tools["rag_retrieval"] = (
            RagRetrievalTool(
                embedding=OllamaEmbedding(),
                vector_store=QdrantVectorStore(),
            )
        )

        memory_manager = (
            MemoryManager(
                self.session
            )
        )

        # 刻意不传 retriever。
        #
        # 本项目的 RAG 通路是独立且已可用的：
        # EvidenceAnalysisSkill → RagRetrievalTool → evidence
        # （由 RAG_ENABLED / enable_rag 按次开关）。
        # 若在这里再接 QdrantContextRetriever，就会对同一份语料
        # 做第二次检索 —— 重复且多付一次 Ollama 嵌入 + Qdrant 往返。
        #
        # ContextManager 的职责是「跨 run 历史记忆」，
        # 不是「语义召回」。
        context_manager = (
            ContextManager(
                memory_manager
            )
        )

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

    async def start(
        self,
        run_id: str,
        enable_rag: bool | None = None,
    ):
        """
        启动新的 Analysis Workflow。

        enable_rag：
            按次覆盖 RAG 开关。
            留空则跟随服务端 RAG_ENABLED 配置。
            结果写进 state.data，由证据环节读取 ——
            这样不必为此加数据库列，也不会影响其它 run。
        """

        run_repo = AnalysisRunRepository(
            self.session
        )

        run = await run_repo.get_by_id(
            run_id
        )

        if run is None:
            raise ValueError(
                f"Analysis run not found: {run_id}"
            )

        repository = await self.session.get(
            Repository,
            run.repository_id,
        )

        if repository is None:
            raise ValueError(
                f"Repository not found: "
                f"{run.repository_id}"
            )

        state = WorkflowState(
            run_id=run.id
        )

        state.data = {
            "run_id": run.id,
            "repository_id": repository.id,
            "repo_url": repository.url,
            "owner": repository.owner,
            "repo": repository.name,
            # RAG 按次开关：请求没指定就跟服务端配置走。
            "rag_enabled": (
                get_settings().RAG_ENABLED
                if enable_rag is None
                else bool(enable_rag)
            ),
            "question": (
                run.question
                or (
                    "请分析这个 GitHub Agent 项目，"
                    "重点分析 Multi-Agent、Workflow、"
                    "Skill、Tool、RAG、Memory 和数据库。"
                )
            ),
        }

        context = self.build_context(
            repository_id=repository.id
        )

        workflow = (
            build_analysis_workflow(
                context
            )
        )

        result = await self.engine.run(
            workflow,
            state,
            context,
        )

        return await self._sync_run(
            result
        )

    async def approve(
        self,
        run_id: str,
    ):
        """批准 Design Gate 或 Human Review。"""

        state = await self.checkpoint.load(
            run_id
        )

        if state is None:
            raise ValueError(
                f"Checkpoint not found: {run_id}"
            )

        run_repo = AnalysisRunRepository(
            self.session
        )

        run = await run_repo.get_by_id(
            run_id
        )

        if run is None:
            raise ValueError(
                f"Analysis run not found: {run_id}"
            )

        state.approve()

        await self.checkpoint.save(
            state
        )

        context = self.build_context(
            repository_id=run.repository_id
        )

        workflow = (
            build_analysis_workflow(
                context
            )
        )

        result = await self.engine.resume(
            workflow,
            context,
            run_id,
        )

        return await self._sync_run(
            result
        )

    async def pause(
        self,
        run_id: str,
    ):
        """人工暂停 Workflow。"""

        state = await self.checkpoint.load(
            run_id
        )

        if state is None:
            raise ValueError(
                f"Checkpoint not found: {run_id}"
            )

        result = await self.engine.pause(
            state
        )

        return await self._sync_run(
            result
        )

    async def resume(
        self,
        run_id: str,
    ):
        """从 PAUSED Checkpoint 恢复。"""

        run_repo = AnalysisRunRepository(
            self.session
        )

        run = await run_repo.get_by_id(
            run_id
        )

        if run is None:
            raise ValueError(
                f"Analysis run not found: {run_id}"
            )

        context = self.build_context(
            repository_id=run.repository_id
        )

        workflow = (
            build_analysis_workflow(
                context
            )
        )

        result = await self.engine.resume(
            workflow,
            context,
            run_id,
        )

        return await self._sync_run(
            result
        )

    async def retry(
        self,
        run_id: str,
    ):
        """重新执行失败的 Workflow。"""

        run_repo = AnalysisRunRepository(
            self.session
        )

        run = await run_repo.get_by_id(
            run_id
        )

        if run is None:
            raise ValueError(
                f"Analysis run not found: {run_id}"
            )

        state = await self.checkpoint.load(
            run_id
        )

        if state is None:
            raise ValueError(
                f"Checkpoint not found: {run_id}"
            )

        context = self.build_context(
            repository_id=run.repository_id
        )

        workflow = (
            build_analysis_workflow(
                context
            )
        )

        result = await self.engine.retry(
            workflow,
            context,
            run_id,
        )

        return await self._sync_run(
            result
        )

    async def cancel(
        self,
        run_id: str,
    ):
        """
        人工放弃本次分析。

        只置状态，不删数据 ——
        报告文件、已落库的 evidence 都保留，
        用户之后仍能在历史里查看这个 run 走到过哪一步。
        """

        state = await self.checkpoint.load(
            run_id
        )

        if state is None:
            raise ValueError(
                f"Checkpoint not found: {run_id}"
            )

        state = await self.engine.cancel(state)

        return await self._sync_run(state)

    async def replan(
        self,
        run_id: str,
        question: str,
    ):
        """
        改问题后重新规划。

        做法：把 state 的 current_node 拨回 planner_agent，
        清掉上一轮规划产物，然后用不带 resume_from 的
        engine.run 重新执行该节点 ——
        引擎遇到"已有 current_node 的 state"会重跑这个节点，
        而不是像 resume 那样跳到下一个。
        重跑完 planner 会经 transition 自动回到 design_gate 停住。
        """

        run_repo = AnalysisRunRepository(
            self.session
        )

        run = await run_repo.get_by_id(
            run_id
        )

        if run is None:
            raise ValueError(
                f"Analysis run not found: {run_id}"
            )

        # run 表里的 question 也要更新：
        # 历史列表、报告头、后续 deep-dive 都读它，
        # 只改 state 会导致同一件事在两处显示不一致。
        run.question = question

        await self.session.commit()

        state = await self.checkpoint.load(
            run_id
        )

        if state is None:
            raise ValueError(
                f"Checkpoint not found: {run_id}"
            )

        state.replan(question)

        context = self.build_context(
            repository_id=run.repository_id
        )

        workflow = build_analysis_workflow(
            context
        )

        result = await self.engine.run(
            workflow,
            state,
            context,
        )

        return await self._sync_run(result)

    async def get_report(
        self,
        run_id: str,
    ):
        """
        获取最终报告。

        两条路：

        1. 从 checkpoint 读（正常路径）
        2. 读不出来时退回磁盘上的报告文件

        第 2 条是必需的，不是锦上添花：
        checkpoint 的 state_data 一旦超过
        asyncmy 的大字段读取上限，
        这个 run 的 state 就永久读不回来了，
        但报告正文其实早就写在
        reports/{run_id}_analysis.md 里。
        没有这条兜底的话，
        「分析成功但报告 500」就会一直存在。
        """

        try:

            state = await self.checkpoint.load(
                run_id
            )

        except Exception as error:

            # 读不出来不让请求挂掉，
            # 交给文件兜底。
            logger.warning(
                "checkpoint load failed | run_id=%s | %s: %s",
                run_id,
                type(error).__name__,
                error,
            )

            state = None

        report = None

        if state is not None:

            report = state.data.get(
                "final_report"
            )

        return self._report_from_disk(
            run_id,
            report,
        )

    async def learning_path(
        self,
        run_id: str,
        goal: str | None = None,
    ):
        """
        基于已有分析结果生成学习路线（Phase 14.1）。

        不重新联网、不重新分析 ——
        只用该 run 已经采集到的数据。
        产物是独立的一份 markdown，
        不修改原报告。
        """

        state = await self.checkpoint.load(run_id)

        if state is None:
            raise ValueError(
                f"Checkpoint not found: {run_id}"
            )

        data = state.data or {}

        context = self.build_context(
            repository_id=data.get(
                "repository_id"
            )
        )

        skill = context.skills.get(
            "learning_path"
        )

        if skill is None:
            raise ValueError(
                "Learning path skill is not "
                "registered."
            )

        return await skill.execute(
            context,
            {
                **data,
                "run_id": run_id,
                "goal": goal or data.get("question"),
            },
        )

    async def get_json_report(
        self,
        run_id: str,
    ):
        """
        获取结构化报告（Phase 14.2）。

        优先读 Finalizer 落盘的 .json；
        读不到就用 ReportService 从
        checkpoint 的 state 现场重建。

        现场重建让早期 run（没产出过 JSON）
        也能拿到结构化报告。
        """

        state = None

        try:

            state = await self.checkpoint.load(
                run_id
            )

        except Exception as error:

            logger.warning(
                "checkpoint load failed for json "
                "report | run_id=%s | %s: %s",
                run_id,
                type(error).__name__,
                error,
            )

        data = (
            state.data
            if state is not None
            else {}
        )

        # 1. 落盘的 JSON
        path = self._json_report_path(
            run_id,
            data,
        )

        if path is not None:

            try:

                return json.loads(
                    Path(path).read_text(
                        encoding="utf-8"
                    )
                )

            except (OSError, ValueError):

                # 文件损坏时继续走重建，
                # 不把「读到坏文件」变成 500。
                pass

        # 2. 现场重建
        if not data:

            return None

        from app.services.report_service import (
            ReportService,
        )

        return ReportService.build_document(
            data,
            run_id=run_id,
        )

    @staticmethod
    def _json_report_path(
        run_id: str,
        data: dict,
    ):
        """找出 JSON 报告文件路径。"""

        final_report = (
            data.get("final_report")
            if isinstance(data, dict)
            else None
        )

        if isinstance(final_report, dict):

            json_report = final_report.get(
                "json_report"
            )

            if isinstance(json_report, dict):

                candidate = json_report.get("path")

                if candidate and Path(candidate).is_file():

                    return candidate

        # 早期 run 没记录路径，
        # 按命名约定猜一下。
        fallback = (
            Path("reports")
            / f"{run_id}_analysis.json"
        )

        if fallback.is_file():
            return str(fallback)

        return None

    @staticmethod
    def _report_from_disk(
        run_id: str,
        report,
    ):
        """
        用磁盘上的报告文件补齐 report。

        两种情况都走这里：

        - report 完全没有（checkpoint 读不出来）
        - report 有路径但没有正文
          （state 瘦身时丢掉了 content）
        """

        directory = Path("reports")

        path = None

        if isinstance(report, dict):

            inner = report.get("report")

            if isinstance(inner, dict):

                path = inner.get("path")

        candidates = []

        if path:

            candidates.append(Path(path))

        candidates.append(
            directory / f"{run_id}_analysis.md"
        )

        for candidate in candidates:

            if not candidate.is_file():
                continue

            try:

                content = candidate.read_text(
                    encoding="utf-8"
                )

            except OSError:

                continue

            if isinstance(report, dict) and report.get(
                "content"
            ):

                return report

            return {
                "report": {
                    "path": str(candidate),
                    "format": "markdown",
                },
                "content": content,
            }

        return report

    async def deep_dive_module(
        self,
        run_id: str,
        module: str,
    ):
        """
        对某个已完成 run 的单个模块做深挖。

        复用该 run 已保存的仓库信息
        （owner / repo / branch / readme），
        因此不需要重新解析 URL，
        也不需要重跑整个分析流程。

        深挖只读不写：不修改 checkpoint，
        产物是单独一份 markdown。
        """

        state = await self.checkpoint.load(
            run_id
        )

        if state is None:
            raise ValueError(
                f"Checkpoint not found: {run_id}"
            )

        data = state.data or {}

        owner = data.get("owner")

        repo = data.get("repo")

        if not owner or not repo:
            raise ValueError(
                "该 run 缺少 owner / repo，"
                "无法定位仓库做深挖。"
            )

        repository = await self.session.get(
            Repository,
            data.get("repository_id"),
        )

        context = self.build_context(
            repository_id=data.get(
                "repository_id"
            )
        )

        skill = context.skills.get(
            "module_deep_dive"
        )

        if skill is None:
            raise ValueError(
                "Module deep dive skill "
                "is not registered."
            )

        return await skill.execute(
            context,
            {
                "run_id": run_id,
                "module": module,
                "owner": owner,
                "repo": repo,
                "branch": data.get(
                    "branch",
                    "main",
                ),
                "readme": data.get("readme"),
                "repository": data.get(
                    "repository"
                ),
                "repo_url": (
                    repository.url
                    if repository is not None
                    else data.get("repo_url")
                ),
            },
        )

    async def _sync_run(
        self,
        state,
    ):
        """把 Workflow 状态同步到 AnalysisRun。"""

        run_repo = AnalysisRunRepository(
            self.session
        )

        run = await run_repo.get_by_id(
            state.run_id
        )

        if run is None:
            raise ValueError(
                f"Analysis run not found: "
                f"{state.run_id}"
            )

        await run_repo.update_runtime_state(
            run,
            status=state.status,
            current_node=state.current_node,
            retry_count=state.retry_count,
        )

        await self.session.commit()

        return state