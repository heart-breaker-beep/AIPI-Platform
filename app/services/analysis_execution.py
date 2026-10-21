"""Serialize lifecycle operations across workers and bind one execution trace."""

import asyncio
from contextlib import suppress
from functools import wraps

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.analysis.trace.recorder import TraceRecorder
from app.core.exceptions import ConflictError
from app.core.trace import bind_trace, result_summary, trace_span
from app.persistence.repositories.analysis_execution import execution_lock
from app.persistence.repositories.analysis_trace import AnalysisTraceRepository

HEARTBEAT_INTERVAL = 5


async def record_created(session, run_id):
    if not isinstance(session, AsyncSession) or session.bind is None:
        return
    recorder = TraceRecorder(run_id, AnalysisTraceRepository(
        async_sessionmaker(session.bind, expire_on_commit=False),
    ))
    recorder.execution["status"] = "created"
    await recorder.emit(event_type="run.created", category="run", name="created")


def traced_action(name):
    def decorate(function):
        @wraps(function)
        async def wrapped(self, session, run_id, *args, **kwargs):
            # In-memory service tests and adapters have no database binding.
            if not isinstance(session, AsyncSession) or session.bind is None:
                return await function(self, session, run_id, *args, **kwargs)
            async with execution_lock(session.bind, run_id) as check_owner:
                # Re-read state after taking the lock, outside an old MySQL snapshot.
                await session.rollback()
                recorder = TraceRecorder(run_id, AnalysisTraceRepository(
                    async_sessionmaker(session.bind, expire_on_commit=False),
                ))
                owner_task = asyncio.current_task()
                lost_lock = False

                async def monitor():
                    nonlocal lost_lock
                    while True:
                        await asyncio.sleep(HEARTBEAT_INTERVAL)
                        if check_owner is not None:
                            try:
                                await asyncio.wait_for(check_owner(), timeout=3)
                            except Exception:  # noqa: BLE001 - loss of ownership stops work.
                                lost_lock = True
                                owner_task.cancel()
                                return
                        await recorder.heartbeat()

                heartbeat = None
                try:
                    async with bind_trace(recorder), trace_span("run", name) as outcome:
                        heartbeat = asyncio.create_task(monitor())
                        result = await function(self, session, run_id, *args, **kwargs)
                        outcome["status"], outcome["attributes"] = result_summary(result)
                        return result
                except asyncio.CancelledError:
                    if lost_lock:
                        raise ConflictError("执行锁连接已断开，本次执行已中断，请查询任务状态。") from None
                    raise
                finally:
                    if heartbeat is not None:
                        heartbeat.cancel()
                        with suppress(asyncio.CancelledError):
                            await heartbeat
        return wrapped
    return decorate
