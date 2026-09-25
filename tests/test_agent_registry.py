"""
测试 Agent Registry。

验证：

Agent 是否可以正常注册和获取。


"""


from app.skills.registry import (
    create_skill_registry
)


from app.agents.agent_registry import (
    create_agent_registry
)



def test_agent_registry():


    # 创建Skill管理器

    skill_registry = (
        create_skill_registry()
    )



    # 创建Agent管理器

    registry = (
        create_agent_registry(
            skill_registry
        )
    )



    # 判断Agent是否存在

    assert (
        registry.get(
            "repository_analysis_agent"
        )
        is not None
    )