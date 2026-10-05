"""
FastAPI 应用入口。

负责：

1. FastAPI 应用初始化
2. 全局配置加载
3. 日志初始化
4. 全局异常处理
5. API 路由注册
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.v1.analysis import (
    router as analysis_router,
)
from app.core.config import get_settings
from app.core.error_handlers import (
    application_error_handler,
    unexpected_error_handler,
)
from app.core.exceptions import ApplicationError
from app.core.logging import (
    get_logger,
    setup_logging,
)


settings = get_settings()


# 前端静态资源目录。
STATIC_DIR = Path(__file__).parent / "static"


# 应用启动时初始化全局日志。
setup_logging()

logger = get_logger(
    __name__
)


app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "AI Agent GitHub Project "
        "Intelligence Platform"
    ),
    version="0.1.0",
    debug=settings.DEBUG,
)


# 注册统一业务异常处理器。
app.add_exception_handler(
    ApplicationError,
    application_error_handler,
)


# 注册未预期异常处理器。
app.add_exception_handler(
    Exception,
    unexpected_error_handler,
)


# 注册 Analysis API。
app.include_router(
    analysis_router,
    prefix="/api/v1",
)


# 样式与脚本走静态挂载。
#
# 挂在 /static 而不是根路径，
# 免得和 /api/v1、/health 抢路由。
if STATIC_DIR.is_dir():

    app.mount(
        "/static",
        StaticFiles(directory=str(STATIC_DIR)),
        name="static",
    )


@app.get(
    "/health",
    tags=["System"],
)
async def health_check():
    """
    健康检查接口。
    """

    return {
        "status": "ok",
        "environment": settings.APP_ENV,
    }


@app.get(
    "/",
    tags=["System"],
)
async def root():
    """
    根路径返回操作页面。

    前端无构建步骤（index.html + app.css + app.js），
    只调用本服务已有的 /api/v1 接口，
    静态资源由 /static 挂载提供。

    文件缺失时退回 JSON，
    保证 API 本身不受影响。
    """

    index = STATIC_DIR / "index.html"

    if index.is_file():

        return FileResponse(
            index,
            media_type="text/html",
        )

    return {
        "name": settings.APP_NAME,
        "version": "0.1.0",
        "status": "running",
        "ui": "app/static/index.html not found",
    }