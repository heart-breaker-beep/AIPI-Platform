"""
Finalizer Workflow Node。

负责：

Human Review
    ↓
Finalizer
    ↓
ReportGenerationSkill
    ↓
Final Report
"""

from .base import BaseNode


class FinalizerNode(BaseNode):
    """最终报告生成节点。"""

    name = "finalizer"

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
        """生成最终项目分析报告。"""

        report_input = {
            key: value
            for key, value in state.data.items()
            if not key.startswith("_")
        }

        report_input.setdefault(
            "title",
            "GitHub Project Intelligence Report",
        )

        report_input.setdefault(
            "filename",
            f"{state.run_id}_analysis.md",
        )

        # Phase 14.2：同时产出 markdown 与结构化 JSON。
        #
        # markdown 是给人读的主产物；
        # JSON 是同一份数据的结构化形态，
        # 供程序消费（导出、二次加工、比对）。
        # 两者由 ReportService 从同一份文档派生，
        # 不会各写各的导致漂移。
        report_input.setdefault(
            "format",
            "both",
        )

        result = await self.skill.execute(
            context=context,
            input_data=report_input,
        )

        state.data["final_report"] = result

        state.outputs.append(result)

        return state