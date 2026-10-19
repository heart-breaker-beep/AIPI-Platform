"""验证移除领域转发层后，分析用例仍正确协调状态与工作流。"""

from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.analysis.workflow import AnalysisWorkflowOrchestrator
from app.core.exceptions import ValidationError
from app.schemas.analysis import AnalysisCreateRequest, AnalysisReplanRequest
from app.services import analysis_service as module
from app.workflow.state import WorkflowState, WorkflowStatus


@pytest.fixture
def analysis(monkeypatch):
    run = SimpleNamespace(
        id="run-1",
        repository_id=7,
        status="PAUSED",
        question="分析 workflow",
        current_node="design_gate",
        retry_count=0,
        error_message=None,
        created_at=datetime.now(timezone.utc),
    )
    repository = SimpleNamespace(
        id=7,
        url="https://github.com/demo/project",
        owner="demo",
        name="project",
    )
    session = SimpleNamespace(commit=AsyncMock())

    async def update_state(record, **fields):
        for key, value in fields.items():
            setattr(
                record,
                key,
                None if value is module.AnalysisRunRepository.CLEAR else value,
            )

    clear = module.AnalysisRunRepository.CLEAR
    runs = SimpleNamespace(
        get_by_id=AsyncMock(return_value=run),
        create=AsyncMock(return_value=run),
        update_runtime_state=AsyncMock(side_effect=update_state),
    )
    repositories = SimpleNamespace(
        get_by_id=AsyncMock(return_value=repository),
        get_by_url=AsyncMock(return_value=repository),
    )
    run_factory = lambda session: runs
    run_factory.CLEAR = clear
    monkeypatch.setattr(module, "AnalysisRunRepository", run_factory)
    monkeypatch.setattr(module, "RepositoryRepository", lambda session: repositories)
    monkeypatch.setattr(
        module,
        "CheckpointRepository",
        lambda session: SimpleNamespace(
            get_latest=AsyncMock(return_value=None),
        ),
    )
    workflow = AsyncMock(spec=AnalysisWorkflowOrchestrator)
    service = module.AnalysisService()
    monkeypatch.setattr(service, "_get_workflow", lambda session: workflow)
    return service, session, run, repository, workflow


@pytest.mark.asyncio
async def test_create_passes_complete_initial_data_directly_to_workflow(
    analysis, monkeypatch
):
    service, session, run, repository, workflow = analysis
    monkeypatch.setattr(module, "uuid4", lambda: "run-1")
    workflow.start_workflow.return_value = WorkflowState(
        run_id=run.id,
        status=WorkflowStatus.WAITING_DESIGN,
        current_node="design_gate",
    )
    request = AnalysisCreateRequest(
        repo_url=repository.url, question=run.question, enable_rag=True
    )
    response = await service.create_analysis(session, request)
    assert response.status == "WAITING_DESIGN"
    data = workflow.start_workflow.await_args.kwargs["initial_data"]
    assert data == {
        "run_id": "run-1",
        "repository_id": 7,
        "repo_url": repository.url,
        "owner": "demo",
        "repo": "project",
        "rag_enabled": True,
        "question": run.question,
    }
    assert session.commit.await_count == 2


@pytest.mark.parametrize(
    ("action", "initial", "final"),
    (
        ("approve", "WAITING_DESIGN", "COMPLETED"),
        ("pause", "ANALYZING", "PAUSED"),
        ("resume", "PAUSED", "COMPLETED"),
        ("retry", "FAILED", "COMPLETED"),
        ("cancel", "PAUSED", "CANCELED"),
        ("replan", "WAITING_DESIGN", "WAITING_DESIGN"),
    ),
)
@pytest.mark.asyncio
async def test_lifecycle_updates_run_and_preserves_identity(
    analysis, action, initial, final
):
    service, session, run, repository, workflow = analysis
    run.status = initial
    operation = getattr(workflow, f"{action}_workflow")
    operation.return_value = WorkflowState(
        run_id=run.id, status=final, current_node="design_gate"
    )
    args = [session, run.id]
    if action == "replan":
        args.append(AnalysisReplanRequest(question="新的分析问题"))
    response = await getattr(service, f"{action}_analysis")(*args)
    assert response.status == final
    assert run.status == final
    session.commit.assert_awaited()
    operation.assert_awaited_once()
    if action in ("approve", "resume", "retry"):
        assert operation.await_args.kwargs["identity"] == {
            "run_id": run.id,
            "repository_id": 7,
            "repo_url": repository.url,
            "owner": "demo",
            "repo": "project",
        }
    if action == "replan":
        assert run.question == "新的分析问题"
        assert operation.await_args.kwargs["question"] == "新的分析问题"


@pytest.mark.asyncio
async def test_invalid_approval_does_not_execute_workflow(analysis):
    service, session, run, _, workflow = analysis
    run.status = "COMPLETED"
    with pytest.raises(ValidationError):
        await service.approve_analysis(session, run.id)
    assert workflow.mock_calls == []
    session.commit.assert_not_awaited()
