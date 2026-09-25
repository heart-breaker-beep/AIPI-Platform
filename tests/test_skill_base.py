from app.skills.base import BaseSkill



def test_skill_has_name():

    """
    测试Skill是否具备基本属性
    """


    class DemoSkill(BaseSkill):


        name = "demo"


        description = "demo skill"



        async def execute(
            self,
            context,
            input_data
        ):

            return {}



    skill = DemoSkill()



    assert skill.name == "demo"