"""
Design Gate Workflow Node。

职责：
    - 读取 Planner Agent 生成的 Research Plan
    - 将 Research Plan 提升到 WorkflowState.data 顶层
    - 将 Workflow 置为 WAITING_DESIGN
    - 等待人工审批后继续执行
"""

from app.workflow.node import BaseNode


class DesignGateNode(BaseNode):
    """
    Phase 12 研究计划设计闸门。

    Planner Agent 完成后进入该节点。

    数据流：

        planner_agent
            ↓
        planner_agent["research_plan"]
            ↓
        state.data["research_plan"]
            ↓
        WAITING_DESIGN
            ↓
        Human Approval
    """

    name = "design_gate"

    async def execute(
        self,
        state,
        context,
    ):
        """
        保存 Research Plan，并暂停 Workflow 等待设计审批。
        """

        # 获取 Planner Agent 的输出。
        planner_result = state.data.get(
            "planner_agent",
            {},
        )

        # Planner Agent 应该返回 research_plan。
        research_plan = planner_result.get(
            "research_plan"
        )

        # 将 Research Plan 保存到 WorkflowState 顶层。
        #
        # 这样后续：
        #   - PlanExecutorNode
        #   - Checkpoint
        #   - Memory
        #   - Human Approval
        #
        # 都可以直接读取 state.data["research_plan"]。
        if research_plan is not None:
            state.data[
                "research_plan"
            ] = research_plan

        # 进入 Design Gate，
        # 等待人工确认研究计划。
        state.mark_waiting_design()

        return state