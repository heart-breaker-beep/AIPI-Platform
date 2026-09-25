"""Analysis 任务业务逻辑。"""

from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ValidationError
from app.core.logging import get_logger, log_with_run_id
from app.repositories.analysis_run import (
    AnalysisRunRepository,
)
from app.repositories.repository_basic import (
    RepositoryRepository,
)
from app.schemas.analysis import (
    AnalysisCreateRequest,
    AnalysisResponse,
)
from app.models.repository import Repository


logger = get_logger(__name__)


class AnalysisService:
    """负责 Analysis 任务的业务编排。"""

    async def create_analysis(
        self,
        session: AsyncSession,
        request: AnalysisCreateRequest,
    ) -> AnalysisResponse:
        """创建 Repository 和 Analysis Run。"""

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

        repository_repo = RepositoryRepository(
            session
        )

        analysis_run_repo = AnalysisRunRepository(
            session
        )

        repository = await repository_repo.get_by_url(
            repo_url
        )

        if repository is None:
            repository = await repository_repo.create(
                url=repo_url,
                owner=owner,
                name=name,
            )

        run_id = str(uuid4())

        # Phase 11：
        # 将用户问题真正保存到 AnalysisRun。
        run = await analysis_run_repo.create(
            run_id=run_id,
            repository_id=repository.id,
            question=request.question,
        )

        await session.commit()

        log_with_run_id(
            logger,
            level=20,
            message="analysis task created",
            run_id=run_id,
        )

        return AnalysisResponse(
            run_id=run.id,
            status=run.status,
            repo_url=repository.url,
            created_at=run.created_at,
        )

    async def get_analysis(
        self,
        session: AsyncSession,
        run_id: str,
    ) -> AnalysisResponse:
        """根据 run_id 查询分析任务。"""

        repository_run = AnalysisRunRepository(
            session
        )

        run = await repository_run.get_by_id(
            run_id
        )

        if run is None:
            raise ValidationError(
                f"Analysis run not found: {run_id}"
            )

        repository_repo = RepositoryRepository(
            session
        )

        repository = await session.get(
            Repository,
            run.repository_id,
        )

        if repository is None:
            raise ValidationError(
                f"Repository not found: {run.repository_id}"
            )

        return AnalysisResponse(
            run_id=run.id,
            status=run.status,
            repo_url=repository.url,
            created_at=run.created_at,
        )

    @staticmethod
    def _parse_github_url(
        repo_url: str,
    ) -> tuple[str, str]:
        """解析 GitHub owner 和 repository name。"""

        path = repo_url.rstrip("/").split("/")

        if len(path) < 2:
            raise ValidationError(
                "Invalid GitHub repository URL."
            )

        owner = path[-2]
        name = path[-1]

        if not owner or not name:
            raise ValidationError(
                "Invalid GitHub repository URL."
            )

        return owner, name

    async def approve_analysis(
        self,
        session: AsyncSession,
        run_id: str,
    ) -> AnalysisResponse:
        """通过 Design Gate。"""

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
            "pending",
            "WAITING_DESIGN",
            "WAITING_DESIGN_APPROVAL",
        }:
            raise ValidationError(
                f"Analysis run cannot be approved "
                f"from status: {run.status}"
            )

        await run_repo.update_runtime_state(
            run,
            status="ANALYZING",
        )

        await session.commit()

        repository = await session.get(
            Repository,
            run.repository_id,
        )

        if repository is None:
            raise ValidationError(
                f"Repository not found: {run.repository_id}"
            )

        return AnalysisResponse(
            run_id=run.id,
            status=run.status,
            repo_url=repository.url,
            created_at=run.created_at,
        )

    async def pause_analysis(
        self,
        session: AsyncSession,
        run_id: str,
    ) -> AnalysisResponse:
        """人工暂停 Analysis Run。"""

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

        if run.status != "ANALYZING":
            raise ValidationError(
                f"Analysis run cannot be paused "
                f"from status: {run.status}"
            )

        await run_repo.update_runtime_state(
            run,
            status="PAUSED",
        )

        await session.commit()

        repository = await session.get(
            Repository,
            run.repository_id,
        )

        if repository is None:
            raise ValidationError(
                f"Repository not found: {run.repository_id}"
            )

        return AnalysisResponse(
            run_id=run.id,
            status=run.status,
            repo_url=repository.url,
            created_at=run.created_at,
        )

    async def resume_analysis(
        self,
        session: AsyncSession,
        run_id: str,
    ) -> AnalysisResponse:
        """从 Checkpoint 恢复 Analysis Run。"""

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
            "PAUSED",
            "WAITING_HUMAN",
        }:
            raise ValidationError(
                f"Analysis run cannot be resumed "
                f"from status: {run.status}"
            )

        await run_repo.update_runtime_state(
            run,
            status="ANALYZING",
        )

        await session.commit()

        repository = await session.get(
            Repository,
            run.repository_id,
        )

        if repository is None:
            raise ValidationError(
                f"Repository not found: {run.repository_id}"
            )

        return AnalysisResponse(
            run_id=run.id,
            status=run.status,
            repo_url=repository.url,
            created_at=run.created_at,
        )

    async def retry_analysis(
        self,
        session: AsyncSession,
        run_id: str,
    ) -> AnalysisResponse:
        """重新执行失败的 Analysis Run。"""

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

        await run_repo.update_runtime_state(
            run,
            status="RETRYING",
            retry_count=run.retry_count + 1,
        )

        await session.commit()

        repository = await session.get(
            Repository,
            run.repository_id,
        )

        if repository is None:
            raise ValidationError(
                f"Repository not found: {run.repository_id}"
            )

        return AnalysisResponse(
            run_id=run.id,
            status=run.status,
            repo_url=repository.url,
            created_at=run.created_at,
        )


analysis_service = AnalysisService()