"""Repository 数据访问层测试。"""

import pytest
from sqlalchemy import delete

from app.db.session import AsyncSessionLocal
from app.models.repository import Repository
from app.repositories.repository import RepositoryRepository


@pytest.mark.asyncio
async def test_create_and_get_repository():
    """测试 Repository 创建和查询。"""

    url = "https://github.com/test-user/test-agent-project"

    async with AsyncSessionLocal() as session:
        # 先清理上一次运行可能残留的同 URL 记录，
        # 否则 repositories.url 的 UNIQUE 约束会让重复运行失败。
        await session.execute(
            delete(Repository).where(
                Repository.url == url
            )
        )
        await session.commit()

        repository_repository = RepositoryRepository(
            session
        )

        repository = await repository_repository.create(
            url=url,
            owner="test-user",
            name="test-agents-project",
            description="Test Agent Project",
            default_branch="main",
            language="Python",
            stars=100,
            forks=20,
        )

        assert repository.id is not None
        assert repository.owner == "test-user"
        assert repository.name == "test-agents-project"

        found = await repository_repository.get_by_url(
            url
        )

        assert found is not None
        assert found.id == repository.id
        assert found.url == url

        found_by_id = await repository_repository.get_by_id(
            repository.id
        )

        assert found_by_id is not None
        assert found_by_id.name == "test-agents-project"