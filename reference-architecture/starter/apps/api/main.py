from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from typing import Annotated, AsyncIterator

from fastapi import Depends, FastAPI, Header, HTTPException, Query, status
from fastapi.responses import StreamingResponse

from packages.contracts import (
    AgentDefinition,
    ApprovalCommand,
    ApprovalStatus,
    Artifact,
    EvalResult,
    ReleaseRoute,
    TaskCreate,
    TaskEvent,
    TaskRecord,
    TaskRequest,
    TaskStatus,
)
from packages.dependencies import container
from packages.registry import ReleaseRejected


TERMINAL = {TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED}


class RequestIdentity:
    def __init__(self, tenant_id: str, user_id: str) -> None:
        self.tenant_id = tenant_id
        self.user_id = user_id


async def request_identity(
    x_tenant_id: Annotated[str | None, Header(alias="X-Tenant-ID")] = None,
    x_user_id: Annotated[str | None, Header(alias="X-User-ID")] = None,
) -> RequestIdentity:
    if not x_tenant_id or not x_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="trusted identity headers are required",
        )
    return RequestIdentity(x_tenant_id, x_user_id)


async def platform_admin(
    x_platform_admin: Annotated[str | None, Header(alias="X-Platform-Admin")] = None,
) -> None:
    if x_platform_admin != "true":
        raise HTTPException(status_code=403, detail="platform admin permission required")


Identity = Annotated[RequestIdentity, Depends(request_identity)]
Admin = Annotated[None, Depends(platform_admin)]


@asynccontextmanager
async def lifespan(_: FastAPI):
    await container.initialize()
    try:
        yield
    finally:
        await container.close()


app = FastAPI(
    title="Reference Agent Platform",
    version="0.5.0",
    lifespan=lifespan,
)


async def owned_task(task_id: str, identity: RequestIdentity) -> TaskRecord:
    task = await container.repository.get(task_id)
    if task is None or task.tenant_id != identity.tenant_id:
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
    agent_id = request.agent_id or container.settings.default_agent_id
    routing_key = idempotency_key or f"{identity.tenant_id}:{identity.user_id}:{request.query}"
    try:
        definition = container.registry.resolve(agent_id, routing_key)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    # Release manifest is snapshotted into the Task. The worker does not consult a
    # mutable Control Plane during execution, which makes retries reproducible.
    command = TaskCreate(
        tenant_id=identity.tenant_id,
        user_id=identity.user_id,
        query=request.query,
        agent_id=definition.agent_id,
        agent_version=definition.version,
        prompt_version=definition.prompt_version,
        model_route=definition.model_route,
        allowed_tools=definition.allowed_tools,
        metadata=request.metadata,
        budget=request.budget,
        idempotency_key=idempotency_key,
    )
    task, created = await container.repository.create(command)
    if created:
        await container.events.publish(
            task.task_id,
            "TaskCreated",
            trace_id=task.trace_id,
            agent_id=task.agent_id,
            agent_version=task.agent_version,
            prompt_version=task.prompt_version,
            model_route=task.model_route,
        )
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
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
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


# -------------------------- Control Plane --------------------------


@app.get("/control-plane/agents", response_model=list[AgentDefinition])
async def list_agents(_: Admin) -> list[AgentDefinition]:
    return container.registry.list_agents()


@app.post("/control-plane/agents", response_model=AgentDefinition)
async def register_agent(definition: AgentDefinition, _: Admin) -> AgentDefinition:
    return container.registry.register(definition)


@app.post("/control-plane/evals", response_model=EvalResult)
async def record_eval(result: EvalResult, _: Admin) -> EvalResult:
    return container.registry.record_eval(result)


@app.put("/control-plane/releases/{agent_id}", response_model=ReleaseRoute)
async def update_release(agent_id: str, route: ReleaseRoute, _: Admin) -> ReleaseRoute:
    if route.agent_id != agent_id:
        raise HTTPException(status_code=400, detail="route agent_id does not match path")
    try:
        return container.registry.release(route)
    except (ReleaseRejected, KeyError) as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@app.get("/control-plane/releases/{agent_id}", response_model=ReleaseRoute)
async def get_release(agent_id: str, _: Admin) -> ReleaseRoute:
    route = container.registry.routes.get(agent_id)
    if route is None:
        raise HTTPException(status_code=404, detail="release route not found")
    return route
