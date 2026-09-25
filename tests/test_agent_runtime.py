"""
测试 Agent Runtime。


验证：

Runtime

    |

    v

Agent

    |

    v

返回结果


"""


import pytest


from app.agents.agent_runtime import (
    AgentRuntime
)




class FakeAgent:


    async def execute(
        self,
        context,
        input_data
    ):


        return {


            "success":

                True

        }





class FakeRegistry:


    def get(
        self,
        name
    ):


        return FakeAgent()





@pytest.mark.asyncio
async def test_agent_runtime():



    runtime = AgentRuntime(

        FakeRegistry()

    )



    result = await runtime.execute(

        "test_agent",

        None,

        {}

    )



    assert (

        result["success"]

        is True

    )