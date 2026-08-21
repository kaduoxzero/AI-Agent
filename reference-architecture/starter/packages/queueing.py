from __future__ import annotations

import asyncio
import os
import socket
from dataclasses import dataclass
from typing import Protocol
from uuid import uuid4

from redis.asyncio import Redis
from redis.exceptions import ResponseError


@dataclass(frozen=True)
class ReservedTask:
    message_id: str
    task_id: str


class TaskQueue(Protocol):
    async def initialize(self) -> None: ...
    async def enqueue(self, task_id: str) -> None: ...
    async def reserve(self, timeout: int = 2) -> ReservedTask | None: ...
    async def ack(self, message: ReservedTask) -> None: ...
    async def close(self) -> None: ...


class InMemoryTaskQueue:
    def __init__(self) -> None:
        self._queue: asyncio.Queue[str] = asyncio.Queue()

    async def initialize(self) -> None:
        return None

    async def enqueue(self, task_id: str) -> None:
        await self._queue.put(task_id)

    async def reserve(self, timeout: int = 2) -> ReservedTask | None:
        try:
            task_id = await asyncio.wait_for(self._queue.get(), timeout=timeout)
            return ReservedTask(message_id=task_id, task_id=task_id)
        except TimeoutError:
            return None

    async def ack(self, message: ReservedTask) -> None:
        self._queue.task_done()

    async def close(self) -> None:
        return None


class RedisTaskQueue:
    """Redis Streams queue with consumer groups and stale-message recovery.

    Compared with BLPOP, a Stream message remains pending until XACK. If a worker
    crashes after reserving a task, another worker can reclaim the stale message.
    """

    def __init__(
        self,
        redis_url: str,
        queue_name: str,
        group_name: str = "agent-workers",
        stale_after_ms: int = 60_000,
    ) -> None:
        self.redis = Redis.from_url(redis_url, decode_responses=True)
        self.stream = queue_name
        self.group = group_name
        self.stale_after_ms = stale_after_ms
        self.consumer = f"{socket.gethostname()}-{os.getpid()}-{uuid4().hex[:8]}"

    async def initialize(self) -> None:
        try:
            await self.redis.xgroup_create(
                self.stream,
                self.group,
                id="0",
                mkstream=True,
            )
        except ResponseError as exc:
            if "BUSYGROUP" not in str(exc):
                raise

    async def enqueue(self, task_id: str) -> None:
        await self.redis.xadd(self.stream, {"task_id": task_id})

    async def _claim_stale(self) -> ReservedTask | None:
        result = await self.redis.xautoclaim(
            self.stream,
            self.group,
            self.consumer,
            min_idle_time=self.stale_after_ms,
            start_id="0-0",
            count=1,
        )
        # redis-py returns (next_start_id, [(message_id, fields)], deleted_ids?)
        messages = result[1] if len(result) >= 2 else []
        if not messages:
            return None
        message_id, fields = messages[0]
        return ReservedTask(message_id=message_id, task_id=fields["task_id"])

    async def reserve(self, timeout: int = 2) -> ReservedTask | None:
        reclaimed = await self._claim_stale()
        if reclaimed is not None:
            return reclaimed

        response = await self.redis.xreadgroup(
            self.group,
            self.consumer,
            streams={self.stream: ">"},
            count=1,
            block=max(timeout, 1) * 1000,
        )
        if not response:
            return None
        _, messages = response[0]
        message_id, fields = messages[0]
        return ReservedTask(message_id=message_id, task_id=fields["task_id"])

    async def ack(self, message: ReservedTask) -> None:
        await self.redis.xack(self.stream, self.group, message.message_id)

    async def close(self) -> None:
        await self.redis.aclose()
