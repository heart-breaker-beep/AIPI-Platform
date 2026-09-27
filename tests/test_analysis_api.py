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