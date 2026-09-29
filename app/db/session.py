"""数据库 Engine、Session 和 FastAPI 数据库依赖。"""

import json

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import get_settings


settings = get_settings()

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,

    # JSON 列默认使用 ensure_ascii=True 序列化，
    # 中文会被转义成 \uXXXX，
    # 一个汉字从 3 字节（utf8mb4）膨胀到 6 字节。
    #
    # checkpoints.state_data 里包含中文报告，
    # 转义会让单行体积显著增大，
    # 进而在读取时触发 asyncmy 驱动的
    # 「BufferError: object cannot be re-sized」
    # → Lost connection to MySQL server。
    #
    # 连接字符集是 utf8mb4，
    # 直接写原文是安全的。
    json_serializer=lambda value: json.dumps(
        value,
        ensure_ascii=False,
    ),
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """为 API 请求提供数据库 Session。"""

    async with AsyncSessionLocal() as session:
        yield session