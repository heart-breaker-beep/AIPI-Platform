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

from app.agents.agent_registry import (
    create_agent_registry,
)
from app.context.manager import (
    ContextManager,
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
from app.tools.mysql_query_tool import (
    MySQLQueryTool,
)
from app.tools.qdrant_search_tool import (
    QdrantSearchTool,
)
from app.tools.report_export_tool import (
    ReportExportTool,
)
from app.skills.registry import (
    create_skill_registry,
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
        }

        memory_manager = (
            MemoryManager(
                self.session
            )
        )

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
    ):
        """启动新的 Analysis Workflow。"""

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

    async def get_report(
        self,
        run_id: str,
    ):
        """获取最终报告。"""

        state = await self.checkpoint.load(
            run_id
        )

        if state is None:
            raise ValueError(
                f"Checkpoint not found: {run_id}"
            )

        return state.data.get(
            "final_report"
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