"""
Planner 计划执行节点。

负责：
    1. 读取 PlannerAgent 生成的 tasks
    2. 按 tasks 顺序获取 Agent
    3. 依次执行 Agent
    4. 将 Agent 输出合并回 WorkflowState.data

Planner 只负责规划。
PlanExecutorNode 负责消费规划结果。
"""

from .base import BaseNode


class PlanExecutorNode(BaseNode):
    """
    根据 PlannerAgent 输出的 tasks 执行 Agent。
    """

    name = "plan_executor"

    def __init__(
        self,
        name: str = "plan_executor",
        planner_key: str = "planner_agent",
    ):
        self.name = name
        self.planner_key = planner_key

    async def execute(
        self,
        state,
        context,
    ):
        """
        执行 Planner 生成的任务列表。

        Planner 输出：

        {
            "tasks": [
                "repository_analysis_agent",
                "architecture_analysis_agent",
                "technology_analysis_agent",
                "evidence_analysis_agent",
                "critic_agent"
            ]
        }
        """

        planner_result = state.data.get(
            self.planner_key
        )

        if not isinstance(
            planner_result,
            dict,
        ):
            raise ValueError(
                "Planner result is missing."
            )

        tasks = planner_result.get(
            "tasks"
        )

        if not isinstance(
            tasks,
            list,
        ):
            raise ValueError(
                "Planner result must contain "
                "a list field named 'tasks'."
            )

        if not tasks:
            raise ValueError(
                "Planner returned an empty task list."
            )

        executed_tasks = []

        for agent_name in tasks:

            if not isinstance(
                agent_name,
                str,
            ):
                raise ValueError(
                    "Planner task must be "
                    "an Agent name string."
                )

            agent = context.agents.get(
                agent_name
            )

            if agent is None:
                raise ValueError(
                    f"Agent not found: {agent_name}"
                )

            result = await agent.execute(
                context,
                state.data,
            )

            # 保留 Agent 级别结果。
            state.data[
                agent_name
            ] = result

            # 将结构化 Agent 输出合并到当前 Workflow 数据。
            #
            # 例如：
            #
            # RepositoryAnalysisAgent
            #     -> {"repository": ...}
            #
            # 合并后：
            #
            # state.data["repository"]
            #
            # 这样 CriticAgent 可以直接读取。
            if isinstance(
                result,
                dict,
            ):
                state.data.update(
                    result
                )

            state.outputs.append(
                result
            )

            executed_tasks.append(
                agent_name
            )

        state.data[
            "executed_tasks"
        ] = executed_tasks

        return state