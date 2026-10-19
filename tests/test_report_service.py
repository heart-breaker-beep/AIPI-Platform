"""报告服务拆分后保留文件兜底和检查点重建行为。"""

import json
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.core.exceptions import ValidationError
from app.services import report_service as module


@pytest.fixture
def reports(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    run_repo = SimpleNamespace(
        get_by_id=AsyncMock(
            return_value=SimpleNamespace(id="run-1", status="COMPLETED")
        )
    )
    checkpoint = SimpleNamespace(get_latest=AsyncMock(return_value=None))
    monkeypatch.setattr(module, "AnalysisRunRepository", lambda session: run_repo)
    monkeypatch.setattr(module, "CheckpointRepository", lambda session: checkpoint)
    return module.ReportService(), run_repo, checkpoint


@pytest.mark.asyncio
async def test_json_file_is_read_when_checkpoint_is_unavailable(reports, tmp_path):
    service, _, checkpoint = reports
    checkpoint.get_latest.side_effect = RuntimeError("checkpoint unavailable")
    directory = tmp_path / "reports"
    directory.mkdir()
    document = {"schema_version": 1, "project": {"name": "demo"}}
    (directory / "run-1_analysis.json").write_text(
        json.dumps(document), encoding="utf-8"
    )
    result = await service.get_report_json(object(), "run-1")
    assert result.document == document


@pytest.mark.asyncio
async def test_corrupt_json_is_rebuilt_from_checkpoint(reports, tmp_path):
    service, _, checkpoint = reports
    path = tmp_path / "broken.json"
    path.write_text("{broken", encoding="utf-8")
    checkpoint.get_latest.return_value = SimpleNamespace(
        data={
            "run_id": "run-1",
            "question": "分析项目",
            "final_report": {"json_report": {"path": str(path)}},
        }
    )
    result = await service.get_report_json(object(), "run-1")
    assert result.document["schema_version"] == 1
    assert result.document["run_id"] == "run-1"


@pytest.mark.asyncio
async def test_markdown_file_survives_missing_checkpoint(reports, tmp_path):
    service, _, checkpoint = reports
    checkpoint.get_latest.side_effect = RuntimeError("checkpoint unavailable")
    directory = tmp_path / "reports"
    directory.mkdir()
    (directory / "run-1_analysis.md").write_text("# 已完成的报告", encoding="utf-8")
    result = await service.get_report(object(), "run-1")
    assert result.report["content"] == "# 已完成的报告"


@pytest.mark.asyncio
async def test_missing_report_returns_empty_document(reports):
    service, _, _ = reports
    assert (await service.get_report_json(object(), "run-1")).document is None


@pytest.mark.asyncio
async def test_unknown_run_is_rejected_before_reading_checkpoint(reports):
    service, runs, checkpoint = reports
    runs.get_by_id.return_value = None
    with pytest.raises(ValidationError):
        await service.get_report_json(object(), "missing")
    checkpoint.get_latest.assert_not_awaited()
