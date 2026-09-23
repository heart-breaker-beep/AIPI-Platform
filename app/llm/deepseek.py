"""
DeepSeek LLM实现。
"""

from .base import BaseLLM
class DeepSeekLLM(BaseLLM):

    def __init__(
        self,
        client
    ):

        self.client = client
    async def chat(
        self,
        messages
    ):

        response = await self.client.chat.completions.create(

            model="deepseek-chat",
            messages=messages
        )
        return response.choices[0].message.content