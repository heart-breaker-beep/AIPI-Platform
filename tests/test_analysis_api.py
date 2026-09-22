"""Analysis API 测试，验证任务创建、查询和参数校验。"""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    """测试健康检查接口。"""

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"


def test_create_analysis():
    """测试创建 GitHub 项目分析任务。"""

    response = client.post(
        "/api/v1/analysis",
        json={
            "repo_url": "https://github.com/openai/openai-python"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "run_id" in data
    assert data["status"] == "pending"
    assert (
        data["repo_url"]
        == "https://github.com/openai/openai-python"
    )


def test_get_analysis():
    """测试根据 run_id 查询分析任务。"""

    # 先创建任务，再使用返回的 run_id 查询。
    # 这样可以验证创建和查询两个接口之间的数据链路。
    create_response = client.post(
        "/api/v1/analysis",
        json={
            "repo_url": "https://github.com/openai/openai-python"
        },
    )

    run_id = create_response.json()["run_id"]

    response = client.get(
        f"/api/v1/analysis/{run_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["run_id"] == run_id
    assert data["status"] == "pending"


def test_invalid_repository_url():
    """测试非法 Repository URL。"""

    response = client.post(
        "/api/v1/analysis",
        json={
            "repo_url": "https://example.com/test"
        },
    )

    assert response.status_code == 400

    data = response.json()

    assert data["success"] is False
    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_analysis_not_found():
    """测试查询不存在的分析任务。"""

    response = client.get(
        "/api/v1/analysis/not-exist-run-id"
    )

    assert response.status_code == 400

    data = response.json()

    assert data["success"] is False
    assert data["error"]["code"] == "VALIDATION_ERROR"