"""项目统一异常体系，用于区分参数、Workflow、Tool、Agent 和 LLM 等不同错误。"""


class ApplicationError(Exception):
    """所有业务异常的基类。"""

    status_code = 500
    error_code = "APPLICATION_ERROR"

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ValidationError(ApplicationError):
    """请求参数或业务数据验证失败。"""
    status_code = 400
    error_code = "VALIDATION_ERROR"


class WorkflowError(ApplicationError):
    """Workflow 执行失败。"""
    status_code = 500
    error_code = "WORKFLOW_ERROR"


class ToolError(ApplicationError):
    """Tool 执行失败。"""
    status_code = 500
    error_code = "TOOL_ERROR"


class AgentError(ApplicationError):
    """Agent 执行失败。"""
    status_code = 500
    error_code = "AGENT_ERROR"


class RepositoryError(ApplicationError):
    """Repository 数据访问失败。"""
    status_code = 500
    error_code = "REPOSITORY_ERROR"


class LLMError(ApplicationError):
    """LLM 调用失败。"""
    status_code = 500
    error_code = "LLM_ERROR"


class RetryableError(ApplicationError):
    """可以通过重试机制恢复的异常。"""
    status_code = 500
    error_code = "RETRYABLE_ERROR"


class NonRetryableError(ApplicationError):
    """不应该继续重试的异常。"""
    status_code = 500
    error_code = "NON_RETRYABLE_ERROR"