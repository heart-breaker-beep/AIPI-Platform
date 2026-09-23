"""数据库连接测试。"""

import pytest
from sqlalchemy import text

from app.db.session import AsyncSessionLocal


@pytest.mark.asyncio
async def test_database_connection():
    """测试 SQLAlchemy 是否可以连接 MySQL。"""

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            text("SELECT 1")
        )

        assert result.scalar() == 1