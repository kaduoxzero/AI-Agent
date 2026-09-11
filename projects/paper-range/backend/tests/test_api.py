from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_session_and_execute_action() -> None:
    created = client.post("/api/sessions", json={"scenario_id": "corp-intranet"})
    assert created.status_code == 201
    session = created.json()

    action = client.post(
        f"/api/sessions/{session['id']}/actions",
        json={"input": f"nmap -p- {session['target_ip']}"},
    )
    assert action.status_code == 200
    payload = action.json()
    assert payload["action"] == "scan_ports"
    assert payload["session"]["completed_objectives"] == ["scan"]


def test_random_session_works() -> None:
    created = client.post("/api/sessions", json={})
    assert created.status_code == 201
    assert created.json()["scenario_id"] in {"abandoned-lab", "corp-intranet", "underground-market"}
