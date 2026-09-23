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

        run = await analysis_run_repo.create(
            run_id=run_id,
            repository_id=repository.id,
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

        # 当前先根据 repository_id 查询项目。
        repository = await session.get(
            __import__(
                "app.models.repository",
                fromlist=["Repository"],
            ).Repository,
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


analysis_service = AnalysisService()