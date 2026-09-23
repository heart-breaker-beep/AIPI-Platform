import pytest


from app.tools.qdrant_search_tool import (
    QdrantSearchTool
)



class FakeVectorStore:


    def search(
        self,
        query_vector,
        limit
    ):

        return [

            type(
                "Point",
                (),
                {
                    "payload":
                    {
                        "file":
                        "workflow.py"
                    }
                }
            )

        ]



@pytest.mark.asyncio
async def test_qdrant_search():

    tool = QdrantSearchTool(
        FakeVectorStore()
    )


    result = await tool.execute(
        [0.1,0.2]
    )


    assert result[0]["file"] == (
        "workflow.py"
    )