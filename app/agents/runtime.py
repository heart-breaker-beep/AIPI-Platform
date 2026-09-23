"""
Agent运行环境。
"""


class AgentRuntime:


    def __init__(
        self,
        llm,
        tools=None,
        skills=None
    ):

        self.llm = llm

        self.tools = tools or {}

        self.skills = skills or {}



    async def execute(
        self,
        agent,
        state
    ):

        result = await agent.run(
            state,
            self
        )


        return result