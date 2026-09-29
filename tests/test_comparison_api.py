"""Comparison API 测试。"""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(
    app
)


def test_comparison_route_exists():
    """
    验证 Comparison API 已经挂载。

    这里使用非法 Run ID，
    重点检查路由是否存在，而不是执行真实比较。
    """

    response = client.post(
        "/api/v1/comparison",
        json={
            "run_ids": [
                "run-a",
                "run-b",
            ]
        },
    )

    # 由于 run 不存在，
    # 应该进入统一业务异常处理，
    # 而不是 404 路由不存在。
    assert response.status_code != 404


def test_comparison_request_requires_two_runs():
    """必须提供两个 Run ID。"""

    response = client.post(
        "/api/v1/comparison",
        json={
            "run_ids": [
                "only-one-run"
            ]
        },
    )

    assert (
        response.status_code
        == 422
    )