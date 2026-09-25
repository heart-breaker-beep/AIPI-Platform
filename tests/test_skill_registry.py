from app.skills.registry import (
    create_skill_registry
)



def test_skill_registry():


    registry = create_skill_registry()



    assert (
        "repository_analysis"
        in registry.skills
    )



    assert (
        registry.get(
            "repository_analysis"
        )
        is not None
    )