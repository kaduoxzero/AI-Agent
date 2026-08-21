from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from typing import Annotated, AsyncIterator

from fastapi import Depends, FastAPI, Header, HTTPException, Query, status
from fastapi.responses import StreamingResponse

from packages.contracts import (
    ApprovalCommand,
    ApprovalStatus,
    Artifact,
    TaskCreate,
    TaskEvent,
    TaskRecord,
    TaskRequest,
    TaskStatus,
)
from packages.dependencies import container


TERMINAL = {TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED}


class RequestIdentity:
    def __init__(self, tenant_id: str, user_id: str) -> None:
        self.tenant_id = tenant_id
        self.user_id = user_id


async def request_identity(
    x_tenant_id: Annotated[str | None, Header(alias="X-Tenant-ID")] = None,
    x_user_id: Annotated[str | None, Header(alias="X-User-ID")] = None,
) -> RequestIdentity:
    # These headers model a trusted API-gateway boundary. In production they must
    # be written by authenticated middleware/gateway, never trusted from the open Internet.
    if not x_tenant_id or not x_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="trusted identity headers are required",
        )
    return RequestIdentity(x_tenant_id, x_user_id)


Identity = Annotated[RequestIdentity, Depends(request_identity)]


@asynccontextmanager
async def lifespan(_: FastAPI):
    await container.initialize()
    try:
        yield
    finally:
        await container.close()


app = FastAPI(
    title="Reference Agent Platform",
    version="0.3.0",
    lifespan=lifespan,
)


async def owned_task(task_id: str, identity: RequestIdentity) -> TaskRecord:
    task = await container.repository.get(task_id)
    if task is None or task.tenant_id != identity.tenant_id:
        # Return 404 for cross-tenant IDs to avoid leaking object existence.
        raise HTTPException(status_code=404, detail="task not found")
    return task


@app.get("/health")
async def health() -> dict[str, object]:
    return {
        "status": "ok",
        "durable_mode": container.settings.durable_mode,
        "database": "postgres" if container.settings.database_url else "memory",
        "queue": "redis-streams" if container.settings.redis_url else "memory",
        "artifact_store": "file" if container.settings.artifact_dir else "memory",
    }


@app.post("/tasks", response_model=TaskRecord, status_code=status.HTTP_202_ACCEPTED)
async def create_task(
    request: TaskRequest,
    identity: Identity,
    idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
) -> TaskRecord:
    command = TaskCreate(
        tenant_id=identity.tenant_id,
        user_id=identity.user_id,
        query=request.query,
        metadata=request.metadata,
        budget=request.budget,
        idempotency_key=idempotency_key,
    )
    task, created = await container.repository.create(command)
    if created:
        await container.events.publish(task.task_id, "TaskCreated", trace_id=task.trace_id)
        await container.queue.enqueue(task.task_id)
    return task


@app.get("/tasks", response_model=list[TaskRecord])
async def list_tasks(
    identity: Identity,
    limit: int = Query(default=50, ge=1, le=100),
) -> list[TaskRecord]:
    return await container.repository.list_by_tenant(identity.tenant_id, limit=limit)


@app.get("/tasks/{task_id}", response_model=TaskRecord)
async def get_task(task_id: str, identity: Identity) -> TaskRecord:
    return await owned_task(task_id, identity)


@app.get("/tasks/{task_id}/events", response_model=list[TaskEvent])
async def get_events(
    task_id: str,
    identity: Identity,
    start: int = Query(default=0, ge=0),
) -> list[TaskEvent]:
    await owned_task(task_id, identity)
    return await container.events.list(task_id, start=start)


@app.get("/tasks/{task_id}/events/stream")
async def stream_events(
    task_id: str,
    identity: Identity,
    start: int = Query(default=0, ge=0),
) -> StreamingResponse:
    await owned_task(task_id, identity)

    async def generate() -> AsyncIterator[str]:
        cursor = start
        idle_after_terminal = 0
        while True:
            events = await container.events.list(task_id, start=cursor)
            for event in events:
                cursor += 1
                yield (
                    f"id: {cursor - 1}\n"
                    f"event: {event.event_type}\n"
                    f"data: {event.model_dump_json()}\n\n"
                )

            task = await container.repository.get(task_id)
            if task is None or task.status in TERMINAL:
                if events:
                    idle_after_terminal = 0
                else:
                    idle_after_terminal += 1
                if idle_after_terminal >= 2:
                    break
            yield ": keepalive\n\n"
            await asyncio.sleep(0.5)

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@app.get("/tasks/{task_id}/artifact", response_model=Artifact)
async def get_artifact(task_id: str, identity: Identity) -> Artifact:
    task = await owned_task(task_id, identity)
    if not task.artifact_uri:
        raise HTTPException(status_code=404, detail="artifact not available")
    artifact = await container.artifacts.get(task.artifact_uri)
    if artifact is None:
        raise HTTPException(status_code=404, detail="artifact not found")
    return artifact


@app.post("/tasks/{task_id}/cancel", response_model=TaskRecord)
async def cancel_task(task_id: str, identity: Identity) -> TaskRecord:
    task = await owned_task(task_id, identity)
    if task.status in TERMINAL:
        raise HTTPException(status_code=409, detail=f"terminal task: {task.status.value}")

    task = task.transition(TaskStatus.CANCELLING, cancel_requested=True)
    await container.repository.save(task)
    await container.events.publish(
        task_id,
        "CancellationRequested",
        actor_id=identity.user_id,
    )
    return task


@app.post("/tasks/{task_id}/approval", response_model=TaskRecord)
async def decide_approval(
    task_id: str,
    command: ApprovalCommand,
    identity: Identity,
) -> TaskRecord:
    task = await owned_task(task_id, identity)
    if command.actor_id != identity.user_id:
        raise HTTPException(status_code=403, detail="approval actor does not match identity")
    if task.status != TaskStatus.WAITING_APPROVAL:
        raise HTTPException(status_code=409, detail="task is not waiting for approval")

    if command.approve:
        task = task.transition(
            TaskStatus.PENDING,
            approval_status=ApprovalStatus.APPROVED,
            approval_reason=command.reason,
        )
        await container.repository.save(task)
        await container.events.publish(
            task_id,
            "ApprovalResolved",
            decision="approved",
            actor_id=identity.user_id,
        )
        await container.queue.enqueue(task_id)
        return task

    task = task.transition(
        TaskStatus.CANCELLED,
        approval_status=ApprovalStatus.REJECTED,
        approval_reason=command.reason,
    )
    await container.checkpoints.delete(task_id)
    await container.repository.save(task)
    await container.events.publish(
        task_id,
        "ApprovalResolved",
        decision="rejected",
        actor_id=identity.user_id,
    )
    return task
