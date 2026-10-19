"""
Workflow 层异常定义。

统一使用：

    app.core.exceptions.WorkflowError

避免项目中出现两个不同的 WorkflowError。
"""

from app.core.exceptions import WorkflowError


__all__ = [
    "WorkflowError",
]
