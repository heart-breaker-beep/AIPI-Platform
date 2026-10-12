"""
Node执行结果。
"""


from dataclasses import dataclass
from typing import Any


@dataclass
class NodeResult:
    """
    节点执行返回结果。
    """


    # 是否执行成功
    success: bool


    # 返回数据
    data: Any = None


    # 错误信息
    error: str | None = None