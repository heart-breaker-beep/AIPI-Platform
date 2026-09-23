import pytest

from app.db.session import AsyncSessionLocal
from app.services.repository_service import RepositoryService
from app.project_analysis.repository_indexer import RepositoryIndexer



@pytest.mark.asyncio
async def test_repository_pipeline():

    url = (
        "https://github.com/"
        "langchain-ai/langchain"
    )


    async with AsyncSessionLocal() as session:

        service = (
            RepositoryService(session)
        )


        repository = await (
            service.get_or_create(
                url
            )
        )


        assert (
            repository.owner
            ==
            "langchain-ai"
        )


        indexer = (
            RepositoryIndexer()
        )


        result = await (
            indexer.index(
                repository.owner,
                repository.name,
                repository.default_branch,
            )
        )


        assert result == 1