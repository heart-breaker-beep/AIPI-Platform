"""
LLM Chat Tool。

把 LLM 调用封装成 Tool，
供 Skill 通过 context.tools 获取，
与其它 Tool 的装配方式保持一致。

设计约束
========

本 Tool **永不抛异常**。

原因：报告综合分析只是报告的增强章节，
LLM 不可用（没有 API Key / 网络不通 /
额度耗尽 / 返回超时）时，
报告仍然应该正常产出，
只是缺少「结论摘要」部分。

因此所有失败都转成：

    {
        "available": False,
        "reason": "<可读原因>"
    }

由调用方决定如何降级。
"""

import weakref

from openai import AsyncOpenAI

from app.core.config import get_settings
from app.integrations.llm.deepseek import DeepSeekLLM
from app.integrations.base import BaseTool


# 进程内创建过的 Tool 实例。
#
# 用弱引用集合：实例本身随 Context 被回收，
# 这里不需要任何注销逻辑，
# 也不会因为这个登记表把内存留住。
_LIVE_TOOLS: "weakref.WeakSet" = weakref.WeakSet()


async def aclose_llm_clients() -> None:
    """
    关闭进程内所有 LLM 客户端。

    由 FastAPI 的 lifespan 在应用退出时调用 ——
    客户端自带连接池，不关就等 GC，
    进程重启/测试多次建应用时会攒下若干条空闲连接。
    """

    for tool in list(_LIVE_TOOLS):
        await tool.aclose()


class LLMChatTool(BaseTool):

    name = "llm_chat"

    def __init__(
        self,
        llm=None,
    ):
        """
        llm 允许注入一个假实现用于测试。

        注入时完全不读取配置、不创建网络客户端。
        """

        self._llm = llm

        # 自己创建的 AsyncOpenAI 客户端。
        # 注入 llm 时为 None（别人的东西不由我们关）。
        self._client = None

        _LIVE_TOOLS.add(self)

    def _build_llm(self):
        """按配置创建真实的 DeepSeek 客户端。"""

        settings = get_settings()

        api_key = (
            settings.LLM_API_KEY or ""
        ).strip()

        if not api_key:
            return None, (
                "未配置 LLM_API_KEY，"
                "无法调用 LLM 生成综合分析。"
            )

        client = AsyncOpenAI(
            api_key=api_key,
            base_url=settings.LLM_BASE_URL,
            timeout=settings.LLM_TIMEOUT,
        )

        self._client = client

        return (
            DeepSeekLLM(
                client,
                model=settings.LLM_MODEL,
                timeout=settings.LLM_TIMEOUT,
                max_tokens=settings.LLM_MAX_TOKENS,
            ),
            None,
        )

    async def execute(
        self,
        messages,
        model: str | None = None,
        **kwargs,
    ):
        """
        执行一次对话。

        返回：

            {"available": True,  "content": "..."}
            {"available": False, "reason": "..."}
        """

        llm = self._llm

        if llm is None:

            llm, reason = self._build_llm()

            if llm is None:

                return {
                    "available": False,
                    "reason": reason,
                }

            # 缓存到实例上。
            #
            # 为什么必须缓存：AsyncOpenAI 自带连接池，
            # 每次 execute 都新建一个的话，
            # 每次 LLM 调用都会泄漏一个连接池
            # （要等 GC 才可能回收，期间连接一直挂着）。
            # 同一个 Context 里的多次调用现在共用一个客户端。
            self._llm = llm

        try:

            # 默认不传 model，
            # 沿用 BaseLLM 的最小契约
            # chat(messages)，
            # 这样只实现该契约的假实现也能工作。
            if model is None:

                content = await llm.chat(
                    messages
                )

            else:

                content = await llm.chat(
                    messages,
                    model=model,
                )

        # 真实事故的防线：
        # LLM 侧的异常种类很多
        # （鉴权 / 限流 / 超时 / 连接失败），
        # 逐个捕获没有意义，
        # 这里统一降级为 available=False。
        except Exception as error:

            return {
                "available": False,
                "reason": (
                    "LLM 调用失败："
                    f"{type(error).__name__}: "
                    f"{error}"
                ),
            }

        if not isinstance(
            content,
            str,
        ) or not content.strip():

            return {
                "available": False,
                "reason": (
                    "LLM 返回了空内容。"
                ),
            }

        return {
            "available": True,
            "content": content,
        }

    async def aclose(self) -> None:
        """
        关闭由本工具创建的 LLM 客户端。

        注入的假实现没有可关的连接，直接跳过。
        关闭后实例恢复成「还没建过」的状态，
        下次 execute 会按配置重新建一个。
        """

        client = self._client

        self._client = None
        self._llm = None

        if client is None:
            return

        close = getattr(
            client,
            "aclose",
            None,
        )

        if callable(close):

            await close()
