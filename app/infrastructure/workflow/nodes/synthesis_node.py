"""
Report Synthesis Workflow Node。

负责：

Human Review
    ↓
SynthesisNode
    ↓
ReportSynthesisSkill
    ↓
state.data["synthesis"]

位置在 Human Review 之后、Finalizer 之前：

- 放在 Human Review 之后，
  是为了让综合分析跑在人工批准之后，
  不占用人工等待期间的资源；
- 放在 Finalizer 之前，
  是因为 Finalizer 会把 state.data 中
  所有非 "_" 开头的键转发给报告 Skill，
  因此本节点写入的 "synthesis"
  会被报告自动带上，无需额外接线。
"""

from .base import BaseNode


class SynthesisNode(BaseNode):
    """报告综合分析节点。"""

    name = "synthesis"

    def __init__(
        self,
        skill,
    ):
        self.skill = skill

    async def execute(
        self,
        state,
        context,
    ):
        """生成综合分析结论。"""

        synthesis_input = {
            key: value
            for key, value in state.data.items()
            if not key.startswith("_")
        }

        try:

            result = await self.skill.execute(
                context=context,
                input_data=synthesis_input,
            )

        # 综合分析只是报告的增强章节。
        #
        # 真实事故的防线：
        # 报告中任何一个环节抛异常
        # 都会让整个 Workflow 变成 FAILED
        # （此前一个 README 请求超时
        # 就让 5-Agent 计划整体失败），
        # 因此这里必须降级而不是冒泡。
        except Exception as error:

            result = {
                "available": False,
                "reason": (
                    "综合分析执行失败："
                    f"{type(error).__name__}: "
                    f"{error}"
                ),
                "summary": {},
                "dimensions": {},
            }

        state.data["synthesis"] = result

        state.outputs.append(result)

        return state
