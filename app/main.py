"""FastAPI 应用入口：负责应用初始化、日志、异常处理和 API 路由注册。"""

from fastapi import FastAPI

from app.api.v1.analysis import router as analysis_router
from app.core.config import get_settings
from app.core.error_handlers import (
    application_error_handler,
    unexpected_error_handler,
)
from app.core.exceptions import ApplicationError
from app.core.logging import get_logger, setup_logging


settings = get_settings()

# 应用启动时初始化全局日志，保证各模块使用统一的日志格式。
setup_logging()
logger = get_logger(__name__)


app = FastAPI(
    title=settings.APP_NAME,
    description="AI Agent GitHub Project Intelligence Platform",
    version="0.1.0",
    debug=settings.DEBUG,
)

# 所有业务异常统一转换成标准 HTTP 错误响应，
# 避免每个 API 都单独处理异常。
app.add_exception_handler(
    ApplicationError,
    application_error_handler,
)

# 捕获未预期异常，避免直接向客户端暴露内部错误信息。
app.add_exception_handler(
    Exception,
    unexpected_error_handler,
)

# 注册 v1 API。
# 后续 Workflow、Agent、Project 等接口都会继续挂载到这里。
app.include_router(
    analysis_router,
    prefix="/api/v1",
)


@app.get("/health", tags=["System"])
async def health_check():
    """健康检查接口，用于确认 API 服务是否正常运行。"""
    return {
        "status": "ok",
        "environment": settings.APP_ENV,
    }


@app.get("/", tags=["System"])
async def root():
    """项目根路径，返回应用基本信息。"""
    return {
        "name": settings.APP_NAME,
        "version": "0.1.0",
        "status": "running",
    }