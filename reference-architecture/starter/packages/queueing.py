from __future__ import annotations

import asyncio
from typing import Protocol

from redis.asyncio import Redis


class TaskQueue(Protocol):
    async def enqueue(self, task_id: str) -> None: ...
    async def dequeue(self, timeout: int = 2) -> str | None: ...
    async def close(self) -> None: ...


class InMemoryTaskQueue:
    def __init__(self) -> None:
        self._queue: asyncio.Queue[str] = asyncio.Queue()

    async def enqueue(self, task_id: str) -> None:
        await self._queue.put(task_id)

    async def dequeue(self, timeout: int = 2) -> str | None:
        try:
            return await asyncio.wait_for(self._queue.get(), timeout=timeout)
        except TimeoutError:
            return None

    async def close(self) -> None:
        return None


class RedisTaskQueue:
    def __init__(self, redis_url: str, queue_name: str) -> None:
        self.redis = Redis.from_url(redis_url, decode_responses=True)
        self.queue_name = queue_name

    async def enqueue(self, task_id: str) -> None:
        await self.redis.rpush(self.queue_name, task_id)

    async def dequeue(self, timeout: int = 2) -> str | None:
        item = await self.redis.blpop(self.queue_name, timeout=timeout)
        if item is None:
            return None
        _, task_id = item
        return task_id

    async def close(self) -> None:
        await self.redis.aclose()
