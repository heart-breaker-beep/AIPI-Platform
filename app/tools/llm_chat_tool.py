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

from openai import AsyncOpenAI

from app.core.config import get_settings
from app.llm.deepseek import DeepSeekLLM
from app.tools.base import BaseTool


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
