"""
Analysis Workflow Orchestrator - 分析任务编排（领域层）。

职责：
- 管理 Workflow 生命周期（start, approve, resume, retry, cancel）
- 编排业务流程
- 不依赖具体技术实现（通过接口注入）

依赖倒置：
- WorkflowEngine: 注入（来自 Infrastructure）
- WorkflowContextFactory: 注入（来自 Infrastructure）
- CheckpointManager: 注入（来自 Infrastructure）
"""

from pathlib import Path

from app.core.logging import get_logger
from app.infrastructure.workflow.state import WorkflowState

logger = get_logger(__name__)


class AnalysisWorkflowOrchestrator:
    """
    分析 Workflow 编排器（领域层）。

    核心原则：
    - 只管业务编排，不管技术细节
    - 通过接口依赖技术实现（依赖倒置）
    - 无状态服务（状态由 WorkflowState 承载）
    """

    def __init__(
        self,
        engine,  # WorkflowEngine（来自 infrastructure）
        context_factory,  # WorkflowContextFactory（来自 infrastructure）
        checkpoint_manager,  # CheckpointManager（来自 infrastructure）
        workflow_builder,  # build_analysis_workflow（来自 infrastructure）
    ):
        """
        Args:
            engine: Workflow 执行引擎
            context_factory: 用于创建 WorkflowContext 的工厂
            checkpoint_manager: 用于保存/加载 Checkpoint
            workflow_builder: 用于构建 Workflow 定义的函数
        """
        self.engine = engine
        self.context_factory = context_factory
        self.checkpoint_manager = checkpoint_manager
        self.workflow_builder = workflow_builder

    async def start_workflow(
        self,
        run_id: str,
        repository_id: int,
        initial_data: dict,
    ):
        """
        启动新的分析 Workflow。

        Args:
            run_id: Analysis Run ID
            repository_id: Repository ID
            initial_data: 初始数据（repo_url, owner, repo, question 等）

        Returns:
            WorkflowState
        """
        # 1. 创建 Context
        context = self.context_factory.create(repository_id)

        # 2. 创建初始状态
        state = WorkflowState(run_id=run_id)
        state.data = initial_data

        # 3. 构建 Workflow 定义
        workflow = self.workflow_builder(context)

        # 4. 执行 Workflow
        result = await self.engine.run(workflow, state, context)

        return result

    async def approve_workflow(
        self,
        run_id: str,
        repository_id: int,
        identity: dict | None = None,
    ):
        """
        批准 Design Gate 或 Human Review。

        Args:
            run_id: Analysis Run ID
            repository_id: Repository ID
            identity: 身份字段（run_id / repo_url / owner / repo 等），
                用于补齐早期版本留下的缺字段 checkpoint

        Returns:
            WorkflowState
        """
        # 1. 加载 Checkpoint
        state = await self.checkpoint_manager.load(run_id)

        if state is None:
            raise ValueError(f"Checkpoint not found: {run_id}")

        self._apply_identity(state, identity)

        # 2. 标记批准并保存（包含补齐的身份字段）
        state.approve()
        await self.checkpoint_manager.save(state)

        # 3. 创建 Context
        context = self.context_factory.create(repository_id)

        # 4. 重建 Workflow
        workflow = self.workflow_builder(context)

        # 5. 恢复执行
        result = await self.engine.resume(workflow, context, run_id)

        return result

    @staticmethod
    def _apply_identity(state, identity: dict | None) -> bool:
        """
        把身份字段补回 state.data。

        为什么需要：早期版本的 checkpoint 里缺 owner / repo / run_id，
        这些字段一旦缺失，repository_analysis_skill 拿不到仓库坐标，
        恢复或重试就会原地再失败一次。

        身份字段由 Application 层从 Repository 行构造，
        不在这里从 repo_url 反解 ——
        数据库里的 owner / name 才是权威来源，
        反解只是在猜。

        Returns:
            是否真的补写了字段（调用方据此决定要不要落盘）
        """

        if not identity:
            return False

        changed = False

        for key, value in identity.items():

            if value is None:
                continue

            if state.data.get(key) == value:
                continue

            state.data[key] = value
            changed = True

        return changed

    async def pause_workflow(self, run_id: str):
        """
        人工暂停 Workflow。

        Args:
            run_id: Analysis Run ID

        Returns:
            WorkflowState
        """
        state = await self.checkpoint_manager.load(run_id)

        if state is None:
            raise ValueError(f"Checkpoint not found: {run_id}")

        result = await self.engine.pause(state)

        return result

    async def resume_workflow(
        self,
        run_id: str,
        repository_id: int,
        identity: dict | None = None,
    ):
        """
        从 PAUSED Checkpoint 恢复。

        Args:
            run_id: Analysis Run ID
            repository_id: Repository ID
            identity: 身份字段，用于补齐缺字段的旧 checkpoint

        Returns:
            WorkflowState
        """
        # 加载 Checkpoint
        state = await self.checkpoint_manager.load(run_id)

        if state is None:
            raise ValueError(f"Checkpoint not found: {run_id}")

        if self._apply_identity(state, identity):
            # 必须落盘：engine.resume 会重新从 checkpoint 加载 state，
            # 只改内存里的这一份等于没改。
            await self.checkpoint_manager.save(state)

        # 创建 Context
        context = self.context_factory.create(repository_id)

        # 重建 Workflow
        workflow = self.workflow_builder(context)

        # 恢复执行
        result = await self.engine.resume(workflow, context, run_id)

        return result

    async def retry_workflow(
        self,
        run_id: str,
        repository_id: int,
        identity: dict | None = None,
    ):
        """
        重新执行失败的 Workflow。

        Args:
            run_id: Analysis Run ID
            repository_id: Repository ID
            identity: 身份字段，用于补齐缺字段的旧 checkpoint

        Returns:
            WorkflowState
        """
        # 加载 Checkpoint
        state = await self.checkpoint_manager.load(run_id)

        if state is None:
            raise ValueError(f"Checkpoint not found: {run_id}")

        if self._apply_identity(state, identity):
            # 必须落盘：engine.retry 会重新从 checkpoint 加载 state。
            await self.checkpoint_manager.save(state)

        # 创建 Context
        context = self.context_factory.create(repository_id)

        # 重建 Workflow
        workflow = self.workflow_builder(context)

        # 重试
        result = await self.engine.retry(workflow, context, run_id)

        return result

    async def cancel_workflow(self, run_id: str):
        """
        人工取消 Workflow。

        只置状态，不删数据 ——
        报告文件、已落库的 evidence 都保留，
        用户之后仍能在历史里查看这个 run 走到过哪一步。

        Args:
            run_id: Analysis Run ID

        Returns:
            WorkflowState
        """
        state = await self.checkpoint_manager.load(run_id)

        if state is None:
            raise ValueError(f"Checkpoint not found: {run_id}")

        result = await self.engine.cancel(state)

        return result

    async def replan_workflow(
        self,
        run_id: str,
        repository_id: int,
        question: str,
    ):
        """
        改问题后重新规划。

        Args:
            run_id: Analysis Run ID
            repository_id: Repository ID
            question: 新的分析问题

        Returns:
            WorkflowState
        """
        # 加载 Checkpoint
        state = await self.checkpoint_manager.load(run_id)

        if state is None:
            raise ValueError(f"Checkpoint not found: {run_id}")

        # 重新规划
        state.replan(question)

        # 创建 Context
        context = self.context_factory.create(repository_id)

        # 重建 Workflow
        workflow = self.workflow_builder(context)

        # 重新执行
        result = await self.engine.run(workflow, state, context)

        return result

    async def execute_skill(
        self,
        run_id: str,
        repository_id: int,
        skill_name: str,
        input_data: dict,
    ):
        """
        执行独立的 Skill（用于 deep_dive, learning_path 等场景）。

        不修改 Workflow 状态，只返回 Skill 的执行结果。

        Args:
            run_id: Analysis Run ID
            repository_id: Repository ID
            skill_name: Skill 名称
            input_data: Skill 的输入数据

        Returns:
            Skill 的执行结果
        """
        # 创建 Context
        context = self.context_factory.create(repository_id)

        # 获取 Skill
        skill = context.skills.get(skill_name)

        if skill is None:
            raise ValueError(f"Skill not found: {skill_name}")

        # 执行 Skill
        return await skill.execute(context, input_data)

    async def get_checkpoint(self, run_id: str):
        """
        获取 Checkpoint（用于读取 state.data）。

        Args:
            run_id: Analysis Run ID

        Returns:
            WorkflowState 或 None
        """
        try:
            return await self.checkpoint_manager.load(run_id)
        except Exception as error:
            logger.warning(
                "checkpoint load failed | run_id=%s | %s: %s",
                run_id,
                type(error).__name__,
                error,
            )
            return None

    @staticmethod
    def get_report_from_disk(run_id: str, report: dict | None) -> dict | None:
        """
        用磁盘上的报告文件补齐 report。

        两种情况都走这里：
        - report 完全没有（checkpoint 读不出来）
        - report 有路径但没有正文（state 瘦身时丢掉了 content）

        Args:
            run_id: Analysis Run ID
            report: 从 state.data 读到的 final_report

        Returns:
            补齐后的 report
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

        candidates.append(directory / f"{run_id}_analysis.md")

        for candidate in candidates:
            if not candidate.is_file():
                continue

            try:
                content = candidate.read_text(encoding="utf-8")
            except OSError:
                continue

            # 如果已经有 content 就不覆盖
            if isinstance(report, dict) and report.get("content"):
                return report

            return {
                "report": {
                    "path": str(candidate),
                    "format": "markdown",
                },
                "content": content,
            }

        return report

    @staticmethod
    def get_json_report_path(run_id: str, data: dict) -> str | None:
        """
        找出 JSON 报告文件路径。

        Args:
            run_id: Analysis Run ID
            data: state.data

        Returns:
            JSON 报告文件路径或 None
        """
        final_report = data.get("final_report") if isinstance(data, dict) else None

        if isinstance(final_report, dict):
            json_report = final_report.get("json_report")

            if isinstance(json_report, dict):
                candidate = json_report.get("path")

                if candidate and Path(candidate).is_file():
                    return candidate

        # 早期 run 没记录路径，按命名约定猜一下
        fallback = Path("reports") / f"{run_id}_analysis.json"

        if fallback.is_file():
            return str(fallback)

        return None
