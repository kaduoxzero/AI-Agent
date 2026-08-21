from __future__ import annotations

import asyncio
from typing import Any, Protocol

from redis.asyncio import Redis

from packages.contracts import TaskEvent


class EventStore(Protocol):
    async def publish(self, task_id: str, event_type: str, **data: Any) -> TaskEvent: ...
    async def list(self, task_id: str, start: int = 0) -> list[TaskEvent]: ...
    async def close(self) -> None: ...


class InMemoryEventStore:
    def __init__(self) -> None:
        self._items: dict[str, list[TaskEvent]] = {}
        self._lock = asyncio.Lock()

    async def publish(self, task_id: str, event_type: str, **data: Any) -> TaskEvent:
        event = TaskEvent(task_id=task_id, event_type=event_type, data=data)
        async with self._lock:
            self._items.setdefault(task_id, []).append(event)
        return event

    async def list(self, task_id: str, start: int = 0) -> list[TaskEvent]:
        async with self._lock:
            return list(self._items.get(task_id, [])[start:])

    async def close(self) -> None:
        return None


class RedisEventStore:
    def __init__(self, redis_url: str, key_prefix: str) -> None:
        self.redis = Redis.from_url(redis_url, decode_responses=True)
        self.key_prefix = key_prefix

    def _key(self, task_id: str) -> str:
        return f"{self.key_prefix}:{task_id}"

    async def publish(self, task_id: str, event_type: str, **data: Any) -> TaskEvent:
        event = TaskEvent(task_id=task_id, event_type=event_type, data=data)
        await self.redis.rpush(self._key(task_id), event.model_dump_json())
        return event

    async def list(self, task_id: str, start: int = 0) -> list[TaskEvent]:
        raw = await self.redis.lrange(self._key(task_id), start, -1)
        return [TaskEvent.model_validate_json(item) for item in raw]

    async def close(self) -> None:
        await self.redis.aclose()
