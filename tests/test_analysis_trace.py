"""Trace delivery, isolation and lifecycle tests. Optional MySQL uses a disposable database."""

import asyncio
import os
from contextlib import asynccontextmanager
from types import SimpleNamespace
from uuid import uuid4

import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.analysis.trace.recorder import TraceRecorder
from app.analysis.trace.sanitizer import safe_attributes
from app.core.exceptions import ConflictError, NotFoundError
from app.core.trace import bind_trace, trace_span, traced
from app.persistence.base import Base
from app.persistence.models import AnalysisRun, Repository
from app.persistence.repositories.analysis_execution import execution_lock
from app.persistence.repositories.analysis_trace import AnalysisTraceRepository
from app.schemas.analysis import AnalysisCreateRequest
from app.services.analysis_service import AnalysisService
from app.services.trace_service import TraceService
from app.workflow.state import WorkflowState


class MemorySink:
    def __init__(self):
        self.events = []

    async def append(self, run_id, execution_id, event, execution):
        self.events.append({"run_id": run_id, "execution_id": execution_id, **event})


@pytest.mark.asyncio
async def test_started_event_visible_before_slow_call_finishes_and_parent_is_preserved():
    sink = MemorySink()
    recorder = TraceRecorder("run-a", sink)
    entered, release = asyncio.Event(), asyncio.Event()

    @traced("file", "read_file")
    async def slow_file(file_path):
        entered.set()
        await release.wait()
        return "source"

    async def execute():
        async with bind_trace(recorder), trace_span("node", "architecture"):
            return await slow_file("src/main.py")

    task = asyncio.create_task(execute())
    await asyncio.wait_for(entered.wait(), 2)
    assert not task.done()
    assert len(sink.events) == 2
    assert sink.events[1]["parent_span_id"] == sink.events[0]["span_id"]
    release.set()
    assert await task == "source"
    assert [e["event_type"] for e in sink.events] == ["span.started", "span.started", "span.finished", "span.finished"]
    assert sink.events[2]["span_id"] == sink.events[1]["span_id"]
    assert sink.events[2]["duration_ms"] >= 0


@pytest.mark.asyncio
async def test_concurrent_runs_and_exceptions_do_not_leak_context():
    sink = MemorySink()

    async def run(name):
        async with bind_trace(TraceRecorder(name, sink)), trace_span("skill", name):
            await asyncio.sleep(0)
            async with trace_span("tool", name + "-child"):
                if name == "a":
                    raise RuntimeError("secret not copied")

    result = await asyncio.gather(run("a"), run("b"), return_exceptions=True)
    assert isinstance(result[0], RuntimeError)
    for event in sink.events:
        assert event["name"].startswith(event["run_id"])
    assert any(e["status"] == "failed" for e in sink.events if e["run_id"] == "a")
    assert not any("secret" in str(e) for e in sink.events)
    async with trace_span("tool", "outside"):
        pass
    assert len(sink.events) == 8


@pytest.mark.parametrize("reply,status", [({"available": False}, "unavailable"),
                                         ({"modules": [{"error": "404"}]}, "partial"),
                                         ({"count": 3}, "completed"), ("", "unavailable")])
@pytest.mark.asyncio
async def test_non_exception_degradation_is_not_success(reply, status):
    sink = MemorySink()

    @traced("skill", "sample")
    async def execute():
        return reply

    async with bind_trace(TraceRecorder("run", sink)):
        assert await execute() == reply
    assert sink.events[-1]["status"] == status


@pytest.mark.asyncio
async def test_trace_storage_failure_does_not_change_business_result():
    class BrokenSink:
        async def append(self, *args):
            raise RuntimeError("database unavailable")

    recorder = TraceRecorder("run", BrokenSink())
    async with bind_trace(recorder), trace_span("node", "sample"):
        value = 42
    assert value == 42
    assert recorder.gaps == 2


def test_metadata_allowlist_and_token_redaction():
    attrs = safe_attributes({"prompt": "private", "headers": {"secret": "x"},
                             "file_path": "src/sk-SECRET.py", "count": 3,
                             "model": "token=SECRET"})
    assert "prompt" not in attrs and "headers" not in attrs
    assert "SECRET" not in str(attrs)
    assert attrs["count"] == 3


@pytest_asyncio.fixture
async def trace_db():
    if os.environ.get("AIPI_TRACE_MYSQL_TEST") != "1":
        pytest.skip("Set AIPI_TRACE_MYSQL_TEST=1 to test against a disposable local MySQL database")
    from app.core.config import get_settings

    settings = get_settings()
    database = "aipi_trace_test_" + uuid4().hex
    url = URL.create("mysql+asyncmy", username=settings.MYSQL_USER, password=settings.MYSQL_PASSWORD,
                     host=settings.MYSQL_HOST, port=settings.MYSQL_PORT, query={"charset": "utf8mb4"})
    admin = create_async_engine(url, echo=False)
    engine = None
    try:
        async with admin.begin() as connection:
            await connection.execute(text(f"CREATE DATABASE `{database}` CHARACTER SET utf8mb4"))
        engine = create_async_engine(url.set(database=database), echo=False)
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
        yield engine, async_sessionmaker(engine, expire_on_commit=False)
    finally:
        if engine:
            await engine.dispose()
        assert database.startswith("aipi_trace_test_") and len(database) == len("aipi_trace_test_") + 32
        async with admin.begin() as connection:
            await connection.execute(text(f"DROP DATABASE IF EXISTS `{database}`"))
        await admin.dispose()


@pytest.mark.asyncio
async def test_mysql_concurrent_commits_are_ordered_and_pagination_has_no_gaps(trace_db):
    _, sessions = trace_db
    repo = AnalysisTraceRepository(sessions)

    async def write(number):
        await repo.append("run-a", "execution", {"event_type": "progress", "category": "tool",
            "name": str(number), "span_id": None, "parent_span_id": None,
            "message": "", "status": "completed", "level": "info", "duration_ms": None,
            "attributes": {}}, {"status": "completed"})

    await asyncio.gather(*(write(n) for n in range(12)))
    cursor, received = 0, []
    while True:
        events, more, _ = await repo.read("run-a", cursor, 3)
        received.extend(events)
        cursor = events[-1]["sequence"] if events else cursor
        if not more:
            break
    assert [e["sequence"] for e in received] == list(range(1, 13))
    assert len({e["event_id"] for e in received}) == 12
    assert (await repo.read("another-run", 0, 10))[0] == []


@pytest.mark.asyncio
async def test_mysql_lock_prevents_concurrent_actions_across_connections(trace_db):
    engine, _ = trace_db
    async with execution_lock(engine, "same-run"):
        with pytest.raises(ConflictError):
            async with execution_lock(engine, "same-run"):
                pytest.fail("duplicate ownership")
        async with execution_lock(engine, "different-run"):
            pass
    async with execution_lock(engine, "same-run"):
        pass


@pytest.mark.asyncio
async def test_mysql_deferred_start_streams_while_request_is_running(trace_db, monkeypatch):
    _, sessions = trace_db
    service = AnalysisService()
    entered, release = asyncio.Event(), asyncio.Event()

    class SlowWorkflow:
        @traced("skill", "repository_analysis")
        async def start_workflow(self, run_id, **kwargs):
            entered.set()
            await release.wait()
            return WorkflowState(run_id=run_id, status="WAITING_DESIGN", current_node="design_gate")

    monkeypatch.setattr(service, "_get_workflow", lambda session: SlowWorkflow())
    async with sessions() as session:
        run = await service.create_analysis(session, AnalysisCreateRequest(
            repo_url="https://github.com/demo/trace-example", defer_start=True, enable_rag=True,
        ))
    assert run.status == "CREATED"
    assert not entered.is_set()

    async def start():
        async with sessions() as session:
            return await service.start_analysis(session, run.run_id)

    task = asyncio.create_task(start())
    await asyncio.wait_for(entered.wait(), 5)
    try:
        async with sessions() as session:
            live = await TraceService().read(session, run.run_id)
        assert live.execution["status"] == "running"
        assert any(e["name"] == "repository_analysis" and e["event_type"] == "span.started" for e in live.events)
        assert not task.done()
        with pytest.raises(ConflictError):
            await start()
    finally:
        release.set()
    response = await task
    assert response.status == "WAITING_DESIGN"
    async with sessions() as session:
        saved = await TraceService().read(session, run.run_id)
        assert saved.execution["status"] == "waiting"
        assert len(saved.events) == 5
    with pytest.raises(ConflictError):
        await start()


@pytest.mark.asyncio
async def test_mysql_trace_does_not_wait_for_locked_business_row(trace_db):
    _, sessions = trace_db
    async with sessions() as session:
        repository = Repository(url="https://github.com/test/trace", owner="test", name="trace")
        session.add(repository)
        await session.flush()
        session.add(AnalysisRun(id="locked-run", repository_id=repository.id))
        await session.commit()
    async with sessions() as business:
        run = await business.get(AnalysisRun, "locked-run")
        run.status = "ANALYZING"
        await business.flush()
        recorder = TraceRecorder("locked-run", AnalysisTraceRepository(sessions))
        await asyncio.wait_for(recorder.emit(event_type="span.started", category="node", name="analysis"), 2)
        assert recorder.gaps == 0
        events, _, _ = await AnalysisTraceRepository(sessions).read("locked-run", 0, 10)
        assert len(events) == 1
        await business.rollback()


@pytest.mark.asyncio
async def test_trace_not_found_is_404(monkeypatch):
    from app.services import trace_service

    class MissingRun:
        async def get_by_id(self, run_id):
            return None

    monkeypatch.setattr(trace_service, "AnalysisRunRepository", lambda session: MissingRun())
    with pytest.raises(NotFoundError):
        await TraceService().read(SimpleNamespace(), "missing")


@pytest.mark.asyncio
async def test_mysql_loss_of_execution_ownership_interrupts_worker(trace_db, monkeypatch):
    from app.services import analysis_execution

    _, sessions = trace_db

    @asynccontextmanager
    async def lost_lock(bind, run_id):
        async def check():
            raise ConnectionError("lock connection closed")
        yield check

    monkeypatch.setattr(analysis_execution, "execution_lock", lost_lock)
    monkeypatch.setattr(analysis_execution, "HEARTBEAT_INTERVAL", 0.01)

    class Worker:
        @analysis_execution.traced_action("start")
        async def execute(self, session, run_id):
            await asyncio.Future()

    async with sessions() as session:
        with pytest.raises(ConflictError, match="执行锁"):
            await asyncio.wait_for(Worker().execute(session, "lost-lock-run"), 3)
    events, _, execution = await AnalysisTraceRepository(sessions).read("lost-lock-run", 0, 10)
    assert events[-1]["status"] == "interrupted"
    assert execution["status"] == "interrupted"


@pytest.mark.asyncio
async def test_mysql_deferred_workflow_keeps_checkpoint_versions_unique(trace_db, monkeypatch):
    from sqlalchemy import select

    from app.analysis.nodes.end_node import EndNode
    from app.analysis.nodes.start_node import StartNode
    from app.persistence.models.checkpoint import Checkpoint
    from app.services.analysis_factory import create_analysis_workflow
    from app.workflow.transition import Transition
    from app.workflow.workflow import Workflow

    _, sessions = trace_db
    service = AnalysisService()

    def short_workflow(session):
        workflow = create_analysis_workflow(session)

        def build(context):
            graph = Workflow()
            graph.add_node(StartNode())
            graph.add_node(EndNode())
            graph.add_transition(Transition("start", "end"))
            return graph

        workflow.workflow_builder = build
        return workflow

    monkeypatch.setattr(service, "_get_workflow", short_workflow)
    async with sessions() as session:
        created = await service.create_analysis(session, AnalysisCreateRequest(
            repo_url="https://github.com/demo/checkpoint-trace", defer_start=True,
        ))
    async with sessions() as session:
        result = await service.start_analysis(session, created.run_id)
        assert result.status == "COMPLETED"
        versions = (await session.execute(select(Checkpoint.checkpoint_version).where(
            Checkpoint.run_id == created.run_id).order_by(Checkpoint.id))).scalars().all()
        assert versions == sorted(set(versions))
        assert versions[0] == 1 and versions[-1] > 1
