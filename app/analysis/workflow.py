"""项目分析流程定义与生命周期执行协调。"""

from app.analysis.nodes.agent_node import AgentNode
from app.analysis.nodes.design_gate_node import (
    DesignGateNode,
)
from app.analysis.nodes.end_node import EndNode
from app.analysis.nodes.finalizer_node import (
    FinalizerNode,
)
from app.analysis.nodes.human_node import HumanNode
from app.analysis.nodes.plan_executor_node import (
    PlanExecutorNode,
)
from app.analysis.nodes.start_node import StartNode
from app.analysis.nodes.synthesis_node import (
    SynthesisNode,
)
from app.core.logging import get_logger
from app.workflow.state import WorkflowStatus
from app.workflow.transition import Transition
from app.workflow.workflow import Workflow


def build_analysis_workflow(
    context,
) -> Workflow:
    """
    创建单项目完整分析 Workflow。

    Agent 的具体实例来自 WorkflowContext，
    Workflow 本身不负责创建 Agent。
    """

    workflow = Workflow()

    planner = context.agents.get("planner_agent")

    if planner is None:
        raise ValueError("Planner Agent is not registered.")

    report_skill = context.skills.get("report_generation")

    if report_skill is None:
        raise ValueError("Report generation skill is not registered.")

    synthesis_skill = context.skills.get("report_synthesis")

    if synthesis_skill is None:
        raise ValueError("Report synthesis skill is not registered.")

    workflow.add_node(StartNode())

    workflow.add_node(
        AgentNode(
            name="planner_agent",
            agent=planner,
        )
    )

    workflow.add_node(DesignGateNode())

    workflow.add_node(PlanExecutorNode())

    workflow.add_node(HumanNode())

    workflow.add_node(
        SynthesisNode(
            skill=synthesis_skill,
        )
    )

    workflow.add_node(
        FinalizerNode(
            skill=report_skill,
        )
    )

    workflow.add_node(EndNode())

    workflow.add_transition(
        Transition(
            "start",
            "planner_agent",
        )
    )

    workflow.add_transition(
        Transition(
            "planner_agent",
            "design_gate",
        )
    )

    workflow.add_transition(
        Transition(
            "design_gate",
            "plan_executor",
        )
    )

    workflow.add_transition(
        Transition(
            "plan_executor",
            "human_review",
        )
    )

    workflow.add_transition(
        Transition(
            "human_review",
            "synthesis",
        )
    )

    workflow.add_transition(
        Transition(
            "synthesis",
            "finalizer",
        )
    )

    workflow.add_transition(
        Transition(
            "finalizer",
            "end",
        )
    )

    return workflow


logger = get_logger(__name__)


class AnalysisWorkflowOrchestrator:
    """
    分析 Workflow 编排器（分析业务执行组件）。

    核心原则：
    - 只管业务编排，不管技术细节
    - 通过接口依赖技术实现（依赖倒置）
    - 无状态服务（状态由 WorkflowState 承载）
    """

    def __init__(
        self,
        engine,  # WorkflowEngine
        context_factory,  # WorkflowContextFactory
        checkpoint_manager,  # CheckpointManager
        workflow_builder,  # build_analysis_workflow
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
        #
        # 状态类型由引擎提供（engine.new_state），
        state = self.engine.new_state(run_id)
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
        state.data["question"] = question
        for key in ("planner_agent", "research_plan", "executed_tasks", "count"):
            state.data.pop(key, None)
        state.current_node = "planner_agent"
        state.status = WorkflowStatus.PLANNING

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
