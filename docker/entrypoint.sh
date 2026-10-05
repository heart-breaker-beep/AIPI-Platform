#!/bin/sh
# ============================================================
# 容器启动脚本
# ------------------------------------------------------------
# 1. 等 MySQL 真的能连上（compose 的 healthcheck 只管容器活着，
#    不等于 MySQL 已经能接受连接）
# 2. 跑 alembic 迁移建表
# 3. 交棒给 CMD（uvicorn）
# ============================================================

set -e

# 跳过迁移（比如数据库由外部统一管理时）。
if [ "${SKIP_MIGRATIONS}" != "true" ]; then

  echo "[entrypoint] 等待 MySQL 就绪 ..."

  # 用同步驱动探测：异步驱动在这条路径上没有优势，
  # 而且 pymysql 已在依赖里，不需要额外安装。
  python - <<'PY'
import sys
import time

from sqlalchemy import create_engine, text

from app.core.config import get_settings

url = get_settings().DATABASE_URL.replace("+asyncmy", "+pymysql")

last = ""
for attempt in range(1, 61):
    try:
        engine = create_engine(url, pool_pre_ping=True)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        engine.dispose()
        print("[entrypoint] MySQL 已就绪")
        break
    except Exception as exc:            # noqa: BLE001 - 启动期要吞掉所有连接错误
        last = f"{type(exc).__name__}: {exc}"
        print(f"[entrypoint]   [{attempt}/60] 未就绪，2 秒后重试")
        time.sleep(2)
else:
    sys.exit(f"[entrypoint] 等待 MySQL 超时，最后一次错误：{last}")
PY

  echo "[entrypoint] 执行数据库迁移 ..."
  alembic upgrade head

else
  echo "[entrypoint] SKIP_MIGRATIONS=true，跳过迁移"
fi

echo "[entrypoint] 启动应用：$*"

exec "$@"
