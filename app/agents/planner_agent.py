"""
Planner Agent。


负责：

根据用户需求生成任务计划。


当前 Phase 8：

先实现固定规划。


Phase 9：

升级为：

LLM Dynamic Planning


"""


from app.agents.base import BaseAgent




class PlannerAgent(
    BaseAgent
):


    name = (
        "planner_agent"
    )



    async def execute(
        self,
        context,
        input_data
    ):



        # 当前先定义固定分析流程

        # 后续由LLM动态决定

        tasks = [



            "repository_analysis_agent",



            "architecture_analysis_agent",



            "technology_analysis_agent",



            "evidence_analysis_agent",



            "critic_agent"

        ]



        return {


            "tasks":

                tasks

        }