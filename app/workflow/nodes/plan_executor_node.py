"""
Planner 计划执行节点。

负责：

1. 读取 PlannerAgent 生成的 tasks
2. 按 tasks 顺序获取 Agent
3. 构建当前 Agent 所需 Context
4. 依次执行 Agent
5. 将 Agent 输出合并回 WorkflowState.data
"""

from .base import BaseNode


class PlanExecutorNode(BaseNode):
    """根据 PlannerAgent 输出执行 Agent。"""

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
        """执行 Planner 生成的任务列表。"""

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

            agent_input = dict(
                state.data
            )

            # Phase 11 Context Manager 接入。
            if (
                context.context_manager is not None
                and state.data.get(
                    "repository_id"
                ) is not None
            ):
                query = (
                    state.data.get("question")
                    or "GitHub project analysis"
                )

                agent_context = (
                    await context.context_manager.build(
                        run_id=state.run_id,
                        repository_id=state.data[
                            "repository_id"
                        ],
                        query=query,
                        workflow_state=state.data,
                        user_instruction=query,
                    )
                )

                agent_input["_context"] = (
                    agent_context
                )

            result = await agent.execute(
                context,
                agent_input,
            )

            # 保存 Agent 级别输出。
            state.data[
                agent_name
            ] = result

            # 合并结构化输出。
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