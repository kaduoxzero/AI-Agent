from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_session_and_execute_action() -> None:
    created = client.post("/api/sessions", json={"scenario_id": "corp-intranet"})
    assert created.status_code == 201
    session = created.json()
    assert session["score"] == 100

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


def test_random_session_works() -> None:
    created = client.post("/api/sessions", json={})
    assert created.status_code == 201
    assert created.json()["scenario_id"] in {"abandoned-lab", "corp-intranet", "underground-market"}
