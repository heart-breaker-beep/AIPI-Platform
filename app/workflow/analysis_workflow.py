"""
AIPI 单项目分析 Workflow。

完整链路：

Start
    ↓
Planner
    ↓
Design Gate
    ↓
Plan Executor
    ↓
Human Review
    ↓
Finalizer
    ↓
End
"""

from app.workflow.nodes.agent_node import AgentNode
from app.workflow.nodes.design_gate_node import (
    DesignGateNode,
)
from app.workflow.nodes.end_node import EndNode
from app.workflow.nodes.finalizer_node import (
    FinalizerNode,
)
from app.workflow.nodes.human_node import HumanNode
from app.workflow.nodes.plan_executor_node import (
    PlanExecutorNode,
)
from app.workflow.nodes.start_node import StartNode
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

    planner = context.agents.get(
        "planner_agent"
    )

    if planner is None:
        raise ValueError(
            "Planner Agent is not registered."
        )

    report_skill = context.skills.get(
        "report_generation"
    )

    if report_skill is None:
        raise ValueError(
            "Report generation skill is not registered."
        )

    workflow.add_node(
        StartNode()
    )

    workflow.add_node(
        AgentNode(
            name="planner_agent",
            agent=planner,
        )
    )

    workflow.add_node(
        DesignGateNode()
    )

    workflow.add_node(
        PlanExecutorNode()
    )

    workflow.add_node(
        HumanNode()
    )

    workflow.add_node(
        FinalizerNode(
            skill=report_skill,
        )
    )

    workflow.add_node(
        EndNode()
    )

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