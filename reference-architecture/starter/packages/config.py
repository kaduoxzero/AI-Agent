from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_url: str | None = None
    redis_url: str | None = None
    task_queue_name: str = "agent-platform:tasks"
    event_key_prefix: str = "agent-platform:events"
    worker_poll_seconds: int = 2

    @property
    def durable_mode(self) -> bool:
        return bool(self.database_url and self.redis_url)

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            database_url=os.getenv("DATABASE_URL") or None,
            redis_url=os.getenv("REDIS_URL") or None,
            task_queue_name=os.getenv("TASK_QUEUE_NAME", "agent-platform:tasks"),
            event_key_prefix=os.getenv("EVENT_KEY_PREFIX", "agent-platform:events"),
            worker_poll_seconds=int(os.getenv("WORKER_POLL_SECONDS", "2")),
        )
