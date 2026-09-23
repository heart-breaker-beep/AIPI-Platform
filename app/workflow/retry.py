"""
Workflow重试策略。
"""


class RetryPolicy:
    def __init__(
        self,
        max_retry=3
    ):

        # 最大重试次数
        self.max_retry = max_retry

    def can_retry(
        self,
        count
    ):

        return (
            count < self.max_retry
        )