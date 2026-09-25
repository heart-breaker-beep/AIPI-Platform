"""
Agent Runtime。


负责：

执行指定 Agent。


调用流程：

Runtime

    |

    v

Agent

    |

    v

Skill

    |

    v

Tool


"""


class AgentRuntime:



    def __init__(
        self,
        agent_registry
    ):


        # 保存Agent管理器

        self.agent_registry = (
            agent_registry
        )



    async def execute(
        self,
        agent_name,
        context,
        input_data
    ):


        # 根据名称获取Agent

        agent = (
            self.agent_registry.get(
                agent_name
            )
        )



        if agent is None:


            raise Exception(

                f"Agent {agent_name} not found"

            )

        # 执行Agent

        result = await agent.execute(

            context,

            input_data

        )



        return result