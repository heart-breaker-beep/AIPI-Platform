"""
Agent 类型 Workflow 节点。

负责：
    - 调用 Agent.execute()
    - 将 Agent 输出保存到 WorkflowState
    - 保留执行历史
"""

from .base import BaseNode


class AgentNode(BaseNode):
    """
    封装 Agent 执行。
    """

    def __init__(
        self,
        name,
        agent,
    ):
        self.name = name
        self.agent = agent

    async def execute(
        self,
        state,
        context,
    ):
        """
        执行 Agent。

        Agent 新接口：

            execute(
                context,
                input_data
            )
        """

        result = await self.agent.execute(
            context,
            state.data,
        )

        # 保存当前 Agent 输出。
        state.data[self.name] = result

        # 保留执行历史。
        state.outputs.append(result)

        return state