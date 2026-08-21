from __future__ import annotations

import asyncio
from typing import Protocol

from sqlalchemy import JSON, String, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from packages.contracts import TaskCreate, TaskRecord


class TaskRepository(Protocol):
    async def initialize(self) -> None: ...
    async def create(self, command: TaskCreate) -> TaskRecord: ...
    async def get(self, task_id: str) -> TaskRecord | None: ...
    async def save(self, task: TaskRecord) -> TaskRecord: ...
    async def close(self) -> None: ...


class InMemoryTaskRepository:
    def __init__(self) -> None:
        self._items: dict[str, TaskRecord] = {}
        self._lock = asyncio.Lock()

    async def initialize(self) -> None:
        return None

    async def create(self, command: TaskCreate) -> TaskRecord:
        task = TaskRecord.from_create(command)
        async with self._lock:
            self._items[task.task_id] = task
        return task

    async def get(self, task_id: str) -> TaskRecord | None:
        async with self._lock:
            return self._items.get(task_id)

    async def save(self, task: TaskRecord) -> TaskRecord:
        async with self._lock:
            self._items[task.task_id] = task
        return task

    async def close(self) -> None:
        return None


class Base(DeclarativeBase):
    pass


class TaskRow(Base):
    __tablename__ = "agent_tasks"

    task_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(128), index=True)
    status: Mapped[str] = mapped_column(String(32), index=True)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)


class PostgresTaskRepository:
    """JSON payload keeps the starter compact while preserving a typed domain model.

    A mature platform can normalize frequently queried fields and add optimistic
    locking/version columns without changing the TaskRepository interface.
    """

    def __init__(self, database_url: str) -> None:
        self.engine = create_async_engine(database_url, pool_pre_ping=True)
        self.sessions: async_sessionmaker[AsyncSession] = async_sessionmaker(
            self.engine, expire_on_commit=False
        )

    async def initialize(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def create(self, command: TaskCreate) -> TaskRecord:
        task = TaskRecord.from_create(command)
        return await self.save(task)

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
                    status=task.status.value,
                    payload=payload,
                )
                session.add(row)
            else:
                row.tenant_id = task.tenant_id
                row.status = task.status.value
                row.payload = payload
            await session.commit()
        return task

    async def list_by_tenant(self, tenant_id: str, limit: int = 100) -> list[TaskRecord]:
        async with self.sessions() as session:
            result = await session.execute(
                select(TaskRow)
                .where(TaskRow.tenant_id == tenant_id)
                .limit(limit)
            )
            return [TaskRecord.model_validate(row.payload) for row in result.scalars()]

    async def close(self) -> None:
        await self.engine.dispose()
