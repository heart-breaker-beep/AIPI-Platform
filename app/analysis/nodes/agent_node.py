"""
Agent 类型 Workflow 节点。

负责：
    - 调用 Agent.execute()
    - 将 Agent 输出保存到 WorkflowState
    - 保留执行历史
"""

from .base import BaseNode, output_marker


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

        # 执行历史只留痕迹，不复制正文 ——
        # 正文已经在 state.data 里，
        # 而 outputs 不经过体积瘦身。
        state.outputs.append(
            output_marker(
                self.name,
                result,
            )
        )

        return state