"""
DeepSeek LLM实现。

DeepSeek 提供 OpenAI 兼容接口，
底层使用 openai SDK 的 AsyncOpenAI 客户端。

构造方式保持向后兼容：

    DeepSeekLLM(client)

也可以显式指定模型与超时：

    DeepSeekLLM(client, model="deepseek-chat", timeout=60.0)
"""

from .base import BaseLLM


class DeepSeekLLM(BaseLLM):

    # 默认模型。
    #
    # 保留该默认值是为了不破坏
    # 早期只传 client 的调用方式。
    DEFAULT_MODEL = "deepseek-chat"

    def __init__(
        self,
        client,
        model: str | None = None,
        timeout: float | None = None,
        max_tokens: int | None = None,
    ):

        self.client = client

        self.model = (
            model or self.DEFAULT_MODEL
        )

        self.timeout = timeout

        self.max_tokens = max_tokens

    async def chat(
        self,
        messages,
        model: str | None = None,
        max_tokens: int | None = None,
    ):
        """
        发送一次对话请求，返回文本内容。

        model / max_tokens 允许单次调用覆盖实例默认值。
        """

        create_kwargs = {
            "model": model or self.model,
            "messages": messages,
        }

        if self.timeout is not None:
            create_kwargs["timeout"] = (
                self.timeout
            )

        limit = (
            max_tokens
            if max_tokens is not None
            else self.max_tokens
        )

        # 必须显式给出上限。
        #
        # 不设置时走服务端默认值，
        # 综合分析那种几千字符的 JSON 回复
        # 会被中途截断，
        # 截断的 JSON 一定解析失败。
        if limit is not None:
            create_kwargs["max_tokens"] = limit

        response = (
            await self.client
            .chat.completions.create(
                **create_kwargs
            )
        )

        return response.choices[0].message.content
