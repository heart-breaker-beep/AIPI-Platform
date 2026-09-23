"""
Workflow运行状态。
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class WorkflowState:
    """
    保存一次Workflow执行过程中的状态。
    """

    # Workflow执行ID
    run_id: str

    # 当前状态
    status: str = "CREATED"

    # 当前执行节点
    current_node: str | None = None

    # 业务数据
    data: dict[str, Any] = field(
        default_factory=dict
    )

    # 节点执行结果
    outputs: list[Any] = field(
        default_factory=list
    )

    # 错误记录
    errors: list[str] = field(
        default_factory=list
    )

    # 重试次数
    retry_count: int = 0