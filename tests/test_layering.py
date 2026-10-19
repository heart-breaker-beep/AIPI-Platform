"""目录迁移后的分层守卫，使用与命令行检查相同的规则。"""

import pytest

from scripts.check_dependencies import (
    APP_DIR,
    check_dependencies,
    check_file_imports,
    imported_modules,
)


def test_application_respects_layer_boundaries():
    assert check_dependencies() == []


@pytest.mark.parametrize(
    "layer",
    (
        "api",
        "services",
        "analysis",
        "workflow",
        "persistence",
        "integrations",
        "schemas",
        "core",
    ),
)
def test_layers_exist(layer):
    assert list((APP_DIR / layer).rglob("*.py"))


def test_guard_actually_inspects_code():
    modules = imported_modules(APP_DIR / "api" / "v1" / "analysis.py")
    assert "fastapi" in modules
    assert "app.services.analysis_service" in modules


@pytest.mark.parametrize(
    ("relative", "source"),
    (
        (
            "api/v1/bad.py",
            "from app.persistence.repositories.analysis_run import AnalysisRunRepository",
        ),
        (
            "analysis/skills/bad.py",
            "from app.services.analysis_service import AnalysisService",
        ),
        ("analysis/memory/bad.py", "from sqlalchemy import select"),
        (
            "analysis/skills/bad.py",
            "from ...persistence.session import AsyncSessionLocal",
        ),
        ("workflow/bad.py", "from app.analysis.skills.base import BaseSkill"),
        (
            "persistence/bad.py",
            "from app.analysis.workflow import build_analysis_workflow",
        ),
        (
            "integrations/bad.py",
            "from app.analysis.tools.project.analysis_focus import AnalysisFocus",
        ),
        ("services/bad.py", "from sqlalchemy import select"),
        ("services/bad.py", "import app.db.session"),
        ("persistence/bad.py", "from app import services"),
    ),
)
def test_guard_rejects_boundary_crossings(tmp_path, relative, source):
    app_dir = tmp_path / "app"
    path = app_dir / relative
    path.parent.mkdir(parents=True)
    path.write_text(source, encoding="utf-8")
    assert check_file_imports(path, app_dir)


def test_http_dependencies_can_open_sessions(tmp_path):
    app_dir = tmp_path / "app"
    path = app_dir / "api" / "dependencies.py"
    path.parent.mkdir(parents=True)
    path.write_text(
        "from app.persistence.session import AsyncSessionLocal", encoding="utf-8"
    )
    assert check_file_imports(path, app_dir) == []


def test_models_share_the_persistence_base():
    for path in (APP_DIR / "persistence" / "models").glob("*.py"):
        if path.name != "__init__.py":
            assert "app.persistence.base" in imported_modules(path)
