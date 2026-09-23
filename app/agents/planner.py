"""
任务规划Agent。
"""


from .base import BaseAgent



class PlannerAgent(BaseAgent):

    name="planner"

    async def run(
        self,
        state,
        context
    ):

        prompt = f"""
        用户需求:
        {state.data.get("query")}

        请生成分析计划。

        """
        result = await context.llm.chat(
            [
                {
                    "role":"user",
                    "content":prompt
                }
            ]
        )

        state.data[
            "plan"
        ] = result


        return state