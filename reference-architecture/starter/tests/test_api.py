from fastapi.testclient import TestClient

from apps.api.main import app


client = TestClient(app)
TENANT_A = {"X-Tenant-ID": "tenant-a", "X-User-ID": "user-001"}
TENANT_B = {"X-Tenant-ID": "tenant-b", "X-User-ID": "user-002"}
ADMIN = {"X-Platform-Admin": "true"}


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
    assert task["agent_id"] == "research-platform"
    assert task["agent_version"] == "1.0.0"
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


def test_control_plane_requires_admin_permission() -> None:
    assert client.get("/control-plane/agents").status_code == 403
    assert client.get("/control-plane/agents", headers=ADMIN).status_code == 200


def test_canary_release_is_blocked_until_eval_passes() -> None:
    definition = {
        "agent_id": "research-platform",
        "version": "2.0.0-test",
        "prompt_version": "research-v2-test",
        "model_route": "default",
        "allowed_tools": ["search_public_sources", "get_supplier_metrics"],
        "enabled": True,
    }
    assert client.post("/control-plane/agents", headers=ADMIN, json=definition).status_code == 200

    route = {
        "agent_id": "research-platform",
        "stable_version": "1.0.0",
        "canary_version": "2.0.0-test",
        "canary_percent": 100,
    }
    blocked = client.put(
        "/control-plane/releases/research-platform",
        headers=ADMIN,
        json=route,
    )
    assert blocked.status_code == 409

    eval_result = {
        "agent_id": "research-platform",
        "version": "2.0.0-test",
        "suite": "golden+security",
        "score": 0.95,
        "passed": True,
        "metrics": {"task_success": 0.96, "security": 1.0},
    }
    assert client.post("/control-plane/evals", headers=ADMIN, json=eval_result).status_code == 200
    released = client.put(
        "/control-plane/releases/research-platform",
        headers=ADMIN,
        json=route,
    )
    assert released.status_code == 200

    task = client.post(
        "/tasks",
        headers={**TENANT_A, "Idempotency-Key": "canary-test-request"},
        json={"query": "验证 canary 分配"},
    ).json()
    assert task["agent_version"] == "2.0.0-test"

    # Restore default route so the test suite does not leak mutable control-plane state.
    restore = {
        "agent_id": "research-platform",
        "stable_version": "1.0.0",
        "canary_version": None,
        "canary_percent": 0,
    }
    assert client.put(
        "/control-plane/releases/research-platform",
        headers=ADMIN,
        json=restore,
    ).status_code == 200
