"""Analysis API 测试。"""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"


def test_create_analysis():

    response = client.post(
        "/api/v1/analysis",
        json={
            "repo_url":
                "https://github.com/openai/openai-python",
            "question":
                "分析这个项目的 Agent 和 Workflow",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "run_id" in data

    assert (
        data["status"]
        == "WAITING_DESIGN"
    )

    assert (
        data["current_node"]
        == "design_gate"
    )

    assert (
        data["progress"]
        == 20
    )

    assert (
        data["repo_url"]
        == "https://github.com/openai/openai-python"
    )


def test_get_analysis():

    create_response = client.post(
        "/api/v1/analysis",
        json={
            "repo_url":
                "https://github.com/openai/openai-python",
            "question":
                "分析项目架构",
        },
    )

    assert (
        create_response.status_code
        == 200
    )

    run_id = (
        create_response
        .json()["run_id"]
    )

    response = client.get(
        f"/api/v1/analysis/{run_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["run_id"]
        == run_id
    )

    assert (
        data["status"]
        == "WAITING_DESIGN"
    )

    assert (
        data["current_node"]
        == "design_gate"
    )


def test_invalid_repository_url():

    response = client.post(
        "/api/v1/analysis",
        json={
            "repo_url":
                "https://example.com/test"
        },
    )

    assert response.status_code == 400

    data = response.json()

    assert data["success"] is False

    assert (
        data["error"]["code"]
        == "VALIDATION_ERROR"
    )


def test_analysis_not_found():

    response = client.get(
        "/api/v1/analysis/not-exist-run-id"
    )

    assert response.status_code == 400

    data = response.json()

    assert data["success"] is False

    assert (
        data["error"]["code"]
        == "VALIDATION_ERROR"
    )

def test_parse_github_url_strips_query_string():
    """
    带 query string 的 GitHub URL 必须被正确解析。

    旧实现按 "/" 朴素切分，
    会把 "?utm_source=chatgpt.com" 当成 repository name 的一部分，
    导致 README 与配置文件全部 404、
    证据为 0、technology_stack 全空，
    而该 run 仍然被标记为 COMPLETED。
    """

    from app.services.analysis_service import (
        AnalysisService,
    )

    owner, name = AnalysisService._parse_github_url(
        "https://github.com/smlfy/"
        "enterprise-workflow-agent-platform"
        "?utm_source=chatgpt.com"
    )

    assert owner == "smlfy"

    assert name == "enterprise-workflow-agent-platform"


def test_parse_github_url_handles_common_forms():
    """常见的 URL 写法都要能解析。"""

    from app.services.analysis_service import (
        AnalysisService,
    )

    cases = [
        (
            "https://github.com/openai/openai-python",
            ("openai", "openai-python"),
        ),
        (
            "https://github.com/openai/openai-python.git",
            ("openai", "openai-python"),
        ),
        (
            "https://github.com/openai/openai-python/",
            ("openai", "openai-python"),
        ),
        (
            "https://github.com/openai/openai-python"
            "?tab=readme-ov-file#install",
            ("openai", "openai-python"),
        ),
    ]

    for url, expected in cases:
        assert (
            AnalysisService._parse_github_url(url)
            == expected
        ), url


def test_parse_github_url_rejects_non_github():
    """非 GitHub 域名必须抛业务异常（→ HTTP 400）。"""

    import pytest

    from app.core.exceptions import ValidationError
    from app.services.analysis_service import (
        AnalysisService,
    )

    with pytest.raises(ValidationError):
        AnalysisService._parse_github_url(
            "https://example.com/owner/name"
        )
