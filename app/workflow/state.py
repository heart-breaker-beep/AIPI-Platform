"""
Workflow 运行状态。

Phase 10：
- 支持 Design Gate
- 支持 Human Review
- 支持 Pause / Resume
- 支持 Retry
- 支持 Checkpoint
"""

from dataclasses import dataclass, field
from typing import Any

class WorkflowStatus:
    """Workflow 状态常量。"""

    CREATED = "CREATED"

    PLANNING = "PLANNING"

    WAITING_DESIGN = "WAITING_DESIGN"

    ANALYZING = "ANALYZING"

    WAITING_HUMAN = "WAITING_HUMAN"

    PAUSED = "PAUSED"

    RETRYING = "RETRYING"

    FAILED = "FAILED"

    COMPLETED = "COMPLETED"

    # 人工放弃。
    #
    # 与 FAILED 刻意分开：
    # FAILED 是「跑出错了」，CANCELED 是「我改主意了」。
    # 混用会让失败率统计失真，
    # 用户也分不清是自己的操作还是系统故障。
    CANCELED = "CANCELED"


@dataclass
class WorkflowState:
    """
    保存一次 Workflow 执行过程中的完整状态。

    该对象可以被 CheckpointManager 序列化并恢复。
    """

    # Workflow 执行 ID
    run_id: str

    # 当前 Workflow 状态
    status: str = WorkflowStatus.CREATED

    # 当前正在执行的 Node
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

    # 当前 Node 的重试次数
    retry_count: int = 0

    # 当前 Node 最大重试次数
    max_retry: int = 3

    # 暂停原因
    pause_reason: str | None = None

    # 是否已经获得人工批准
    human_approved: bool = False

    # Checkpoint 版本
    checkpoint_version: int = 0

    def mark_waiting_design(self) -> None:
        """进入 Design Gate，等待人工审批。"""

        self.status = WorkflowStatus.WAITING_DESIGN

    def approve(self) -> None:
        """人工批准 Research Plan。"""

        self.human_approved = True
        self.status = WorkflowStatus.ANALYZING

    def pause(
        self,
        reason: str = "manual_pause",
    ) -> None:
        """暂停 Workflow。"""

        self.status = WorkflowStatus.PAUSED
        self.pause_reason = reason

    def resume(self) -> None:
        """恢复 Workflow。"""

        self.status = WorkflowStatus.ANALYZING
        self.pause_reason = None

    def cancel(
        self,
        reason: str = "manual_cancel",
    ) -> None:
        """人工放弃本次分析。"""

        self.status = WorkflowStatus.CANCELED
        self.pause_reason = reason

    def replan(self, question: str) -> None:
        """
        回到 Planner 重新规划。

        清掉上一轮的规划产物，否则重新执行 planner_agent 时
        它读到的还是旧结果，方案不会变 ——
        用户改了问题却看不到方案变化，会以为功能失效。
        """

        self.data["question"] = question

        for key in (
            "planner_agent",
            "research_plan",
            "executed_tasks",
            "count",
        ):
            self.data.pop(key, None)

        self.current_node = "planner_agent"
        self.status = WorkflowStatus.PLANNING

    def start_retry(self) -> None:
        """进入 Retry 状态。"""

        self.status = WorkflowStatus.RETRYING

    def reset_retry(self) -> None:
        """重置当前 Node 的 retry count。"""

        self.retry_count = 0

    def can_retry(self) -> bool:
        """判断当前 Node 是否还能继续重试。"""

        return self.retry_count < self.max_retry

    def increase_retry(self) -> None:
        """增加当前 Node 的 retry 次数。"""

        self.retry_count += 1