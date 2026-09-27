"""
Planner Agent。

负责：

根据用户需求生成项目分析计划。
"""

from app.agents.base import BaseAgent


class PlannerAgent(
    BaseAgent
):
    """项目分析规划 Agent。"""

    name = "planner_agent"

    description = (
        "Create a research plan for GitHub "
        "project analysis."
    )

    async def execute(
        self,
        context,
        input_data,
    ):
        """生成第一版项目分析计划。"""

        tasks = [
            "repository_analysis_agent",
            "architecture_analysis_agent",
            "technology_analysis_agent",
            "evidence_analysis_agent",
            "critic_agent",
        ]

        research_plan = {
            "plan_version": 1,
            "analysis_type": (
                "github_agent_project"
            ),
            "question": input_data.get(
                "question"
            ),
            "tasks": tasks,
            "evidence_required": True,
        }

        return {
            "tasks": tasks,
            "research_plan": research_plan,
        }