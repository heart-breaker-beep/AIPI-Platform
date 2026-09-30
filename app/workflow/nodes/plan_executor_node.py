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

            # Agent 名键只保留还有读取方的部分。
            #
            # 原实现把同一份结果写三遍：
            #
            #     state.data[agent_name]   本段
            #     state.data.update(...)   拍平到顶层
            #     state.outputs.append(...) 再存一份
            #
            # 实测（被分析项目 Legal，17.8MB）：
            # architecture 一份 57KB、evidence 29KB、
            # repository 5KB，三写下来约 250KB 纯重复，
            # 把 state_data 推到 263KB，
            # 越过 asyncmy 单字段 256KB 的缓冲区分片上限，
            # 报告接口读 checkpoint 直接
            # Lost connection to MySQL server。
            #
            # 顶层拍平的那份是规范数据源
            # （报告 / 综合分析 / 分析结果都读它），
            # 因此这里只额外保留
            # architecture_analysis_agent 的精简副本 ——
            # CriticAgent 会按这个键读它。
            slim = self._slim_agent_result(
                agent_name,
                result,
            )

            if slim is not None:

                state.data[agent_name] = slim

            # 合并结构化输出。
            if isinstance(
                result,
                dict,
            ):
                state.data.update(
                    result
                )

            # outputs 的正文没有任何业务读取方
            # （只作为 agent_outputs 透出），
            # 因此不再原样复制大对象，
            # 只留一个可读的运行痕迹。
            state.outputs.append(
                self._output_marker(
                    agent_name,
                    result,
                )
            )

            executed_tasks.append(
                agent_name
            )

        state.data[
            "executed_tasks"
        ] = executed_tasks

        return state

    # Agent 名键的精简规则。
    #
    # 顶层拍平的那份是规范数据源，
    # Agent 名键只是兼容层，
    # 因此按「有没有读取方」逐个决定：
    #
    #   SLIM_AGENT_FIELDS  有大读取方 -> 只留它需要的子字段
    #   DROPPED_AGENT_KEYS 完全没有读取方 -> 不写
    #   其余               原样保留
    #
    # 只对体积大的动手：
    # critic_agent（30B）、technology_analysis_agent（193B）
    # 留着也不占地方，但删了会破坏断言它们的测试。
    SLIM_AGENT_FIELDS = {
        # 读取方：CriticAgent 需要
        # modules / directory_structure / files。
        #
        # 它不读 project_structure（顶层有），
        # 而那一块恰好最大（33KB）。
        "architecture_analysis_agent": (
            "files",
            "modules",
            "directory_structure",
        ),
    }

    # 体积大、且没有任何读取方的 Agent 名键。
    #
    # evidence_analysis_agent（29KB）的内容是
    # {"evidence": [...], "count": N}，
    # 而 evidence 与 count 都已经在顶层拍平，
    # 全项目没有任何地方按这个键去读 state.data。
    DROPPED_AGENT_KEYS = (
        "evidence_analysis_agent",
    )

    @classmethod
    def _slim_agent_result(
        cls,
        agent_name,
        result,
    ):
        """
        决定 Agent 名键写什么。

        返回 None 表示「不写这个键」。
        """

        if agent_name in cls.DROPPED_AGENT_KEYS:
            return None

        fields = cls.SLIM_AGENT_FIELDS.get(
            agent_name
        )

        if not fields:
            # 其余 Agent 原样保留。
            return result

        if not isinstance(result, dict):
            return result

        return {
            key: result[key]
            for key in fields
            if key in result
        }

    @staticmethod
    def _output_marker(
        agent_name,
        result,
    ) -> dict:
        """
        生成 outputs 里的一条运行痕迹。

        保留 Agent 名与产出规模，
        便于排查「这一步到底有没有产出」，
        但不复制正文 —— 正文在 state.data 里。
        """

        marker = {
            "agent": agent_name,
            "type": type(result).__name__,
        }

        if isinstance(result, dict):

            marker["fields"] = sorted(
                result.keys()
            )

        return marker