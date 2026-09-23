import pytest

from app.tools.mysql_query_tool import (
    MySQLQueryTool
)



class FakeResult:


    def mappings(self):

        return self


    def all(self):

        return [
            {
                "name": "test_repo"
            }
        ]



class FakeSession:


    async def execute(
        self,
        sql,
        params
    ):

        return FakeResult()



@pytest.mark.asyncio
async def test_mysql_query_tool():


    tool = MySQLQueryTool(
        FakeSession()
    )


    result = await tool.execute(
        "select * from repo"
    )


    assert result[0]["name"] == (
        "test_repo"
    )