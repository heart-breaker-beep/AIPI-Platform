"""
Critic Agent。

负责检查分析结果是否完整。
"""

from app.agents.base import BaseAgent


class CriticAgent(
    BaseAgent
):
    """
    分析结果检查 Agent。
    """

    name = "critic_agent"

    description = (
        "Validate repository analysis results"
    )

    async def execute(
        self,
        context,
        input_data,
    ):
        errors = []

        required_fields = {
            "repository": [
                "repository",
                "repository_analysis",
                "repository_analysis_agent",
            ],
            "architecture": [
                "architecture",
                "architecture_analysis",
                "architecture_analysis_agent",
            ],
            "technology": [
                "technology",
                "technology_analysis",
                "technology_analysis_agent",
                "technology_stack",
            ],
        }

        for logical_name, aliases in (
            required_fields.items()
        ):
            if not any(
                alias in input_data
                for alias in aliases
            ):
                errors.append(
                    f"{logical_name} missing"
                )

        return {
            "passed": not errors,
            "errors": errors,
        }