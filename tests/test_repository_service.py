"""Repository Service 测试。"""

import pytest

from app.db.session import AsyncSessionLocal
from app.services.repository_service import RepositoryService


@pytest.mark.asyncio
async def test_get_or_create_repository():
    """测试 Repository 不存在时创建，存在时复用。"""

    url = "https://github.com/service-test/agent-project"

    async with AsyncSessionLocal() as session:
        service = RepositoryService(session)

        first = await service.get_or_create(url)

        assert first.id is not None
        assert first.owner == "service-test"
        assert first.name == "agent-project"

        second = await service.get_or_create(url)

        assert second.id == first.id
        assert second.url == first.url