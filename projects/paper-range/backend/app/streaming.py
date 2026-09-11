from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncIterator
from typing import Protocol

from .models import GameEvent
from .runtime import SessionStore


POLL_INTERVAL_SECONDS = 0.25
EVENT_STAGGER_SECONDS = 0.08
HEARTBEAT_INTERVAL_SECONDS = 10.0


class DisconnectProbe(Protocol):
    async def is_disconnected(self) -> bool: ...


def encode_sse_event(event: GameEvent) -> str:
    """Encode a game event using the browser EventSource wire format."""

    return f"id: {event.seq}\nevent: game_event\ndata: {event.model_dump_json()}\n\n"


def encode_sse_control(event_name: str, payload: dict[str, object]) -> str:
    data = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    return f"event: {event_name}\ndata: {data}\n\n"


def resolve_event_cursor(after: int, last_event_id: str | None) -> int:
    cursor = max(0, after)
    if last_event_id and last_event_id.isdigit():
        cursor = max(cursor, int(last_event_id))
    return cursor


async def session_event_stream(
    store: SessionStore,
    session_id: str,
    disconnect_probe: DisconnectProbe,
    *,
    after: int = 0,
) -> AsyncIterator[str]:
    """Stream process-local GameEvents without introducing persistent state.

    The stream polls the in-memory SessionStore, replays events after the supplied
    cursor and staggers each frame slightly so narrative/agent feedback can render
    progressively in the browser. No external network activity is performed.
    """

    cursor = max(0, after)
    loop = asyncio.get_running_loop()
    last_activity = loop.time()

    while True:
        if await disconnect_probe.is_disconnected():
            return

        try:
            session = store.get(session_id)
        except KeyError:
            yield encode_sse_control("session_end", {"reason": "session_not_found"})
            return

        pending = [event for event in session.events if event.seq > cursor]
        if pending:
            for event in pending:
                if await disconnect_probe.is_disconnected():
                    return
                cursor = event.seq
                yield encode_sse_event(event)
                await asyncio.sleep(EVENT_STAGGER_SECONDS)

            last_activity = loop.time()
            if session.status == "completed" and cursor >= session.events[-1].seq:
                yield encode_sse_control(
                    "session_complete",
                    {"session_id": session.id, "last_event_id": cursor},
                )
                return
            continue

        if session.status == "completed":
            yield encode_sse_control(
                "session_complete",
                {"session_id": session.id, "last_event_id": cursor},
            )
            return

        now = loop.time()
        if now - last_activity >= HEARTBEAT_INTERVAL_SECONDS:
            yield ": heartbeat\n\n"
            last_activity = now

        await asyncio.sleep(POLL_INTERVAL_SECONDS)
