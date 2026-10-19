"""
通用数据访问层基类。

消除了之前各个 Repository 中重复的 CRUD 方法。
通过泛型 + SQLAlchemy 提供统一的数据访问模式。
"""

from typing import Generic, Optional, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """通用数据访问层基类。

    所有 Repository 应继承此类，并声明 model 类变量。

    Example:
        class AnalysisRunRepository(BaseRepository[AnalysisRun]):
            model = AnalysisRun

            async def get_by_run_id(self, run_id: str):
                # 特殊查询方法
                ...
    """

    model: Type[T]

    def __init__(self, session: AsyncSession) -> None:
        """初始化 Repository。

        Args:
            session: SQLAlchemy 异步会话
        """
        self.session = session

    def isolated_write(self):
        """将单条写入隔离在 SAVEPOINT 中，保留外层事务。"""
        return self.session.begin_nested()

    async def create(self, **kwargs) -> T:
        """创建并保存一条记录。

        Args:
            **kwargs: 模型字段键值对

        Returns:
            创建的实体对象

        Example:
            run = await repo.create(
                id="run_123",
                repository_id=1,
                question="What is this?",
            )
        """
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.flush()
        return instance

    async def get_by_id(self, id: any) -> Optional[T]:
        """根据 ID 查询单条记录。

        Args:
            id: 主键值

        Returns:
            查询到的实体对象，不存在返回 None

        Example:
            run = await repo.get_by_id("run_123")
        """
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def delete(self, id: any) -> Optional[T]:
        """删除指定 ID 的记录。

        Args:
            id: 主键值

        Returns:
            被删除的实体对象，不存在返回 None

        Example:
            deleted_run = await repo.delete("run_123")
        """
        instance = await self.get_by_id(id)
        if instance is None:
            return None

        await self.session.delete(instance)
        await self.session.flush()
        return instance

    async def exists(self, id: any) -> bool:
        """检查指定 ID 是否存在。

        Args:
            id: 主键值

        Returns:
            存在返回 True，否则 False

        Example:
            exists = await repo.exists("run_123")
        """
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none() is not None
