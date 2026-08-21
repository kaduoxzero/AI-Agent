from __future__ import annotations

import asyncio
from typing import Protocol

from sqlalchemy import JSON, String, UniqueConstraint, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from packages.contracts import TaskCreate, TaskRecord


class TaskRepository(Protocol):
    async def initialize(self) -> None: ...
    async def create(self, command: TaskCreate) -> tuple[TaskRecord, bool]: ...
    async def get(self, task_id: str) -> TaskRecord | None: ...
    async def save(self, task: TaskRecord) -> TaskRecord: ...
    async def list_by_tenant(self, tenant_id: str, limit: int = 100) -> list[TaskRecord]: ...
    async def close(self) -> None: ...


class InMemoryTaskRepository:
    def __init__(self) -> None:
        self._items: dict[str, TaskRecord] = {}
        self._idempotency: dict[tuple[str, str], str] = {}
        self._lock = asyncio.Lock()

    async def initialize(self) -> None:
        return None

    async def create(self, command: TaskCreate) -> tuple[TaskRecord, bool]:
        async with self._lock:
            if command.idempotency_key:
                existing_id = self._idempotency.get((command.tenant_id, command.idempotency_key))
                if existing_id:
                    return self._items[existing_id], False
            task = TaskRecord.from_create(command)
            self._items[task.task_id] = task
            if command.idempotency_key:
                self._idempotency[(command.tenant_id, command.idempotency_key)] = task.task_id
            return task, True

    async def get(self, task_id: str) -> TaskRecord | None:
        async with self._lock:
            return self._items.get(task_id)

    async def save(self, task: TaskRecord) -> TaskRecord:
        async with self._lock:
            self._items[task.task_id] = task
        return task

    async def list_by_tenant(self, tenant_id: str, limit: int = 100) -> list[TaskRecord]:
        async with self._lock:
            items = [item for item in self._items.values() if item.tenant_id == tenant_id]
        items.sort(key=lambda item: item.created_at, reverse=True)
        return items[:limit]

    async def close(self) -> None:
        return None


class Base(DeclarativeBase):
    pass


class TaskRow(Base):
    __tablename__ = "agent_tasks"
    __table_args__ = (
        UniqueConstraint("tenant_id", "idempotency_key", name="uq_task_tenant_idempotency"),
    )

    task_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(128), index=True)
    idempotency_key: Mapped[str | None] = mapped_column(String(200), nullable=True)
    status: Mapped[str] = mapped_column(String(32), index=True)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)


class PostgresTaskRepository:
    """Compact durable repository using a typed JSON payload plus indexed columns.

    A mature platform should manage this schema with Alembic migrations and can
    normalize additional query-heavy fields without changing the domain interface.
    """

    def __init__(self, database_url: str) -> None:
        self.engine = create_async_engine(database_url, pool_pre_ping=True)
        self.sessions: async_sessionmaker[AsyncSession] = async_sessionmaker(
            self.engine, expire_on_commit=False
        )

    async def initialize(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def create(self, command: TaskCreate) -> tuple[TaskRecord, bool]:
        async with self.sessions() as session:
            if command.idempotency_key:
                result = await session.execute(
                    select(TaskRow).where(
                        TaskRow.tenant_id == command.tenant_id,
                        TaskRow.idempotency_key == command.idempotency_key,
                    )
                )
                existing = result.scalar_one_or_none()
                if existing:
                    return TaskRecord.model_validate(existing.payload), False

            task = TaskRecord.from_create(command)
            row = TaskRow(
                task_id=task.task_id,
                tenant_id=task.tenant_id,
                idempotency_key=task.idempotency_key,
                status=task.status.value,
                payload=task.model_dump(mode="json"),
            )
            session.add(row)
            await session.commit()
            return task, True

    async def get(self, task_id: str) -> TaskRecord | None:
        async with self.sessions() as session:
            row = await session.get(TaskRow, task_id)
            return TaskRecord.model_validate(row.payload) if row else None

    async def save(self, task: TaskRecord) -> TaskRecord:
        payload = task.model_dump(mode="json")
        async with self.sessions() as session:
            row = await session.get(TaskRow, task.task_id)
            if row is None:
                row = TaskRow(
                    task_id=task.task_id,
                    tenant_id=task.tenant_id,
                    idempotency_key=task.idempotency_key,
                    status=task.status.value,
                    payload=payload,
                )
                session.add(row)
            else:
                row.tenant_id = task.tenant_id
                row.idempotency_key = task.idempotency_key
                row.status = task.status.value
                row.payload = payload
            await session.commit()
        return task

    async def list_by_tenant(self, tenant_id: str, limit: int = 100) -> list[TaskRecord]:
        async with self.sessions() as session:
            result = await session.execute(
                select(TaskRow)
                .where(TaskRow.tenant_id == tenant_id)
                .order_by(TaskRow.task_id.desc())
                .limit(limit)
            )
            return [TaskRecord.model_validate(row.payload) for row in result.scalars()]

    async def close(self) -> None:
        await self.engine.dispose()
