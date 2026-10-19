"""组合根显式注入存储与节点提交策略。"""

from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest

from app.services import analysis_factory
from app.services.analysis_factory import create_analysis_workflow
from app.workflow.state import WorkflowState


@pytest.mark.asyncio
async def test_checkpoint_commits_after_storage_and_context_hides_session(
    monkeypatch, tmp_path
):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(analysis_factory, "QdrantVectorStore", lambda: object())
    monkeypatch.setattr(analysis_factory, "OllamaEmbedding", lambda: object())
    events = []
    session = SimpleNamespace(
        add=Mock(side_effect=lambda record: events.append("add")),
        flush=AsyncMock(side_effect=lambda: events.append("flush")),
        commit=AsyncMock(side_effect=lambda: events.append("commit")),
    )
    workflow = create_analysis_workflow(session)
    context = workflow.context_factory.create(7)
    assert context.config == {"repository_id": 7}
    assert context.evidence_store.evidence_repository.session is session

    state = WorkflowState(run_id="run-1")
    await workflow.checkpoint_manager.save(state)
    assert events == ["add", "flush", "commit"]
    assert state.checkpoint_version == 1
    session.commit.assert_awaited_once()
