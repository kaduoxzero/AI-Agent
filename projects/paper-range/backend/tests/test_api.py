from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_scenario_catalog_exposes_only_public_metadata() -> None:
    response = client.get("/api/scenarios")
    assert response.status_code == 200
    scenarios = response.json()
    assert len(scenarios) == 6

    sample = scenarios[0]
    assert "id" in sample
    assert "objectives" in sample
    assert "ssh_user" in sample
    assert "ssh_password" not in sample
    assert "flag" not in sample
    assert "hidden_paths" not in sample
    assert "evidence_text" not in sample
    assert "web_observation" not in sample


def test_create_session_and_execute_action() -> None:
    created = client.post("/api/sessions", json={"scenario_id": "corp-intranet"})
    assert created.status_code == 201
    session = created.json()
    assert session["score"] == 100
    assert session["evidence_strategy"] is None
    assert session["investigation_checks"] == []

    action = client.post(
        f"/api/sessions/{session['id']}/actions",
        json={"input": f"nmap -p- {session['target_ip']}"},
    )
    assert action.status_code == 200
    payload = action.json()
    assert payload["intent"]["kind"] == "scan_ports"
    assert payload["session"]["completed_objectives"] == ["scan"]


def test_hint_and_report_endpoints() -> None:
    created = client.post("/api/sessions", json={"scenario_id": "abandoned-lab"}).json()
    session_id = created["id"]

    hint = client.post(f"/api/sessions/{session_id}/hint")
    assert hint.status_code == 200
    assert hint.json()["cost"] == 10
    assert hint.json()["session"]["score"] == 90

    report = client.get(f"/api/sessions/{session_id}/report")
    assert report.status_code == 200
    assert report.json()["status"] == "active"
    assert report.json()["grade"] == "A"
    assert report.json()["investigation_checks"] == []


def test_random_session_works_across_six_scenarios() -> None:
    created = client.post("/api/sessions", json={})
    assert created.status_code == 201
    assert created.json()["scenario_id"] in {
        "abandoned-lab",
        "corp-intranet",
        "underground-market",
        "municipal-archive",
        "orbital-relay",
        "night-freight",
    }


def test_investigation_v2_release_and_missing_event_stream() -> None:
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["version"] == "0.6.0"
    assert health.json()["persistence"] == "process-memory-only"

    openapi = client.get("/openapi.json")
    assert openapi.status_code == 200
    assert openapi.json()["info"]["version"] == "0.6.0"

    missing = client.get("/api/sessions/not-a-session/events")
    assert missing.status_code == 404
    assert missing.json()["detail"] == "session not found"
