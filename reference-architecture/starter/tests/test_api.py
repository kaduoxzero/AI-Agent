from fastapi.testclient import TestClient

from apps.api.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_get_and_cancel_task() -> None:
    created = client.post(
        "/tasks",
        json={
            "tenant_id": "tenant-a",
            "user_id": "user-001",
            "query": "分析供应商风险",
        },
    )
    assert created.status_code == 202
    task = created.json()
    assert task["status"] == "PENDING"

    task_id = task["task_id"]
    fetched = client.get(f"/tasks/{task_id}")
    assert fetched.status_code == 200
    assert fetched.json()["task_id"] == task_id

    cancelled = client.post(f"/tasks/{task_id}/cancel")
    assert cancelled.status_code == 200
    assert cancelled.json()["status"] == "CANCELLED"


def test_missing_task_returns_404() -> None:
    response = client.get("/tasks/does-not-exist")
    assert response.status_code == 404
