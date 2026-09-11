import asyncio

from app.models import GameEvent
from app.runtime import SessionStore
from app.streaming import encode_sse_control, encode_sse_event, resolve_event_cursor, session_event_stream


class NeverDisconnect:
    async def is_disconnected(self) -> bool:
        return False


def test_sse_encoder_uses_sequence_as_event_id() -> None:
    event = GameEvent(seq=7, kind="agent", text="剧情事件")
    frame = encode_sse_event(event)

    assert frame.startswith("id: 7\nevent: game_event\n")
    assert '"kind":"agent"' in frame
    assert "剧情事件" in frame
    assert frame.endswith("\n\n")


def test_sse_control_and_cursor_support_eventsource_reconnect() -> None:
    assert resolve_event_cursor(4, "9") == 9
    assert resolve_event_cursor(4, "not-a-number") == 4
    assert resolve_event_cursor(-10, None) == 0

    frame = encode_sse_control("session_complete", {"last_event_id": 12})
    assert frame.startswith("event: session_complete\n")
    assert '"last_event_id":12' in frame


def test_session_event_stream_replays_only_events_after_cursor() -> None:
    store = SessionStore()
    session = store.create("abandoned-lab")

    async def read_one() -> str:
        stream = session_event_stream(store, session.id, NeverDisconnect(), after=2)
        try:
            return await anext(stream)
        finally:
            await stream.aclose()

    frame = asyncio.run(read_one())
    assert frame.startswith("id: 3\n")
    assert "任务：" in frame
