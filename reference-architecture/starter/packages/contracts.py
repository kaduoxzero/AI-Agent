from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    WAITING_APPROVAL = "WAITING_APPROVAL"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLING = "CANCELLING"
    CANCELLED = "CANCELLED"


class ApprovalStatus(str, Enum):
    NOT_REQUIRED = "NOT_REQUIRED"
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class TaskBudget(StrictModel):
    max_steps: int = Field(default=12, ge=1, le=100)
    max_model_calls: int = Field(default=8, ge=1, le=100)
    max_tool_calls: int = Field(default=12, ge=0, le=200)
    max_cost_usd: float = Field(default=1.0, gt=0, le=1000)


class TaskCreate(StrictModel):
    tenant_id: str = Field(min_length=1, max_length=128)
    user_id: str = Field(min_length=1, max_length=128)
    query: str = Field(min_length=1, max_length=10_000)
    metadata: dict[str, Any] = Field(default_factory=dict)
    budget: TaskBudget = Field(default_factory=TaskBudget)


class Evidence(StrictModel):
    evidence_id: str = Field(default_factory=lambda: str(uuid4()))
    source_type: str
    source_id: str
    content: str
    confidence: float = Field(ge=0, le=1)


class Artifact(StrictModel):
    artifact_id: str = Field(default_factory=lambda: str(uuid4()))
    artifact_type: str
    content: dict[str, Any]
    evidence: list[Evidence] = Field(default_factory=list)


class TaskEvent(StrictModel):
    event_id: str = Field(default_factory=lambda: str(uuid4()))
    task_id: str
    event_type: str
    data: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=utcnow)


class ApprovalCommand(StrictModel):
    approve: bool
    reason: str = Field(min_length=1, max_length=1000)
    actor_id: str = Field(min_length=1, max_length=128)


class TaskRecord(StrictModel):
    task_id: str
    trace_id: str
    tenant_id: str
    user_id: str
    query: str
    metadata: dict[str, Any]
    budget: TaskBudget
    status: TaskStatus
    step_count: int = 0
    model_calls: int = 0
    tool_calls: int = 0
    cancel_requested: bool = False
    approval_status: ApprovalStatus = ApprovalStatus.NOT_REQUIRED
    approval_reason: str | None = None
    result: Artifact | None = None
    error: str | None = None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_create(cls, command: TaskCreate) -> "TaskRecord":
        now = utcnow()
        return cls(
            task_id=str(uuid4()),
            trace_id=str(uuid4()),
            tenant_id=command.tenant_id,
            user_id=command.user_id,
            query=command.query,
            metadata=command.metadata,
            budget=command.budget,
            status=TaskStatus.PENDING,
            created_at=now,
            updated_at=now,
        )

    def patch(self, **changes: Any) -> "TaskRecord":
        changes["updated_at"] = utcnow()
        return self.model_copy(update=changes)

    def transition(self, status: TaskStatus, **changes: Any) -> "TaskRecord":
        return self.patch(status=status, **changes)
