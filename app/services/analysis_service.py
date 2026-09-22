"""Analysis Service：负责创建、查询和管理项目分析任务。"""

from datetime import datetime, timezone
from uuid import uuid4

from app.core.exceptions import ValidationError
from app.core.logging import get_logger, log_with_run_id
from app.schemas.analysis import (
    AnalysisCreateRequest,
    AnalysisResponse,
)


logger = get_logger(__name__)


class AnalysisService:
    """负责分析任务的创建、查询和基础状态管理。"""

    def __init__(self) -> None:
        # 当前阶段先使用内存保存任务，
        # Phase 2 接入 MySQL 后会替换成 Repository。
        self._runs: dict[str, AnalysisResponse] = {}

    def create_analysis(
        self,
        request: AnalysisCreateRequest,
    ) -> AnalysisResponse:
        """创建一个新的项目分析任务。"""

        repo_url = request.repo_url.strip()

        # 当前项目的分析入口是 GitHub Repository。
        # 后续可以扩展 GitLab、Gitee 等代码仓库来源。
        if not repo_url:
            raise ValidationError(
                "Repository URL cannot be empty."
            )

        if not repo_url.startswith(
            ("https://github.com/", "http://github.com/")
        ):
            raise ValidationError(
                "Only GitHub repository URLs are supported."
            )

        # 每一次分析都生成独立 run_id，
        # 后续日志、Workflow、Agent 和 Checkpoint 都可以通过它关联。
        run_id = str(uuid4())

        result = AnalysisResponse(
            run_id=run_id,
            status="pending",
            repo_url=repo_url,
            created_at=datetime.now(timezone.utc),
        )

        self._runs[run_id] = result

        log_with_run_id(
            logger,
            level=20,
            message="analysis task created",
            run_id=run_id,
        )

        return result

    def get_analysis(
        self,
        run_id: str,
    ) -> AnalysisResponse:
        """根据 run_id 查询分析任务。"""

        result = self._runs.get(run_id)

        if result is None:
            raise ValidationError(
                f"Analysis run not found: {run_id}"
            )

        log_with_run_id(
            logger,
            level=20,
            message="analysis task queried",
            run_id=run_id,
        )

        return result


# 当前使用单例 Service，保证 API 请求共享任务状态。
# 后续接入依赖注入和数据库后可以进一步调整。
analysis_service = AnalysisService()