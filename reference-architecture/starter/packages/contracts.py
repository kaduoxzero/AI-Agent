from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    WAITING_APPROVAL = "WAITING_APPROVAL"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLING = "CANCELLING"
    CANCELLED = "CANCELLED"


class TaskCreate(BaseModel):
    tenant_id: str = Field(min_length=1)
    user_id: str = Field(min_length=1)
    query: str = Field(min_length=1, max_length=10_000)


class TaskRecord(BaseModel):
    task_id: str
    tenant_id: str
    user_id: str
    query: str
    status: TaskStatus
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_create(cls, command: TaskCreate) -> "TaskRecord":
        now = datetime.now(timezone.utc)
        return cls(
            task_id=str(uuid4()),
            tenant_id=command.tenant_id,
            user_id=command.user_id,
            query=command.query,
            status=TaskStatus.PENDING,
            created_at=now,
            updated_at=now,
        )

    def transition(self, status: TaskStatus) -> "TaskRecord":
        return self.model_copy(
            update={
                "status": status,
                "updated_at": datetime.now(timezone.utc),
            }
        )
