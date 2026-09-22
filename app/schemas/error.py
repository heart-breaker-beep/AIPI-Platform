"""统一错误响应模型，用于保证不同 API 返回一致的错误结构。"""

from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """错误的具体信息。"""

    code: str
    message: str


class ErrorResponse(BaseModel):
    """统一 API 错误响应。"""

    success: bool
    error: ErrorDetail