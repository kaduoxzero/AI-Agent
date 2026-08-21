from fastapi.testclient import TestClient

from apps.api.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["database"] == "memory"
    assert body["queue"] == "memory"


def test_create_get_cancel_and_events() -> None:
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
    assert task["trace_id"]

    task_id = task["task_id"]
    fetched = client.get(f"/tasks/{task_id}")
    assert fetched.status_code == 200
    assert fetched.json()["task_id"] == task_id

    events = client.get(f"/tasks/{task_id}/events")
    assert events.status_code == 200
    assert events.json()[0]["event_type"] == "TaskCreated"

    cancelled = client.post(f"/tasks/{task_id}/cancel")
    assert cancelled.status_code == 200
    assert cancelled.json()["status"] == "CANCELLING"
    assert cancelled.json()["cancel_requested"] is True


def test_missing_task_returns_404() -> None:
    response = client.get("/tasks/does-not-exist")
    assert response.status_code == 404
