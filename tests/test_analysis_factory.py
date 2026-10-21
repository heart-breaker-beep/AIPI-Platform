"""组合根显式注入存储与节点提交策略。"""

import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest

from app.services.analysis_factory import create_analysis_workflow
from app.workflow.state import WorkflowState


def test_application_and_context_work_without_vector_sdks():
    """Fresh import must work even when removed SDKs cannot be imported."""
    result = subprocess.run(
        [sys.executable, "-c", """
import importlib.abc
import sys
from unittest.mock import Mock

class BlockVectorSDKs(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'qdrant_client', 'ollama', 'sentence_transformers'}:
            raise ModuleNotFoundError('Removed SDK: ' + fullname)

sys.meta_path.insert(0, BlockVectorSDKs())
from app.main import app
from app.services.analysis_factory import WorkflowContextFactory
context = WorkflowContextFactory(Mock()).create(7)
assert context.evidence_store is not None
assert context.context_manager is not None
assert 'rag_retrieval' not in context.tools
assert app.openapi()['components']['schemas']['AnalysisCreateRequest']['properties']['enable_rag']['deprecated']
"""],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.asyncio
async def test_checkpoint_commits_after_storage_and_context_hides_session(
    monkeypatch, tmp_path
):
    monkeypatch.chdir(tmp_path)
    events = []
    session = SimpleNamespace(
        add=Mock(side_effect=lambda record: events.append("add")),
        flush=AsyncMock(side_effect=lambda: events.append("flush")),
        commit=AsyncMock(side_effect=lambda: events.append("commit")),
    )
    workflow = create_analysis_workflow(session)
    context = workflow.context_factory.create(7)
    assert "rag_retrieval" not in context.tools
    assert context.memory_manager is not None
    assert context.config == {"repository_id": 7}
    assert context.evidence_store.evidence_repository.session is session

    state = WorkflowState(run_id="run-1")
    await workflow.checkpoint_manager.save(state)
    assert events == ["add", "flush", "commit"]
    assert state.checkpoint_version == 1
    session.commit.assert_awaited_once()
