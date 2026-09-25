"""Research Run Memory。"""

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.analysis_run import AnalysisRun
from app.models.analysis_task import AnalysisTask
from app.repositories.checkpoint import CheckpointRepository
from app.repositories.evidence import EvidenceRepository


class RunMemory:
    """
    读取一次 Analysis Run 的短期 / 情景记忆。

    Phase 11 不新增 Memory 专用表，
    而是复用已经存在的：

    analysis_runs
    analysis_tasks
    checkpoints
    evidences
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

        self.checkpoint_repository = (
            CheckpointRepository(session)
        )

        self.evidence_repository = (
            EvidenceRepository(session)
        )

    async def load(
        self,
        run_id: str,
    ) -> dict[str, Any] | None:
        """加载一次 Run 的完整记忆快照。"""

        result = await self.session.execute(
            select(AnalysisRun).where(
                AnalysisRun.id == run_id
            )
        )

        run = result.scalar_one_or_none()

        if run is None:
            return None

        repository = await self.session.get(
            __import__(
                "app.models.repository",
                fromlist=["Repository"],
            ).Repository,
            run.repository_id,
        )

        task_result = await self.session.execute(
            select(AnalysisTask)
            .where(
                AnalysisTask.run_id == run_id
            )
            .order_by(
                AnalysisTask.created_at
            )
        )

        tasks = list(
            task_result.scalars().all()
        )

        checkpoint = (
            await self.checkpoint_repository.get_latest(
                run_id
            )
        )

        evidences = []

        if repository is not None:
            evidences = (
                await self.evidence_repository
                .list_by_repository(
                    repository.id
                )
            )

        checkpoint_data = (
            checkpoint.data
            if checkpoint
            else {}
        )

        return {
            # 当前 Run
            "run_id": run.id,
            "question": run.question,
            "status": run.status,
            "current_node": run.current_node,

            # Repository
            "repository": (
                {
                    "id": repository.id,
                    "url": repository.url,
                    "owner": repository.owner,
                    "name": repository.name,
                    "description": repository.description,
                    "language": repository.language,
                }
                if repository is not None
                else None
            ),

            # Research Plan
            "research_plan": (
                checkpoint_data.get(
                    "research_plan"
                )
            ),

            # Phase 14/12 可以继续使用
            # 这里提前预留最终报告。
            "final_report": (
                checkpoint_data.get(
                    "final_report"
                )
            ),

            # Agent 输出
            "agent_outputs": (
                checkpoint.outputs
                if checkpoint
                else []
            ),

            # Task 结果
            "task_results": [
                {
                    "id": task.id,
                    "task_type": task.task_type,
                    "status": task.status,
                    "input": task.input,
                    "output": task.output,
                    "error": task.error,
                    "retry_count": task.retry_count,
                }
                for task in tasks
            ],

            # Evidence
            #
            # 第一版只保留最近 20 条，
            # 避免 Context 无限膨胀。
            "evidences": [
                {
                    "id": evidence.id,
                    "source_type": (
                        evidence.source_type
                    ),
                    "file_path": (
                        evidence.file_path
                    ),
                    "line_start": (
                        evidence.line_start
                    ),
                    "line_end": (
                        evidence.line_end
                    ),
                    "content": evidence.content,
                    "verification_status": (
                        evidence.verification_status
                    ),
                }
                for evidence in evidences[-20:]
            ],

            # Workflow Checkpoint
            "workflow_state": (
                {
                    "status": checkpoint.status,
                    "current_node": (
                        checkpoint.current_node
                    ),
                    "data": checkpoint.data,
                    "errors": checkpoint.errors,
                    "retry_count": (
                        checkpoint.retry_count
                    ),
                    "pause_reason": (
                        checkpoint.pause_reason
                    ),
                    "human_approved": (
                        checkpoint.human_approved
                    ),
                    "checkpoint_version": (
                        checkpoint.checkpoint_version
                    ),
                }
                if checkpoint is not None
                else None
            ),
        }