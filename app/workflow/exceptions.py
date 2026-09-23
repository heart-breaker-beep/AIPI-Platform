"""
Workflow异常定义。
"""

from app.core.exceptions import (
    ApplicationError,
)


class WorkflowError(ApplicationError):
    """
    Workflow基础异常。

    继承 ApplicationError，使其能被全局异常处理器识别。
    """
    pass

class NodeExecutionError(WorkflowError):
    """
    Node执行失败异常。
    """

    pass