from fastapi.testclient import TestClient

from apps.api.main import app


client = TestClient(app)
TENANT_A = {"X-Tenant-ID": "tenant-a", "X-User-ID": "user-001"}
TENANT_B = {"X-Tenant-ID": "tenant-b", "X-User-ID": "user-002"}


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["database"] == "memory"
    assert body["queue"] == "memory"
    assert body["artifact_store"] == "memory"


def test_identity_is_required() -> None:
    response = client.post("/tasks", json={"query": "分析供应商风险"})
    assert response.status_code == 401


def test_create_get_cancel_and_events() -> None:
    created = client.post(
        "/tasks",
        headers=TENANT_A,
        json={"query": "分析供应商风险"},
    )
    assert created.status_code == 202
    task = created.json()
    assert task["status"] == "PENDING"
    assert task["tenant_id"] == "tenant-a"
    assert task["user_id"] == "user-001"
    assert task["trace_id"]

    task_id = task["task_id"]
    fetched = client.get(f"/tasks/{task_id}", headers=TENANT_A)
    assert fetched.status_code == 200
    assert fetched.json()["task_id"] == task_id

    events = client.get(f"/tasks/{task_id}/events", headers=TENANT_A)
    assert events.status_code == 200
    assert events.json()[0]["event_type"] == "TaskCreated"

    cancelled = client.post(f"/tasks/{task_id}/cancel", headers=TENANT_A)
    assert cancelled.status_code == 200
    assert cancelled.json()["status"] == "CANCELLING"
    assert cancelled.json()["cancel_requested"] is True


def test_cross_tenant_access_returns_404() -> None:
    created = client.post(
        "/tasks",
        headers=TENANT_A,
        json={"query": "内部风险分析"},
    )
    task_id = created.json()["task_id"]
    assert client.get(f"/tasks/{task_id}", headers=TENANT_B).status_code == 404
    assert client.get(f"/tasks/{task_id}/events", headers=TENANT_B).status_code == 404


def test_idempotency_key_returns_same_task_without_duplicate_event() -> None:
    headers = {**TENANT_A, "Idempotency-Key": "same-request-001"}
    first = client.post("/tasks", headers=headers, json={"query": "幂等请求"})
    second = client.post("/tasks", headers=headers, json={"query": "幂等请求"})
    assert first.status_code == 202
    assert second.status_code == 202
    assert first.json()["task_id"] == second.json()["task_id"]

    events = client.get(
        f"/tasks/{first.json()['task_id']}/events",
        headers=TENANT_A,
    ).json()
    assert [event["event_type"] for event in events].count("TaskCreated") == 1


def test_list_tasks_is_tenant_scoped() -> None:
    client.post("/tasks", headers=TENANT_A, json={"query": "A-only"})
    client.post("/tasks", headers=TENANT_B, json={"query": "B-only"})
    items = client.get("/tasks", headers=TENANT_A).json()
    assert items
    assert all(item["tenant_id"] == "tenant-a" for item in items)


def test_missing_task_returns_404() -> None:
    response = client.get("/tasks/does-not-exist", headers=TENANT_A)
    assert response.status_code == 404
