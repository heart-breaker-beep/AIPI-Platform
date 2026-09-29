"""
多项目比较业务服务。

职责：

API
 ↓
ComparisonService
 ↓
AnalysisRun / RunMemory
 ↓
ComparisonAgent
"""
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.comparison_agent import (
    ComparisonAgent,
)
from app.core.exceptions import ValidationError
from app.memory.run_memory import RunMemory
from app.repositories.analysis_run import (
    AnalysisRunRepository,
)
from app.schemas.comparison import (
    ComparisonCreateRequest,
    ComparisonProjectResponse,
    ComparisonResponse,
)


class ComparisonService:
    """负责多项目分析结果比较。"""

    comparison_agent_factory = (
        ComparisonAgent
    )

    async def create_comparison(
        self,
        session: AsyncSession,
        request: ComparisonCreateRequest,
    ) -> ComparisonResponse:
        """比较两个已经完成的 Analysis Run。"""

        run_ids = [
            run_id.strip()
            for run_id in request.run_ids
        ]

        if len(run_ids) != 2:
            raise ValidationError(
                "Exactly two analysis run IDs "
                "are required."
            )

        if run_ids[0] == run_ids[1]:
            raise ValidationError(
                "The two analysis runs "
                "must be different."
            )

        run_repository = (
            AnalysisRunRepository(
                session
            )
        )

        runs = []

        for run_id in run_ids:
            run = await (
                run_repository.get_by_id(
                    run_id
                )
            )

            if run is None:
                raise ValidationError(
                    f"Analysis run not found: "
                    f"{run_id}"
                )

            if run.status != "COMPLETED":
                raise ValidationError(
                    "Only completed analysis runs "
                    "can be compared: "
                    f"{run_id} "
                    f"has status {run.status}."
                )

            runs.append(run)

        if (
            runs[0].repository_id
            == runs[1].repository_id
        ):
            raise ValidationError(
                "The two analysis runs "
                "must belong to different repositories."
            )

        memory = RunMemory(
            session
        )

        project_a = await memory.load(
            runs[0].id
        )

        project_b = await memory.load(
            runs[1].id
        )

        if project_a is None:
            raise ValidationError(
                f"Analysis memory not found: "
                f"{runs[0].id}"
            )

        if project_b is None:
            raise ValidationError(
                f"Analysis memory not found: "
                f"{runs[1].id}"
            )

        agent = (
            self.comparison_agent_factory(
                skill_registry=None
            )
        )

        result = await agent.execute(
            context=None,
            input_data={
                "project_a": project_a,
                "project_b": project_b,
            },
        )

        projects = [
            ComparisonProjectResponse(
                run_id=project.get(
                    "run_id"
                ),
                repository_id=project.get(
                    "repository_id"
                ),
                repository_url=project.get(
                    "repository_url"
                ),
                repository_name=project.get(
                    "repository_name"
                ),
                status=project.get(
                    "status"
                ),
            )
            for project in result.get(
                "projects",
                [],
            )
        ]

        return ComparisonResponse(
            comparison_id=str(
                uuid4()
            ),
            status="COMPLETED",
            evidence_based=bool(
                result.get(
                    "evidence_based",
                    False,
                )
            ),
            projects=projects,
            comparison=result.get(
                "comparison",
                {},
            ),
        )


comparison_service = ComparisonService()