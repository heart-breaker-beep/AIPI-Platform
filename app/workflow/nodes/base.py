"""
Workflow 节点基类兼容入口。

项目只保留：
    app.workflow.node.BaseNode

这里通过重新导出保持旧代码兼容。
"""

from app.workflow.node import BaseNode


__all__ = [
    "BaseNode",
]