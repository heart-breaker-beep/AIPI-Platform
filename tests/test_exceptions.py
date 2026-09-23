"""项目统一异常体系测试。"""

from app.core.exceptions import (
    AgentError,
    ApplicationError,
    LLMError,
    RetryableError,
    ValidationError,
)


def test_application_error():
    """测试基础应用异常。"""

    error = ApplicationError("test error")

    assert error.message == "test error"
    assert error.status_code == 500
    assert error.error_code == "APPLICATION_ERROR"


def test_validation_error():
    """测试参数验证异常。"""

    error = ValidationError("invalid input")

    assert error.message == "invalid input"
    assert error.status_code == 400
    assert error.error_code == "VALIDATION_ERROR"


def test_agent_error():
    """测试 Agent 异常。"""

    error = AgentError("agents failed")

    assert error.status_code == 500
    assert error.error_code == "AGENT_ERROR"


def test_llm_error():
    """测试 LLM 异常。"""

    error = LLMError("llm failed")

    assert error.status_code == 500
    assert error.error_code == "LLM_ERROR"


def test_retryable_error():
    """测试可重试异常。"""

    error = RetryableError("temporary error")

    assert error.error_code == "RETRYABLE_ERROR"