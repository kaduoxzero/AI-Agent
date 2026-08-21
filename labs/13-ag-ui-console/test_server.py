from __future__ import annotations

import json

from fastapi.testclient import TestClient

from server import app


client = TestClient(app)


def test_event_stream_contains_required_lifecycle_and_state_events() -> None:
    with client.stream("GET", "/events") as response:
        assert response.status_code == 200
        events = []
        for line in response.iter_lines():
            if line.startswith("data: "):
                events.append(json.loads(line[len("data: ") :]))

    event_types = [event["type"] for event in events]

    assert event_types[0] == "RUN_STARTED"
    assert "STATE_SNAPSHOT" in event_types
    assert "TOOL_CALL_START" in event_types
    assert "TOOL_CALL_RESULT" in event_types
    assert "STATE_DELTA" in event_types
    assert "TEXT_MESSAGE_CONTENT" in event_types
    assert event_types[-1] == "RUN_FINISHED"
