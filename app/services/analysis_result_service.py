"""
Analysis Result 构建服务。

职责：

WorkflowState.data

        ↓

AnalysisResult


Phase12新增。
"""


from typing import Any


from app.schemas.analysis_result import (
    AnalysisResult,
    AgentAnalysisResult,
    ProjectOverview,
    TechnologyStack,
)



class AnalysisResultService:
    """
    将 Workflow 数据转换成标准分析结果。
    """



    def build(
        self,
        run_id: str,
        data: dict[str, Any],
    ) -> AnalysisResult:
        """
        构建 AnalysisResult。
        """


        repository = (
            data.get(
                "repository",
                {}
            )
        )



        if not isinstance(
            repository,
            dict,
        ):
            repository = {}



        technology_stack = (
            data.get(
                "technology_stack",
                {}
            )
        )


        if not isinstance(
            technology_stack,
            dict,
        ):
            technology_stack = {}



        agents = []


        agent_outputs = (
            data.get(
                "agent_outputs",
                {}
            )
        )



        if isinstance(
            agent_outputs,
            dict,
        ):


            for agent_name, output in (
                agent_outputs.items()
            ):


                if not isinstance(
                    output,
                    dict,
                ):
                    continue



                agents.append(

                    AgentAnalysisResult(

                        agent_name=agent_name,


                        summary=output.get(
                            "summary"
                        ),


                        facts=output.get(
                            "facts",
                            [],
                        ),


                        evidence_ids=output.get(
                            "evidence_ids",
                            [],
                        ),
                    )
                )



        return AnalysisResult(


            run_id=run_id,



            project_overview=

            ProjectOverview(

                name=repository.get(
                    "name"
                ),


                description=repository.get(
                    "description"
                ),


                repository_url=repository.get(
                    "url"
                ),


                language=repository.get(
                    "language"
                ),
            ),



            technology_stack=

            TechnologyStack(

                languages=

                technology_stack.get(
                    "languages",
                    [],
                ),


                frameworks=

                technology_stack.get(
                    "frameworks",
                    [],
                ),


                databases=

                technology_stack.get(
                    "databases",
                    [],
                ),


                tools=

                technology_stack.get(
                    "tools",
                    [],
                ),
            ),



            agents=agents,



            workflow=

            {

                "state":

                data.get(
                    "workflow_state"
                ),


                "tasks":

                data.get(
                    "task_results",
                    [],
                ),
            },



            skills=data.get(
                "skills",
                [],
            ),



            tools=data.get(
                "tools",
                [],
            ),



            rag=data.get(
                "rag",
                {},
            ),



            memory=data.get(
                "memory",
                {},
            ),



            database=data.get(
                "database",
                {},
            ),



            evidence=data.get(
                "evidences",
                data.get(
                    "evidence",
                    [],
                ),
            ),
        )



analysis_result_service = (
    AnalysisResultService()
)