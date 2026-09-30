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



    # Analysis Workflow 依赖这两个 Skill：
    # 缺任何一个 build_analysis_workflow 都会直接报错。
    assert (
        "report_generation"
        in registry.skills
    )



    assert (
        "report_synthesis"
        in registry.skills
    )



    # 单模块深挖：默认报告只看要点时，
    # 用户点名某个模块靠这个 Skill 展开细节。
    assert (
        "module_deep_dive"
        in registry.skills
    )