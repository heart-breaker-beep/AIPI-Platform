"""验证路由注入和服务拆分，使用替身避免数据库及外部服务调用。"""

from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_analysis_service, get_db, get_report_service
from app.core.exceptions import ValidationError
from app.main import app
from app.services.analysis_service import AnalysisService
from app.services.report_service import ReportService


@pytest.fixture
def api():
    session = object()
    analysis = AsyncMock(spec=AnalysisService)
    reports = AsyncMock(spec=ReportService)
    response = {
        "run_id": "run-1",
        "status": "WAITING_DESIGN",
        "repo_url": "https://github.com/demo/project",
        "question": "分析 workflow",
        "current_node": "design_gate",
        "progress": 20,
        "created_at": datetime.now(timezone.utc),
    }
    saved = app.dependency_overrides.copy()

    async def database():
        yield session

    app.dependency_overrides[get_db] = database
    app.dependency_overrides[get_analysis_service] = lambda: analysis
    app.dependency_overrides[get_report_service] = lambda: reports
    try:
        with TestClient(app) as client:
            yield client, session, analysis, reports, response
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(saved)


def test_create_uses_injected_analysis_service(api):
    client, session, analysis, _, response = api
    analysis.create_analysis.return_value = response
    result = client.post(
        "/api/v1/analysis",
        json={
            "repo_url": response["repo_url"],
            "question": response["question"],
            "enable_rag": True,
        },
    )
    assert result.status_code == 200
    assert result.json()["run_id"] == "run-1"
    assert result.json()["rag_enabled"] is False
    args = analysis.create_analysis.await_args.args
    assert args[0] is session
    assert args[1].enable_rag is True


def test_deferred_create_and_explicit_start_routes(api):
    client, session, analysis, _, response = api
    analysis.create_analysis.return_value = response
    analysis.start_analysis.return_value = response
    result = client.post("/api/v1/analysis", json={"repo_url": response["repo_url"], "defer_start": True})
    assert result.status_code == 200
    assert analysis.create_analysis.await_args.args[1].defer_start is True
    result = client.post("/api/v1/analysis/run-1/start")
    assert result.status_code == 200
    analysis.start_analysis.assert_awaited_once_with(session, "run-1")


def test_trace_route_paginates_and_validates_cursor(api, monkeypatch):
    from types import SimpleNamespace

    from app.api.v1 import analysis as routes
    from app.core.exceptions import NotFoundError
    from app.schemas.trace import TraceResponse

    client, session, *_ = api
    read = AsyncMock(return_value=TraceResponse(run_id="run-1", next_cursor=7))
    monkeypatch.setattr(routes, "TraceService", lambda: SimpleNamespace(read=read))
    result = client.get("/api/v1/analysis/run-1/trace?after=7&limit=20")
    assert result.status_code == 200
    assert result.json()["next_cursor"] == 7
    read.assert_awaited_once_with(session, "run-1", 7, 20)
    assert client.get("/api/v1/analysis/run-1/trace?after=-1").status_code == 422
    assert client.get("/api/v1/analysis/run-1/trace?limit=201").status_code == 422
    read.side_effect = NotFoundError("Analysis run not found.")
    assert client.get("/api/v1/analysis/missing/trace").status_code == 404


@pytest.mark.parametrize(
    "action", ("approve", "pause", "resume", "retry", "cancel", "replan")
)
def test_lifecycle_routes_preserve_arguments(api, action):
    client, session, analysis, _, response = api
    method = getattr(analysis, f"{action}_analysis")
    method.return_value = response
    body = {"question": "新的问题"} if action == "replan" else None
    result = client.post(f"/api/v1/analysis/run-1/{action}", json=body)
    assert result.status_code == 200
    assert method.await_args.args[:2] == (session, "run-1")
    if action == "replan":
        assert method.await_args.args[2].question == "新的问题"


@pytest.mark.parametrize(
    ("suffix", "method", "payload"),
    (
        ("report", "get_report", {"report": {"content": "# 报告"}}),
        ("report/json", "get_report_json", {"document": {"schema_version": 1}}),
    ),
)
def test_report_routes_use_report_service(api, suffix, method, payload):
    client, session, analysis, reports, _ = api
    operation = getattr(reports, method)
    operation.return_value = {"run_id": "run-1", "status": "COMPLETED", **payload}
    result = client.get(f"/api/v1/analysis/run-1/{suffix}")
    assert result.status_code == 200
    assert result.json() == operation.return_value
    operation.assert_awaited_once_with(session, "run-1")
    assert analysis.mock_calls == []


def test_error_response_remains_compatible(api):
    client, _, _, reports, _ = api
    reports.get_report.side_effect = ValidationError("Analysis run not found: missing")
    result = client.get("/api/v1/analysis/missing/report")
    assert result.status_code == 400
    assert result.json() == {
        "success": False,
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Analysis run not found: missing",
        },
    }


def test_invalid_request_does_not_reach_service(api):
    client, _, analysis, _, _ = api
    assert client.post("/api/v1/analysis", json={}).status_code == 422
    analysis.create_analysis.assert_not_awaited()
