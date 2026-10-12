"""
Workflow Checkpoint 数据模型。
"""

from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.db.base import Base


class Checkpoint(Base):
    """
    保存 Workflow 某一时刻的完整执行快照。
    """

    __tablename__ = "checkpoints"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    run_id: Mapped[str] = mapped_column(
        ForeignKey(
            "analysis_runs.id"
        ),
        nullable=False,
        index=True,
    )

    checkpoint_version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    current_node: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    state_data: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )

    outputs: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    errors: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    retry_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    pause_reason: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    human_approved: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )