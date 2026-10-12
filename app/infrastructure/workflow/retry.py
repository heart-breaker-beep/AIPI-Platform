"""
Workflow Retry Policy。

Phase 10：
- Retryable Error
- NonRetryable Error
- 最大重试次数
- 指数退避
"""

import asyncio

from app.core.exceptions import (
    NonRetryableError,
    RetryableError,
)


class RetryPolicy:
    """
    Workflow 重试策略。

    RetryPolicy 本身只负责：
    1. 判断异常是否允许 Retry
    2. 判断是否超过最大 Retry 次数
    3. 给出两次尝试之间该等多久
    """

    def __init__(
        self,
        max_retry: int = 3,
        backoff_base: float = 2.0,
        max_backoff: float = 10.0,
    ) -> None:

        if max_retry < 0:
            raise ValueError(
                "max_retry cannot be negative"
            )

        self.max_retry = max_retry

        # 退避基数与上限。
        #
        # 为什么需要退避：上游限流（GitHub 429、LLM 5xx）
        # 往往是「立刻重试还是失败」，隔几秒就恢复了。
        # 原来是无间隔连打，三次尝试加起来不到一秒，
        # 等于把重试预算浪费在对方的恢复窗口里。
        #
        # 为什么做成参数：测试不该真的睡 6 秒，
        # 把基数设为 0 即可让退避变成一次空转。
        self.backoff_base = backoff_base
        self.max_backoff = max_backoff

    def can_retry(
        self,
        retry_count: int,
    ) -> bool:
        """判断当前 retry_count 是否还能继续 Retry。"""

        return retry_count < self.max_retry

    def is_retryable(
        self,
        error: Exception,
    ) -> bool:
        """
        判断异常是否允许 Retry。

        RetryableError：
            可以重试

        NonRetryableError：
            不允许重试
        """

        if isinstance(
            error,
            NonRetryableError,
        ):
            return False

        if isinstance(
            error,
            RetryableError,
        ):
            return True

        return False

    def should_retry(
        self,
        error: Exception,
        retry_count: int,
    ) -> bool:
        """综合判断是否应该 Retry。"""

        return (
            self.is_retryable(error)
            and self.can_retry(retry_count)
        )

    def backoff_delay(
        self,
        retry_count: int,
    ) -> float:
        """
        计算第 retry_count 次重试前要等多久。

        1 → base，2 → base² …… 直到 max_backoff 封顶。
        """

        if self.backoff_base <= 0:
            return 0.0

        delay = self.backoff_base ** max(
            retry_count,
            0,
        )

        return float(
            min(
                delay,
                self.max_backoff,
            )
        )

    async def wait_before_retry(
        self,
        retry_count: int,
    ) -> None:
        """按退避策略等待（基数 <= 0 时不等）。"""

        delay = self.backoff_delay(
            retry_count
        )

        if delay <= 0:
            return

        await asyncio.sleep(delay)
