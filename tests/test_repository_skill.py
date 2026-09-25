import pytest


from app.skills.repository_analysis_skill import (
    RepositoryAnalysisSkill
)



class FakeGithubTool:


    async def execute(
        self,
        **kwargs
    ):


        return {

            "name":
            kwargs["repo"]

        }




class FakeFileReader:


    async def execute(
        self,
        **kwargs
    ):


        return {

            "content":
            "README"

        }




class FakeDependencyTool:


    async def execute(
        self,
        **kwargs
    ):


        return {

            "fastapi":
            "installed"

        }




class Context:


    tools={

        "github_repository":
            FakeGithubTool(),


        "file_reader":
            FakeFileReader(),


        "dependency_analyzer":
            FakeDependencyTool()

    }





@pytest.mark.asyncio
async def test_repository_skill():


    skill = RepositoryAnalysisSkill()



    result = await skill.execute(

        Context(),

        {

            "owner":
            "test",


            "repo":
            "demo"

        }

    )



    assert (
        result["repository"]["name"]
        ==
        "demo"
    )


    assert (
        "readme"
        in result
    )


    assert (
        "dependencies"
        in result
    )