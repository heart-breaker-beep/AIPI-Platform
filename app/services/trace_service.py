"""Read traces separately from business transactions and distinguish stale work."""

import logging
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import async_sessionmaker

from app.core.exceptions import NotFoundError
from app.persistence.repositories.analysis_run import AnalysisRunRepository
from app.persistence.repositories.analysis_trace import AnalysisTraceRepository
from app.schemas.trace import TraceResponse

logger = logging.getLogger(__name__)


class TraceService:
    async def read(self, session, run_id, after=0, limit=100):
        run = await AnalysisRunRepository(session).get_by_id(run_id)
        if run is None:
            raise NotFoundError("Analysis run not found.")
        try:
            repository = AnalysisTraceRepository(async_sessionmaker(session.bind, expire_on_commit=False))
            events, has_more, execution = await repository.read(run_id, after, limit)
        except Exception:  # noqa: BLE001 - status/report remains usable without trace tables.
            logger.warning("trace query unavailable | run=%s", run_id)
            return TraceResponse(run_id=run_id, next_cursor=after, trace_state="unavailable")
        trace_state = "available" if execution is not None else "not_recorded"
        if execution and not events and after == 0:
            trace_state = "expired"
        execution = execution or {}
        if execution.get("status") == "running" and execution.get("last_seen_at"):
            seen = datetime.fromisoformat(execution["last_seen_at"].replace("Z", "+00:00"))
            if (datetime.now(timezone.utc) - seen).total_seconds() > 30:
                execution["status"] = "interrupted"
        return TraceResponse(
            run_id=run_id, events=events,
            next_cursor=events[-1]["sequence"] if events else after,
            has_more=has_more, trace_state=trace_state, execution=execution,
        )
