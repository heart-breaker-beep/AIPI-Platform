"""
Analysis Application Service - API 适配层。

职责：
- HTTP 请求校验
- 数据库 CRUD 操作
- DTO 转换（AnalysisRun → AnalysisResponse）
- 委托 Domain Service 执行核心业务
- 事务管理

重构说明：
- 保持原有 API 接口不变
- 委托 Domain Service 执行 Workflow 编排
- 使用新架构的 Infrastructure 层
"""

from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.exceptions import ValidationError
from app.core.logging import (
    get_logger,
    log_with_run_id,
)
from app.domain.analysis import create_analysis_service
from app.infrastructure.persistence.models.repository import Repository
from app.infrastructure.persistence.repositories.analysis_run import (
    AnalysisRunRepository,
)
from app.infrastructure.persistence.repositories.checkpoint import (
    CheckpointRepository,
)
from app.infrastructure.persistence.repositories.repository_basic import (
    RepositoryRepository,
)
from app.infrastructure.skills.module_deep_dive_skill import (
    ModuleDeepDiveSkill,
)
from app.infrastructure.tools.github.parser import (
    parse_github_url,
)
from app.schemas.analysis import (
    AnalysisCreateRequest,
    AnalysisDeepDiveResponse,
    AnalysisJsonReportResponse,
    AnalysisReplanRequest,
    AnalysisReportResponse,
    AnalysisResponse,
    LearningPathResponse,
)

logger = get_logger(__name__)


class AnalysisService:
    """
    Analysis Application Service - API 适配层。

    职责：
    - 业务校验（URL 格式、状态校验）
    - 数据库操作（Repository、AnalysisRun CRUD）
    - 委托 Domain Service 执行核心业务
    - 同步 Workflow 状态到数据库
    - DTO 转换

    重构说明：
    - 保留为 Application Service（不是 Domain Service）
    - 委托 domain.analysis.AnalysisService 执行业务编排
    - 负责数据库事务和 DTO 转换
    """

    def _get_domain_service(self, session: AsyncSession):
        """获取 Domain Service 实例（工厂方法）"""
        return create_analysis_service(session)

    async def create_analysis(
        self,
        session: AsyncSession,
        request: AnalysisCreateRequest,
    ) -> AnalysisResponse:
        """创建并启动单项目分析 Workflow。"""

        repo_url = request.repo_url.strip()

        if not repo_url:
            raise ValidationError(
                "Repository URL cannot be empty."
            )

        if not repo_url.startswith(
            (
                "https://github.com/",
                "http://github.com/",
            )
        ):
            raise ValidationError(
                "Only GitHub repository URLs are supported."
            )

        owner, name = self._parse_github_url(
            repo_url
        )

        repository_repo = (
            RepositoryRepository(
                session
            )
        )

        analysis_run_repo = (
            AnalysisRunRepository(
                session
            )
        )

        repository = (
            await repository_repo.get_by_url(
                repo_url
            )
        )

        if repository is None:
            repository = (
                await repository_repo.create(
                    url=repo_url,
                    owner=owner,
                    name=name,
                )
            )

        elif (
            repository.owner != owner
            or repository.name != name
        ):
            # 自愈历史脏数据。
            #
            # 之前 _parse_github_url 不剥离 query string，
            # 因此可能存在
            #
            #     name = "repo?utm_source=chatgpt.com"
            #
            # 这种行。它的危险之处在于不会报错：
            #
            #     api.github.com/repos/{owner}/{name}
            #         → query 被服务端忽略，元数据仍然 200
            #
            #     raw.githubusercontent.com/{owner}/{name}/...
            #         → "?" 被当成路径的一部分，全部 404
            #
            # 结果是 readme 为空、evidences 为 0、
            # technology_stack 全空，
            # 而 run 仍然被标记为 COMPLETED。
            #
            # 按 URL 命中已有行时会直接复用，
            # 所以只修解析器救不了存量数据，
            # 这里顺手把 owner / name 修正回来。
            logger.warning(
                "repairing repository row | "
                "id=%s | name %r -> %r",
                repository.id,
                repository.name,
                name,
            )

            repository.owner = owner

            repository.name = name

        run_id = str(uuid4())

        run = await analysis_run_repo.create(
            run_id=run_id,
            repository_id=repository.id,
            question=request.question,
        )

        await session.commit()

        log_with_run_id(
            logger,
            level=20,
            message="analysis workflow starting",
            run_id=run_id,
        )

        # 准备初始数据
        initial_data = {
            "run_id": run_id,
            "repository_id": repository.id,
            "repo_url": repo_url,
            "owner": owner,
            "repo": name,
            "rag_enabled": (
                get_settings().RAG_ENABLED
                if request.enable_rag is None
                else bool(request.enable_rag)
            ),
            "question": (
                request.question
                or (
                    "请分析这个 GitHub Agent 项目，"
                    "重点分析 Multi-Agent、Workflow、"
                    "Skill、Tool、RAG、Memory 和数据库。"
                )
            ),
        }

        # 使用 Domain Service 启动 Workflow
        domain_service = self._get_domain_service(session)

        state = await domain_service.start_analysis(
            run_id=run_id,
            repository_id=repository.id,
            repo_url=repo_url,
            question=initial_data["question"],
            enable_rag=initial_data["rag_enabled"],
        )

        # 同步 Workflow 状态到数据库
        await self._sync_state_to_run(session, run, state)
        await session.commit()

        run = await analysis_run_repo.get_by_id(
            run_id
        )

        if run is None:
            raise ValidationError(
                f"Analysis run not found: {run_id}"
            )

        return await self._to_response(
            session,
            run,
        )

    async def get_analysis(
        self,
        session: AsyncSession,
        run_id: str,
    ) -> AnalysisResponse:
        """查询 Analysis Run。"""

        run_repo = AnalysisRunRepository(
            session
        )

        run = await run_repo.get_by_id(
            run_id
        )

        if run is None:
            raise ValidationError(
                f"Analysis run not found: {run_id}"
            )

        return await self._to_response(
            session,
            run,
            include_plan=True,
        )

    async def cancel_analysis(
        self,
        session: AsyncSession,
        run_id: str,
    ) -> AnalysisResponse:
        """
        放弃本次分析。

        只允许从「等人工决策」或「已暂停」这些停顿态放弃。
        正在跑（ANALYZING / PLANNING）时不允许 ——
        那种情况下后台还有节点在执行，
        置成 CANCELED 会被随后的 _sync_run 覆盖回 ANALYZING，
        用户会看到"点了放弃却还在跑"。
        """

        run_repo = AnalysisRunRepository(
            session
        )

        run = await run_repo.get_by_id(
            run_id
        )

        if run is None:
            raise ValidationError(
                f"Analysis run not found: {run_id}"
            )

        if run.status not in {
            "WAITING_DESIGN",
            "WAITING_HUMAN",
            "PAUSED",
        }:
            raise ValidationError(
                f"Analysis run cannot be canceled "
                f"from status: {run.status}"
            )

        domain_service = self._get_domain_service(session)

        state = await domain_service.cancel_analysis(run_id)

        # 同步状态到数据库
        await self._sync_state_to_run(session, run, state)
        await session.commit()

        run = await run_repo.get_by_id(
            run_id
        )

        return await self._to_response(
            session,
            run,
            include_plan=True,
        )

    async def replan_analysis(
        self,
        session: AsyncSession,
        run_id: str,
        request: AnalysisReplanRequest,
    ) -> AnalysisResponse:
        """
        在设计闸门修改问题并重新规划。

        只允许在 WAITING_DESIGN 时调用：
        方案已经执行到一半再改问题没有意义，
        那些 Agent 的结果对应的是旧问题。
        """

        run_repo = AnalysisRunRepository(
            session
        )

        run = await run_repo.get_by_id(
            run_id
        )

        if run is None:
            raise ValidationError(
                f"Analysis run not found: {run_id}"
            )

        if run.status != "WAITING_DESIGN":
            raise ValidationError(
                f"Analysis run can only be replanned "
                f"at the design gate, current status: "
                f"{run.status}"
            )

        question = request.question.strip()

        if not question:
            raise ValidationError(
                "Question cannot be empty."
            )

        domain_service = self._get_domain_service(session)

        # 更新 run 表里的 question
        run.question = question
        await session.commit()

        state = await domain_service.replan_analysis(
            run_id=run_id,
            repository_id=run.repository_id,
            question=question,
        )

        # 同步状态到数据库
        await self._sync_state_to_run(session, run, state)
        await session.commit()

        run = await run_repo.get_by_id(
            run_id
        )

        # 重规划后停在同一个闸门，
        # 因此把新方案一并带回，前端可直接刷新显示。
        return await self._to_response(
            session,
            run,
            include_plan=True,
        )

    async def approve_analysis(
        self,
        session: AsyncSession,
        run_id: str,
    ) -> AnalysisResponse:
        """批准 Design Gate 或 Human Review。"""

        run_repo = AnalysisRunRepository(
            session
        )

        run = await run_repo.get_by_id(
            run_id
        )

        if run is None:
            raise ValidationError(
                f"Analysis run not found: {run_id}"
            )

        if run.status not in {
            "WAITING_DESIGN",
            "WAITING_HUMAN",
        }:
            raise ValidationError(
                f"Analysis run cannot be approved "
                f"from status: {run.status}"
            )

        # 使用 Domain Service 批准并恢复 Workflow
        domain_service = self._get_domain_service(session)

        state = await domain_service.approve_analysis(
            run_id=run_id,
            repository_id=run.repository_id,
        )

        # 同步 Workflow 状态到数据库
        await self._sync_state_to_run(session, run, state)
        await session.commit()

        run = await run_repo.get_by_id(
            run_id
        )

        return await self._to_response(
            session,
            run,
        )

    async def pause_analysis(
        self,
        session: AsyncSession,
        run_id: str,
    ) -> AnalysisResponse:
        """暂停 Workflow。"""

        run_repo = AnalysisRunRepository(
            session
        )

        run = await run_repo.get_by_id(
            run_id
        )

        if run is None:
            raise ValidationError(
                f"Analysis run not found: {run_id}"
            )

        if run.status not in {
            "ANALYZING",
            "WAITING_DESIGN",
            "WAITING_HUMAN",
        }:
            raise ValidationError(
                f"Analysis run cannot be paused "
                f"from status: {run.status}"
            )

        domain_service = self._get_domain_service(session)

        state = await domain_service.pause_analysis(run_id)

        # 同步状态到数据库
        await self._sync_state_to_run(session, run, state)
        await session.commit()

        run = await run_repo.get_by_id(
            run_id
        )

        return await self._to_response(
            session,
            run,
        )

    async def resume_analysis(
        self,
        session: AsyncSession,
        run_id: str,
    ) -> AnalysisResponse:
        """从 PAUSED Checkpoint 恢复。"""

        run_repo = AnalysisRunRepository(
            session
        )

        run = await run_repo.get_by_id(
            run_id
        )

        if run is None:
            raise ValidationError(
                f"Analysis run not found: {run_id}"
            )

        if run.status != "PAUSED":
            raise ValidationError(
                f"Analysis run cannot be resumed "
                f"from status: {run.status}"
            )

        domain_service = self._get_domain_service(session)

        state = await domain_service.resume_analysis(
            run_id=run_id,
            repository_id=run.repository_id,
        )

        # 同步状态到数据库
        await self._sync_state_to_run(session, run, state)
        await session.commit()

        run = await run_repo.get_by_id(
            run_id
        )

        return await self._to_response(
            session,
            run,
        )

    async def retry_analysis(
        self,
        session: AsyncSession,
        run_id: str,
    ) -> AnalysisResponse:
        """重新执行失败的 Workflow。"""

        run_repo = AnalysisRunRepository(
            session
        )

        run = await run_repo.get_by_id(
            run_id
        )

        if run is None:
            raise ValidationError(
                f"Analysis run not found: {run_id}"
            )

        if run.status != "FAILED":
            raise ValidationError(
                f"Analysis run cannot be retried "
                f"from status: {run.status}"
            )

        domain_service = self._get_domain_service(session)

        state = await domain_service.retry_analysis(
            run_id=run_id,
            repository_id=run.repository_id,
        )

        # 同步状态到数据库
        await self._sync_state_to_run(session, run, state)
        await session.commit()

        run = await run_repo.get_by_id(
            run_id
        )

        return await self._to_response(
            session,
            run,
        )

    async def learning_path(
        self,
        session: AsyncSession,
        run_id: str,
        goal: str | None = None,
    ) -> LearningPathResponse:
        """
        生成项目的学习路线（Phase 14.1）。

        只读不写：不修改原 run，
        产物是独立的一份 markdown。
        """

        run_repo = AnalysisRunRepository(
            session
        )

        run = await run_repo.get_by_id(run_id)

        if run is None:
            raise ValidationError(
                f"Analysis run not found: {run_id}"
            )

        domain_service = self._get_domain_service(session)

        # 加载 checkpoint 获取数据
        state = await domain_service.get_analysis_state(run_id)

        if state is None:
            raise ValidationError(f"Checkpoint not found: {run_id}")

        data = state.data or {}

        # 执行 learning_path skill
        result = await domain_service.execute_skill(
            run_id=run_id,
            repository_id=data.get("repository_id"),
            skill_name="learning_path",
            input_data={
                **data,
                "run_id": run_id,
                "goal": goal or data.get("question"),
            },
        )

        return LearningPathResponse(
            run_id=run_id,
            available=bool(
                result.get("available")
            ),
            reason=result.get("reason"),
            sections=result.get("sections") or {},
            report=result.get("report"),
            content=result.get("content") or "",
        )

    async def get_report_json(
        self,
        session: AsyncSession,
        run_id: str,
    ) -> AnalysisJsonReportResponse:
        """
        获取结构化报告（Phase 14.2）。

        两条路：

        1. 读 Finalizer 落盘的 .json（正常路径）
        2. 文件不在了就用 ReportService
           从 checkpoint 现场重建

        第 2 条不只是兜底：
        早期 run 没产出过 JSON，
        现场重建让它们也能拿到结构化报告。
        """

        run_repo = AnalysisRunRepository(
            session
        )

        run = await run_repo.get_by_id(run_id)

        if run is None:
            raise ValidationError(
                f"Analysis run not found: {run_id}"
            )

        domain_service = self._get_domain_service(session)

        # 加载 checkpoint
        state = await domain_service.get_analysis_state(run_id)

        data = state.data if state is not None else {}

        # 1. 尝试从磁盘读取 JSON 报告
        json_path = domain_service.get_json_report_path(run_id, data)

        if json_path:
            try:
                import json
                from pathlib import Path

                document = json.loads(Path(json_path).read_text(encoding="utf-8"))

                return AnalysisJsonReportResponse(
                    run_id=run_id,
                    status=run.status,
                    document=document,
                )
            except (OSError, ValueError):
                pass

        # 2. 从 checkpoint 现场重建
        if data:
            from app.services.report_service import ReportService

            document = ReportService.build_document(
                data,
                run_id=run_id,
            )

            return AnalysisJsonReportResponse(
                run_id=run_id,
                status=run.status,
                document=document,
            )

        return AnalysisJsonReportResponse(
            run_id=run_id,
            status=run.status,
            document=None,
        )

    async def get_report(
        self,
        session: AsyncSession,
        run_id: str,
    ) -> AnalysisReportResponse:
        """获取最终分析报告。"""

        run_repo = AnalysisRunRepository(
            session
        )

        run = await run_repo.get_by_id(
            run_id
        )

        if run is None:
            raise ValidationError(
                f"Analysis run not found: {run_id}"
            )

        domain_service = self._get_domain_service(session)

        # 加载 checkpoint
        state = await domain_service.get_analysis_state(run_id)

        report = None

        if state is not None:
            report = state.data.get("final_report")

        # 从磁盘读取报告内容
        report = domain_service.get_report_from_disk(run_id, report)

        return AnalysisReportResponse(
            run_id=run.id,
            status=run.status,
            report=report,
        )

    async def list_analyses(
        self,
        session: AsyncSession,
        limit: int = 20,
    ) -> list[AnalysisResponse]:
        """
        列出最近的分析任务。

        给前端的历史列表用：
        前端只能看到「当前这一个 run」时，
        关掉页面就找不回来了。
        """

        run_repo = AnalysisRunRepository(
            session
        )

        runs = await run_repo.list_recent(limit)

        if not runs:
            return []

        # 一次把所有关联仓库取回来，
        # 避免每个 run 查一次库。
        repository_ids = {
            run.repository_id
            for run in runs
        }

        result = await session.execute(
            select(Repository).where(
                Repository.id.in_(repository_ids)
            )
        )

        repositories = {
            repository.id: repository
            for repository in result.scalars().all()
        }

        responses = []

        for run in runs:

            repository = repositories.get(
                run.repository_id
            )

            responses.append(
                AnalysisResponse(
                    run_id=run.id,
                    status=run.status,
                    repo_url=(
                        repository.url
                        if repository is not None
                        else ""
                    ),
                    question=run.question,
                    current_node=run.current_node,
                    progress=self._progress(
                        run.status,
                        run.current_node,
                    ),
                    created_at=run.created_at,
                )
            )

        return responses

    async def deep_dive_module(
        self,
        session: AsyncSession,
        run_id: str,
        module: str,
    ) -> AnalysisDeepDiveResponse:
        """
        对某个已完成 run 的单个模块做深挖。

        默认报告每章只给要点；
        用户想看某个模块的实现细节时走这里。
        """

        run_repo = AnalysisRunRepository(
            session
        )

        run = await run_repo.get_by_id(
            run_id
        )

        if run is None:
            raise ValidationError(
                f"Analysis run not found: {run_id}"
            )

        normalized = (
            module or ""
        ).strip().lower()

        if normalized not in (
            ModuleDeepDiveSkill.MODULES
        ):
            raise ValidationError(
                f"Unsupported module: {module!r}. "
                "Expected one of "
                f"{', '.join(ModuleDeepDiveSkill.MODULES)}."
            )

        domain_service = self._get_domain_service(session)

        # 加载 checkpoint 获取数据
        state = await domain_service.get_analysis_state(run_id)

        if state is None:
            raise ValidationError(f"Checkpoint not found: {run_id}")

        data = state.data or {}

        # 执行 deep_dive skill
        result = await domain_service.execute_skill(
            run_id=run_id,
            repository_id=data.get("repository_id"),
            skill_name="module_deep_dive",
            input_data={
                **data,
                "run_id": run_id,
                "module": normalized,
            },
        )

        return AnalysisDeepDiveResponse(
            run_id=run_id,
            module=normalized,
            title=result.get("title"),
            report=result.get("report"),
            content=result.get("content"),
            files_read=result.get("files_read")
            or [],
            details=result.get("details", 0),
        )

    async def _to_response(
        self,
        session: AsyncSession,
        run,
        include_plan: bool = False,
    ) -> AnalysisResponse:
        """
        将 AnalysisRun 转成 API Response。

        include_plan：
            是否把分析方案一起带上。方案存在 checkpoint 的
            state_data 里，可能数百 KB，
            因此**默认不读** ——
            历史列表一次要出 30 条，逐条读大 JSON 会明显拖慢。

            只有单条查询（前端轮询当前 run）才需要它。
        """

        if run is None:
            raise ValidationError(
                "Analysis run not found."
            )

        repository = await session.get(
            Repository,
            run.repository_id,
        )

        if repository is None:
            raise ValidationError(
                f"Repository not found: "
                f"{run.repository_id}"
            )

        research_plan = None
        rag_enabled = None

        # 只在设计闸门等待审批时去读 checkpoint：
        # 那时用户确实需要看到方案才能决定批不批。
        if include_plan and run.status == "WAITING_DESIGN":

            try:
                state = await CheckpointRepository(
                    session
                ).get_latest(run.id)

            except Exception as error:  # noqa: BLE001
                # 读不到方案不该让状态查询整体失败 ——
                # 那样用户连"当前在等审批"都看不到。
                logger.warning(
                    "读取 research_plan 失败 | run=%s | %s",
                    run.id,
                    error,
                )
                state = None

            if state is not None:
                data = getattr(state, "data", None) or {}

                research_plan = data.get("research_plan")
                rag_enabled = data.get("rag_enabled")

        return AnalysisResponse(
            run_id=run.id,
            status=run.status,
            repo_url=repository.url,
            question=run.question,
            current_node=run.current_node,
            progress=self._progress(
                run.status,
                run.current_node,
            ),
            research_plan=research_plan,
            rag_enabled=rag_enabled,
            created_at=run.created_at,
        )

    @staticmethod
    def _progress(
        status: str,
        current_node: str | None,
    ) -> int:
        """计算第一版 Workflow 进度。"""

        if status == "COMPLETED":
            return 100

        if status == "FAILED":
            return 100

        mapping = {
            "start": 5,
            "planner_agent": 15,
            "design_gate": 20,
            "plan_executor": 70,
            "human_review": 85,
            "synthesis": 90,
            "finalizer": 95,
            "end": 100,
        }

        return mapping.get(
            current_node,
            0,
        )

    @staticmethod
    async def _sync_state_to_run(
        session: AsyncSession,
        run,
        state,
    ) -> None:
        """
        将 Workflow State 同步到 AnalysisRun 数据库记录。

        从 WorkflowState 中提取：
        - status（ANALYZING / COMPLETED / FAILED / WAITING_DESIGN 等）
        - current_node（当前执行到哪个节点）
        - error_message（失败时的错误信息）

        然后更新 AnalysisRun 表。
        """
        if state is None:
            return

        # 映射 Workflow 状态到 AnalysisRun 状态
        status_mapping = {
            "CREATED": "ANALYZING",
            "PLANNING": "ANALYZING",
            "ANALYZING": "ANALYZING",
            "RETRYING": "ANALYZING",
            "COMPLETED": "COMPLETED",
            "FAILED": "FAILED",
            "PAUSED": "PAUSED",
            "CANCELED": "CANCELED",
            "WAITING_DESIGN": "WAITING_DESIGN",
            "WAITING_HUMAN": "WAITING_HUMAN",
        }

        workflow_status = getattr(state, "status", "ANALYZING")
        run.status = status_mapping.get(workflow_status, "ANALYZING")

        # 同步当前节点
        current_node = getattr(state, "current_node", None)
        if current_node:
            run.current_node = current_node

        # 同步错误信息
        if workflow_status == "failed":
            data = getattr(state, "data", {}) or {}
            run.error_message = data.get("error_message")

        await session.flush()

    @staticmethod
    def _parse_github_url(
        repo_url: str,
    ) -> tuple[str, str]:
        """
        解析 GitHub owner/repository。

        复用 app.tools.github.parser.parse_github_url：
        它基于 urlparse，会正确剥离 query string 与 fragment。

        旧实现直接按 "/" 切分字符串，因此

            https://github.com/owner/name?utm_source=chatgpt.com

        会被解析成

            name = "name?utm_source=chatgpt.com"

        后果是一整条连锁失败：

            repository.name 被污染
                → README / 配置文件全部 404
                → readme 为空
                → evidences 为 0
                → technology_stack 全空
                → 报告多个章节「真实数据不存在」

        而且该 run 仍然会被标记为 COMPLETED，
        继续参与 Phase 13 的多项目比较。
        """

        try:

            return parse_github_url(repo_url)

        except ValueError as error:

            raise ValidationError(
                "Invalid GitHub repository URL."
            ) from error


analysis_service = AnalysisService()