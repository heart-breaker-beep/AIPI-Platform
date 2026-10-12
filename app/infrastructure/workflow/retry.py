"""
Workflow Retry Policy。

Phase 10：
- Retryable Error
- NonRetryable Error
- 最大重试次数
"""

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
    """

    def __init__(
        self,
        max_retry: int = 3,
    ) -> None:

        if max_retry < 0:
            raise ValueError(
                "max_retry cannot be negative"
            )

        self.max_retry = max_retry

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