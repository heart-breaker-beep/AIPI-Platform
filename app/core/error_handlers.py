"""FastAPI 全局异常处理器，负责将项目异常转换为统一 HTTP 响应。"""

import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import ApplicationError


logger = logging.getLogger(__name__)


async def application_error_handler(
    request: Request,
    exc: ApplicationError,
) -> JSONResponse:
    """统一处理项目定义的业务异常。"""

    logger.error(
        "application error | path=%s | error_code=%s | message=%s",
        request.url.path,
        exc.error_code,
        exc.message,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.error_code,
                "message": exc.message,
            },
        },
    )


async def unexpected_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """统一处理未预期的系统异常。"""

    # 未知异常记录完整堆栈，但只向客户端返回通用错误，
    # 避免数据库、API Key 等内部信息泄露。
    logger.exception(
        "unexpected error | path=%s",
        request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "Internal server error",
            },
        },
    )