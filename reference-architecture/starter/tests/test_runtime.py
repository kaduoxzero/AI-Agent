import asyncio

from packages.artifacts import InMemoryArtifactStore
from packages.checkpoints import InMemoryCheckpointStore
from packages.contracts import (
    ApprovalStatus,
    Evidence,
    RuntimeCheckpoint,
    TaskCreate,
    TaskStatus,
)
from packages.events import InMemoryEventStore
from packages.model_gateway import DeterministicProvider, ModelGateway
from packages.policy import PolicyEngine
from packages.rag import ReferenceRetriever
from packages.repositories import InMemoryTaskRepository
from packages.runtime import AgentRuntime
from packages.tools import ToolGateway


def build_runtime():
    repo = InMemoryTaskRepository()
    events = InMemoryEventStore()
    checkpoints = InMemoryCheckpointStore()
    artifacts = InMemoryArtifactStore()
    runtime = AgentRuntime(
        repository=repo,
        events=events,
        checkpoints=checkpoints,
        artifacts=artifacts,
        model_gateway=ModelGateway(DeterministicProvider()),
        retriever=ReferenceRetriever(),
        tools=ToolGateway(),
        policy=PolicyEngine(),
    )
    return repo, events, checkpoints, artifacts, runtime


async def create_task(repo: InMemoryTaskRepository, **kwargs):
    task, created = await repo.create(TaskCreate(**kwargs))
    assert created is True
    return task


def test_runtime_completes_with_typed_artifact() -> None:
    async def scenario():
        repo, events, _, artifacts, runtime = build_runtime()
        task = await create_task(
            repo,
            tenant_id="tenant-a",
            user_id="u1",
            query="分析供应商风险和公开新闻",
        )
        result = await runtime.run(task.task_id)
        assert result is not None
        assert result.status == TaskStatus.COMPLETED
        assert result.result is not None
        assert result.artifact_uri is not None
        assert await artifacts.get(result.artifact_uri) == result.result
        assert result.result.artifact_type == "analysis_report"
        assert result.result.evidence
        assert all("tenant-b" not in e.source_id for e in result.result.evidence)
        event_types = [event.event_type for event in await events.list(task.task_id)]
        assert "PlanCreated" in event_types
        assert "CheckpointSaved" in event_types
        assert "RunCompleted" in event_types

    asyncio.run(scenario())


def test_high_impact_task_stops_for_approval() -> None:
    async def scenario():
        repo, events, _, _, runtime = build_runtime()
        task = await create_task(
            repo,
            tenant_id="tenant-a",
            user_id="u1",
            query="暂停采购并分析供应商风险",
        )
        result = await runtime.run(task.task_id)
        assert result is not None
        assert result.status == TaskStatus.WAITING_APPROVAL
        assert result.approval_status == ApprovalStatus.PENDING
        assert [e.event_type for e in await events.list(task.task_id)] == ["ApprovalRequested"]

    asyncio.run(scenario())


def test_budget_failure_is_fail_closed() -> None:
    async def scenario():
        repo, _, _, _, runtime = build_runtime()
        task = await create_task(
            repo,
            tenant_id="tenant-a",
            user_id="u1",
            query="分析供应商风险",
            budget={
                "max_steps": 1,
                "max_model_calls": 8,
                "max_tool_calls": 12,
                "max_cost_usd": 1.0,
            },
        )
        result = await runtime.run(task.task_id)
        assert result is not None
        assert result.status == TaskStatus.FAILED
        assert "max_steps" in (result.error or "")

    asyncio.run(scenario())


def test_runtime_resumes_from_checkpoint_without_repeating_completed_action() -> None:
    async def scenario():
        repo, events, checkpoints, _, runtime = build_runtime()
        task = await create_task(
            repo,
            tenant_id="tenant-a",
            user_id="u1",
            query="分析供应商风险",
        )
        checkpoint_evidence = Evidence(
            source_type="knowledge_base",
            source_id="checkpoint:doc-a-1",
            content="已在崩溃前完成的内部检索结果",
            confidence=0.9,
        )
        checkpoint = RuntimeCheckpoint(
            task_id=task.task_id,
            plan=[
                "retrieve_internal_knowledge",
                "load_structured_metrics",
                "review_and_synthesize",
            ],
            completed_actions=["retrieve_internal_knowledge"],
            evidence=[checkpoint_evidence],
        )
        await checkpoints.save(checkpoint)
        await repo.save(task.transition(TaskStatus.RUNNING, step_count=2, model_calls=1))

        result = await runtime.run(task.task_id)
        assert result is not None
        assert result.status == TaskStatus.COMPLETED
        assert result.result is not None
        source_ids = [e.source_id for e in result.result.evidence]
        assert source_ids.count("checkpoint:doc-a-1") == 1
        assert "doc-a-1" not in source_ids
        event_types = [event.event_type for event in await events.list(task.task_id)]
        assert "RunResumed" in event_types
        assert "PlanCreated" not in event_types

    asyncio.run(scenario())


def test_idempotency_key_returns_same_task() -> None:
    async def scenario():
        repo, _, _, _, _ = build_runtime()
        command = TaskCreate(
            tenant_id="tenant-a",
            user_id="u1",
            query="分析供应商风险",
            idempotency_key="request-123",
        )
        first, first_created = await repo.create(command)
        second, second_created = await repo.create(command)
        assert first_created is True
        assert second_created is False
        assert first.task_id == second.task_id

    asyncio.run(scenario())
