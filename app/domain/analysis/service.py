"""
Analysis Domain Service - 分析任务领域服务。

职责：
- 业务编排（调度 Workflow 执行）
- 业务规则校验
- 状态管理
- 不涉及技术细节（数据库、HTTP 由外层处理）

依赖倒置：
- 通过接口依赖 Infrastructure 层实现
- 不直接操作数据库（通过 Repository 接口）
"""

from app.core.logging import get_logger

logger = get_logger(__name__)


class AnalysisService:
    """
    分析任务领域服务。

    核心原则：
    - 只管业务编排，不管技术细节
    - 通过接口依赖技术实现（依赖倒置）
    - 无状态服务（状态由 WorkflowState 承载）
    """

    def __init__(
        self,
        workflow_orchestrator,  # AnalysisWorkflowOrchestrator（来自 domain）
        run_repository,  # AnalysisRunRepository（来自 infrastructure）
        checkpoint_repository,  # CheckpointRepository（来自 infrastructure）
    ):
        """
        Args:
            workflow_orchestrator: Workflow 编排器
            run_repository: 分析任务数据仓库
            checkpoint_repository: Checkpoint 数据仓库
        """
        self.orchestrator = workflow_orchestrator
        self.run_repo = run_repository
        self.checkpoint_repo = checkpoint_repository

    async def start_analysis(
        self,
        run_id: str,
        repository_id: int,
        initial_data: dict,
    ):
        """
        启动分析任务。

        initial_data 原样往下传，不在这里重新组装。

        由来：之前本层自己拼了一份 initial_data，于是同一份数据
        在 Application 层和这里各存在一份，字段很快就对不上了 ——
        run_id / owner / repo 丢了，rag_enabled 还被写成 enable_rag，
        导致 RAG 按次开关失效、首次 run 拿不到仓库坐标。
        唯一一份由 Application 层组装。

        Args:
            run_id: Analysis Run ID
            repository_id: Repository ID
            initial_data: 初始业务数据

        Returns:
            WorkflowState
        """
        # 委托 Workflow Orchestrator 执行
        state = await self.orchestrator.start_workflow(
            run_id=run_id,
            repository_id=repository_id,
            initial_data=initial_data,
        )

        # 注意：状态同步由 Application Service 负责
        # Domain Service 只返回 state
        return state

    async def approve_analysis(
        self,
        run_id: str,
        repository_id: int,
        identity: dict | None = None,
    ):
        """
        批准设计闸门或人工审核。

        Args:
            run_id: Analysis Run ID
            repository_id: Repository ID
            identity: 身份字段，用于补齐缺字段的旧 checkpoint

        Returns:
            WorkflowState
        """
        # 委托 Workflow Orchestrator 执行
        state = await self.orchestrator.approve_workflow(
            run_id=run_id,
            repository_id=repository_id,
            identity=identity,
        )

        return state

    async def pause_analysis(self, run_id: str):
        """
        暂停分析任务。

        Args:
            run_id: Analysis Run ID

        Returns:
            WorkflowState
        """
        state = await self.orchestrator.pause_workflow(run_id)

        return state

    async def resume_analysis(
        self,
        run_id: str,
        repository_id: int,
        identity: dict | None = None,
    ):
        """
        恢复分析任务。

        Args:
            run_id: Analysis Run ID
            repository_id: Repository ID
            identity: 身份字段，用于补齐缺字段的旧 checkpoint

        Returns:
            WorkflowState
        """
        state = await self.orchestrator.resume_workflow(
            run_id=run_id,
            repository_id=repository_id,
            identity=identity,
        )

        return state

    async def retry_analysis(
        self,
        run_id: str,
        repository_id: int,
        identity: dict | None = None,
    ):
        """
        重试失败的分析任务。

        Args:
            run_id: Analysis Run ID
            repository_id: Repository ID
            identity: 身份字段，用于补齐缺字段的旧 checkpoint

        Returns:
            WorkflowState
        """
        state = await self.orchestrator.retry_workflow(
            run_id=run_id,
            repository_id=repository_id,
            identity=identity,
        )

        return state

    async def cancel_analysis(self, run_id: str):
        """
        取消分析任务。

        Args:
            run_id: Analysis Run ID

        Returns:
            WorkflowState
        """
        state = await self.orchestrator.cancel_workflow(run_id)

        return state

    async def replan_analysis(
        self,
        run_id: str,
        repository_id: int,
        question: str,
    ):
        """
        重新规划分析任务。

        Args:
            run_id: Analysis Run ID
            repository_id: Repository ID
            question: 新的分析问题

        Returns:
            WorkflowState
        """
        state = await self.orchestrator.replan_workflow(
            run_id=run_id,
            repository_id=repository_id,
            question=question,
        )

        return state

    async def execute_skill(
        self,
        run_id: str,
        repository_id: int,
        skill_name: str,
        input_data: dict,
    ):
        """
        执行独立的 Skill。

        Args:
            run_id: Analysis Run ID
            repository_id: Repository ID
            skill_name: Skill 名称
            input_data: Skill 输入数据

        Returns:
            Skill 执行结果
        """
        return await self.orchestrator.execute_skill(
            run_id=run_id,
            repository_id=repository_id,
            skill_name=skill_name,
            input_data=input_data,
        )

    async def get_analysis_state(self, run_id: str):
        """
        获取分析任务状态。

        Args:
            run_id: Analysis Run ID

        Returns:
            WorkflowState 或 None
        """
        return await self.orchestrator.get_checkpoint(run_id)

    def get_report_from_disk(self, run_id: str, report: dict | None) -> dict | None:
        """
        从磁盘读取报告。

        Args:
            run_id: Analysis Run ID
            report: 从 state.data 读到的 final_report

        Returns:
            补齐后的 report
        """
        return self.orchestrator.get_report_from_disk(run_id, report)

    def get_json_report_path(self, run_id: str, data: dict) -> str | None:
        """
        获取 JSON 报告路径。

        Args:
            run_id: Analysis Run ID
            data: state.data

        Returns:
            JSON 报告文件路径或 None
        """
        return self.orchestrator.get_json_report_path(run_id, data)
