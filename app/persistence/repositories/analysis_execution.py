"""Connection-scoped execution ownership, independent of business commits."""
from contextlib import asynccontextmanager, suppress
from hashlib import sha256

from sqlalchemy import text

from app.core.exceptions import ConflictError

_sqlite_active = set()


@asynccontextmanager
async def execution_lock(bind, run_id):
    """MySQL named locks are connection scoped, independent of business commits."""
    name = "aipi:" + sha256(run_id.encode()).hexdigest()[:48]
    if bind.dialect.name != "mysql":
        # SQLite is supported for local tests; production uses MySQL.
        if bind.dialect.name != "sqlite":
            raise RuntimeError("Execution locks require MySQL")
        if name in _sqlite_active:
            raise ConflictError("该任务已有执行中的操作，请等待其完成。")
        _sqlite_active.add(name)
        try:
            yield None
        finally:
            _sqlite_active.discard(name)
        return
    async with bind.connect() as connection:
        acquired = (await connection.execute(text("SELECT GET_LOCK(:name, 0)"), {"name": name})).scalar()
        if acquired != 1:
            raise ConflictError("该任务已有执行中的操作，请等待其完成。")

        async def check_owner():
            result = await connection.execute(
                text("SELECT IS_USED_LOCK(:name) = CONNECTION_ID()"), {"name": name},
            )
            if result.scalar() != 1:
                raise RuntimeError("Execution lock lost")

        try:
            yield check_owner
        finally:
            if not connection.invalidated:
                with suppress(Exception):
                    await connection.execute(text("SELECT RELEASE_LOCK(:name)"), {"name": name})


\n