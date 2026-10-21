"""Bounded incremental trace response."""

from pydantic import BaseModel, Field


class TraceResponse(BaseModel):
    run_id: str
    events: list[dict] = Field(default_factory=list)
    next_cursor: int = 0
    has_more: bool = False
    trace_state: str = "available"
    execution: dict = Field(default_factory=dict)
