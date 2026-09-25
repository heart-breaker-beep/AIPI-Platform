"""
Critic Agent。


负责：

检查其他 Agent 输出质量。


例如：

- 是否缺少关键结果
- 是否分析失败
- 是否需要重新执行


后续 Phase 会扩展：

Retry

Human Review

Validation


"""


from app.agents.base import BaseAgent




class CriticAgent(
    BaseAgent
):


    name = (
        "critic_agent"
    )
    async def execute(
        self,
        context,
        input_data
    ):
        errors = []
        # 必须存在的分析结果

        required_fields = [

            "repository",

            "architecture",

            "technology"

        ]
        for field in required_fields:


            if field not in input_data:


                errors.append(

                    f"{field} missing"

                )

        return {

            # 是否通过检查

            "passed":

                len(errors) == 0,
            # 错误列表

            "errors":

                errors

        }