"""
Workflow 层异常定义。

统一使用：

    app.core.exceptions.WorkflowError

避免项目中出现两个不同的 WorkflowError。
"""

from app.core.exceptions import WorkflowError


class NodeExecutionError(WorkflowError):
    """
    Workflow Node 执行异常。

    继承统一的 WorkflowError，
    因此可以被 WorkflowError / ApplicationError
    统一捕获。
    """

    pass


__all__ = [
    "WorkflowError",
    "NodeExecutionError",
]