from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class MemoryItem:
    tenant_id: str
    user_id: str
    key: str
    value: str
    source: str
    created_at: datetime


class InMemoryMemoryStore:
    """Reference memory with an explicit trusted-write boundary.

    Web pages/tool results are not automatically persisted. A production version
    should add durable storage, TTL, conflict resolution and user controls.
    """

    TRUSTED_SOURCES = {"user_confirmed", "system", "business_record"}

    def __init__(self) -> None:
        self._items: dict[tuple[str, str, str], MemoryItem] = {}
        self._lock = asyncio.Lock()

    async def write(
        self,
        tenant_id: str,
        user_id: str,
        key: str,
        value: str,
        source: str,
    ) -> None:
        if source not in self.TRUSTED_SOURCES:
            raise PermissionError(f"untrusted memory source: {source}")
        item = MemoryItem(
            tenant_id=tenant_id,
            user_id=user_id,
            key=key,
            value=value,
            source=source,
            created_at=datetime.now(timezone.utc),
        )
        async with self._lock:
            self._items[(tenant_id, user_id, key)] = item

    async def get(self, tenant_id: str, user_id: str, key: str) -> MemoryItem | None:
        async with self._lock:
            return self._items.get((tenant_id, user_id, key))
