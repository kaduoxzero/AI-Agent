from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query, status

from packages.contracts import (
    ApprovalCommand,
    ApprovalStatus,
    TaskCreate,
    TaskEvent,
    TaskRecord,
    TaskStatus,
)
from packages.dependencies import container


TERMINAL = {TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED}


@asynccontextmanager
async def lifespan(_: FastAPI):
    await container.initialize()
    try:
        yield
    finally:
        await container.close()


app = FastAPI(
    title="Reference Agent Platform",
    version="0.2.0",
    lifespan=lifespan,
)


@app.get("/health")
async def health() -> dict[str, object]:
    return {
        "status": "ok",
        "durable_mode": container.settings.durable_mode,
        "database": "postgres" if container.settings.database_url else "memory",
        "queue": "redis" if container.settings.redis_url else "memory",
    }


@app.post("/tasks", response_model=TaskRecord, status_code=status.HTTP_202_ACCEPTED)
async def create_task(command: TaskCreate) -> TaskRecord:
    task = await container.repository.create(command)
    await container.events.publish(task.task_id, "TaskCreated", trace_id=task.trace_id)
    await container.queue.enqueue(task.task_id)
    return task


@app.get("/tasks/{task_id}", response_model=TaskRecord)
async def get_task(task_id: str) -> TaskRecord:
    task = await container.repository.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="task not found")
    return task


@app.get("/tasks/{task_id}/events", response_model=list[TaskEvent])
async def get_events(task_id: str, start: int = Query(default=0, ge=0)) -> list[TaskEvent]:
    if await container.repository.get(task_id) is None:
        raise HTTPException(status_code=404, detail="task not found")
    return await container.events.list(task_id, start=start)


@app.post("/tasks/{task_id}/cancel", response_model=TaskRecord)
async def cancel_task(task_id: str) -> TaskRecord:
    task = await container.repository.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="task not found")
    if task.status in TERMINAL:
        raise HTTPException(status_code=409, detail=f"terminal task: {task.status.value}")

    task = task.transition(TaskStatus.CANCELLING, cancel_requested=True)
    await container.repository.save(task)
    await container.events.publish(task_id, "CancellationRequested")
    return task


@app.post("/tasks/{task_id}/approval", response_model=TaskRecord)
async def decide_approval(task_id: str, command: ApprovalCommand) -> TaskRecord:
    task = await container.repository.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="task not found")
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
            task_id, "ApprovalResolved", decision="approved", actor_id=command.actor_id
        )
        await container.queue.enqueue(task_id)
        return task

    task = task.transition(
        TaskStatus.CANCELLED,
        approval_status=ApprovalStatus.REJECTED,
        approval_reason=command.reason,
    )
    await container.repository.save(task)
    await container.events.publish(
        task_id, "ApprovalResolved", decision="rejected", actor_id=command.actor_id
    )
    return task
