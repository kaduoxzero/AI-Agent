from __future__ import annotations

import asyncio
from typing import Protocol

from redis.asyncio import Redis

from packages.contracts import RuntimeCheckpoint


class CheckpointStore(Protocol):
    async def save(self, checkpoint: RuntimeCheckpoint) -> None: ...
    async def get(self, task_id: str) -> RuntimeCheckpoint | None: ...
    async def delete(self, task_id: str) -> None: ...
    async def close(self) -> None: ...


class InMemoryCheckpointStore:
    def __init__(self) -> None:
        self._items: dict[str, RuntimeCheckpoint] = {}
        self._lock = asyncio.Lock()

    async def save(self, checkpoint: RuntimeCheckpoint) -> None:
        async with self._lock:
            self._items[checkpoint.task_id] = checkpoint

    async def get(self, task_id: str) -> RuntimeCheckpoint | None:
        async with self._lock:
            return self._items.get(task_id)

    async def delete(self, task_id: str) -> None:
        async with self._lock:
            self._items.pop(task_id, None)

    async def close(self) -> None:
        return None


class RedisCheckpointStore:
    def __init__(self, redis_url: str, prefix: str = "agent-platform:checkpoint") -> None:
        self.redis = Redis.from_url(redis_url, decode_responses=True)
        self.prefix = prefix

    def _key(self, task_id: str) -> str:
        return f"{self.prefix}:{task_id}"

    async def save(self, checkpoint: RuntimeCheckpoint) -> None:
        await self.redis.set(self._key(checkpoint.task_id), checkpoint.model_dump_json())

    async def get(self, task_id: str) -> RuntimeCheckpoint | None:
        raw = await self.redis.get(self._key(task_id))
        return RuntimeCheckpoint.model_validate_json(raw) if raw else None

    async def delete(self, task_id: str) -> None:
        await self.redis.delete(self._key(task_id))

    async def close(self) -> None:
        await self.redis.aclose()
