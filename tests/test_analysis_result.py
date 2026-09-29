from app.services.analysis_result_service import (
    analysis_result_service,
)


def test_analysis_result_build():

    data = {

        "repository": {

            "name": "demo",

            "language": "Python",

            "url":
            "https://github.com/a/b",
        },


        "agent_outputs": {

            "ArchitectureAgent": {

                "summary":
                "architecture",

                "facts":[
                    "FastAPI"
                ],

                "evidence_ids":[
                    "e1"
                ],
            }
        },

        "technology_stack": {

            "languages":[
                "Python"
            ]
        }
    }


    result = (
        analysis_result_service.build(
            "run-001",
            data,
        )
    )


    assert (
        result.run_id
        ==
        "run-001"
    )


    assert (
        result.project_overview.name
        ==
        "demo"
    )


    assert (
        len(result.agents)
        ==
        1
    )