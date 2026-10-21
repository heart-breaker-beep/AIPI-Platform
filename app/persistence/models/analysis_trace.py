"""Trace rows deliberately do not lock the workflow's business rows."""

from datetime import datetime

from sqlalchemy import (
    JSON,
    BigInteger,
    DateTime,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.persistence.base import Base


class AnalysisTraceStream(Base):
    __tablename__ = "analysis_trace_streams"

    run_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    last_sequence: Mapped[int] = mapped_column(BigInteger, default=0)
    execution: Mapped[dict] = mapped_column(JSON, default=dict)
    updated_at: Mapped[datetime] = mapped_column(DateTime)


class AnalysisTraceEvent(Base):
    __tablename__ = "analysis_trace_events"
    __table_args__ = (
        UniqueConstraint("run_id", "sequence", name="uq_trace_run_sequence"),
        Index("ix_trace_run_execution_span", "run_id", "execution_id", "span_id"),
    )

    event_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    run_id: Mapped[str] = mapped_column(String(36), index=True)
    sequence: Mapped[int] = mapped_column(BigInteger)
    execution_id: Mapped[str] = mapped_column(String(36))
    span_id: Mapped[str | None] = mapped_column(String(36))
    parent_span_id: Mapped[str | None] = mapped_column(String(36))
    event_type: Mapped[str] = mapped_column(String(40))
    category: Mapped[str] = mapped_column(String(20))
    name: Mapped[str] = mapped_column(String(120))
    message: Mapped[str] = mapped_column(String(500), default="")
    status: Mapped[str] = mapped_column(String(30), default="completed")
    level: Mapped[str] = mapped_column(String(12), default="info")
    occurred_at: Mapped[datetime] = mapped_column(DateTime)
    duration_ms: Mapped[int | None] = mapped_column(Integer)
    attributes: Mapped[dict] = mapped_column(JSON, default=dict)
