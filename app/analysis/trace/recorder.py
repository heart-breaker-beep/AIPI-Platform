"""Best-effort trace recorder. Each event has its own bounded transaction."""

import asyncio
import logging
from time import monotonic
from uuid import uuid4

from app.analysis.trace.sanitizer import safe_attributes, safe_text
from app.persistence.repositories.analysis_trace import utcnow

logger = logging.getLogger(__name__)


class TraceRecorder:
    def __init__(self, run_id, repository):
        self.run_id = run_id
        self.repository = repository
        self.execution_id = str(uuid4())
        self.gaps = 0
        self.retry_after = 0
        self.execution = {"execution_id": self.execution_id, "status": "running"}

    async def emit(self, *, event_type, category, name, message="", status="completed",
                   span_id=None, parent_span_id=None, duration_ms=None, attributes=None):
        now = utcnow().isoformat() + "Z"
        self.execution.update(last_activity_at=now, last_seen_at=now, gap_count=self.gaps)
        if event_type == "span.started":
            self.execution["current_stage"] = safe_text(name, 120)
        attrs = safe_attributes(attributes)
        if category == "run" and event_type == "span.finished":
            self.execution["status"] = status
            self.execution["workflow_status"] = attrs.get("workflow_status")
        if monotonic() < self.retry_after and not (category == "run" and event_type == "span.finished"):
            self.gaps += 1
            return
        try:
            await asyncio.wait_for(self.repository.append(
                self.run_id, self.execution_id,
                {"event_type": event_type, "category": category, "name": safe_text(name, 120),
                 "message": safe_text(message), "span_id": span_id, "parent_span_id": parent_span_id,
                 "status": status, "level": "warning" if status in {
                     "failed", "partial", "unavailable", "interrupted"} else "info",
                 "duration_ms": duration_ms, "attributes": attrs}, dict(self.execution),
            ), timeout=0.8)
        except Exception:  # noqa: BLE001 - trace failure must not fail the analysis.
            self.gaps += 1
            self.retry_after = monotonic() + 5
            logger.warning("trace write unavailable | run=%s | execution=%s", self.run_id, self.execution_id)

    async def heartbeat(self):
        try:
            await asyncio.wait_for(self.repository.heartbeat(self.run_id, self.execution_id), timeout=0.8)
        except Exception:  # noqa: BLE001
            logger.warning("trace heartbeat unavailable | run=%s", self.run_id)
