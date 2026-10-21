"""Ordered, independently committed trace writes and bounded incremental reads."""

from datetime import datetime, timedelta, timezone
from uuid import uuid4

from sqlalchemy import delete, select
from sqlalchemy.dialects.mysql import insert as mysql_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert

from app.persistence.models.analysis_trace import (
    AnalysisTraceEvent,
    AnalysisTraceStream,
)


def utcnow():
    return datetime.now(timezone.utc).replace(tzinfo=None)


class AnalysisTraceRepository:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def append(self, run_id, execution_id, event, execution=None):
        async with self.session_factory() as session, session.begin():
            dialect = session.bind.dialect.name
            insert = mysql_insert if dialect == "mysql" else sqlite_insert
            stmt = insert(AnalysisTraceStream).values(
                run_id=run_id, last_sequence=0, execution={}, updated_at=utcnow(),
            )
            if dialect == "mysql":
                stmt = stmt.on_duplicate_key_update(run_id=stmt.inserted.run_id)
            else:
                stmt = stmt.on_conflict_do_nothing(index_elements=["run_id"])
            await session.execute(stmt)
            stream = (await session.execute(select(AnalysisTraceStream).where(
                AnalysisTraceStream.run_id == run_id).with_for_update())).scalar_one()
            stream.last_sequence += 1
            stream.updated_at = utcnow()
            if execution is not None:
                stream.execution = execution
            session.add(AnalysisTraceEvent(
                event_id=str(uuid4()), run_id=run_id, execution_id=execution_id,
                sequence=stream.last_sequence, occurred_at=utcnow(), **event,
            ))

    async def heartbeat(self, run_id, execution_id):
        async with self.session_factory() as session, session.begin():
            stream = (await session.execute(select(AnalysisTraceStream).where(
                AnalysisTraceStream.run_id == run_id).with_for_update())).scalar_one_or_none()
            if stream and stream.execution.get("execution_id") == execution_id:
                stream.execution = {**stream.execution, "last_seen_at": utcnow().isoformat() + "Z"}

    async def read(self, run_id, after, limit):
        async with self.session_factory() as session:
            stream = await session.get(AnalysisTraceStream, run_id)
            rows = (await session.execute(select(AnalysisTraceEvent).where(
                AnalysisTraceEvent.run_id == run_id, AnalysisTraceEvent.sequence > after,
            ).order_by(AnalysisTraceEvent.sequence).limit(limit + 1))).scalars().all()
            events = [{column.name: getattr(row, column.name) for column in row.__table__.columns}
                      for row in rows[:limit]]
            for event in events:
                event["occurred_at"] = event["occurred_at"].replace(tzinfo=timezone.utc).isoformat()
            return events, len(rows) > limit, dict(stream.execution) if stream else None

    async def purge(self, days=30):
        """Retain stream metadata so an expired trace differs from a legacy run."""
        from app.persistence.models.analysis_run import AnalysisRun

        cutoff = utcnow() - timedelta(days=days)
        async with self.session_factory() as session, session.begin():
            ids = select(AnalysisRun.id).where(
                AnalysisRun.status.in_(["COMPLETED", "FAILED", "CANCELED"]),
                AnalysisRun.updated_at < cutoff,
            )
            await session.execute(delete(AnalysisTraceEvent).where(AnalysisTraceEvent.run_id.in_(ids)))
