"""
FastAPI 应用入口。

负责：

1. FastAPI 应用初始化
2. 全局配置加载
3. 日志初始化
4. 全局异常处理
5. API 路由注册
"""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


class NoCacheStaticFiles(StaticFiles):
    """
    静态资源每次都让浏览器回源校验。

    为什么需要这个
    ==============

    StaticFiles 默认**不发 Cache-Control**。
    浏览器遇到这种响应会启用启发式缓存
    （按 RFC 9111，通常取 Last-Modified 之后 10% 的时间做新鲜期），
    期间直接拿本地副本，不发请求。

    结果是：代码改了、容器重建了，页面却还是旧的。
    这一现象极难判断 —— 用户会以为是功能没生效、
    或者后端没改对，而真正的问题只是浏览器揣着一份旧 JS。

    加 no-cache 之后，浏览器每次带 If-None-Match 回源：
    文件没变就是 304（几十字节，开销可忽略），
    变了立刻拿到新的。
    """

    def file_response(self, *args, **kwargs):
        response = super().file_response(*args, **kwargs)

        # no-cache = 先校验再用，不是「不缓存」。
        response.headers["Cache-Control"] = "no-cache"

        return response

from app.api.v1.analysis import (
    router as analysis_router,
)
from app.core.config import get_settings
from app.api.error_handlers import (
    application_error_handler,
    unexpected_error_handler,
)
from app.core.exceptions import ApplicationError
from app.core.logging import (
    get_logger,
    setup_logging,
)
from app.integrations.llm.chat_tool import (
    aclose_llm_clients,
)


settings = get_settings()


# 前端静态资源目录。
STATIC_DIR = Path(__file__).parent / "static"


# 应用启动时初始化全局日志。
setup_logging()

logger = get_logger(
    __name__
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期钩子。

    退出时关闭进程内的 LLM 客户端 ——
    每个客户端自带连接池，
    不关就只能等 GC 回收，
    反复建应用（例如测试）会攒下若干条空闲连接。

    关闭失败只记日志：退出路径上不该再抛异常。
    """

    yield

    try:

        await aclose_llm_clients()

    except Exception as error:  # noqa: BLE001

        logger.warning(
            "关闭 LLM 客户端失败：%s",
            error,
        )


app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "AI Agent GitHub Project "
        "Intelligence Platform"
    ),
    version="0.1.0",
    debug=settings.DEBUG,
    lifespan=lifespan,
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
        NoCacheStaticFiles(
            directory=str(STATIC_DIR)
        ),
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
