import asyncio

from packages.contracts import ApprovalStatus, TaskCreate, TaskStatus
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
    runtime = AgentRuntime(
        repository=repo,
        events=events,
        model_gateway=ModelGateway(DeterministicProvider()),
        retriever=ReferenceRetriever(),
        tools=ToolGateway(),
        policy=PolicyEngine(),
    )
    return repo, events, runtime


def test_runtime_completes_with_typed_artifact() -> None:
    async def scenario():
        repo, events, runtime = build_runtime()
        task = await repo.create(
            TaskCreate(
                tenant_id="tenant-a",
                user_id="u1",
                query="分析供应商风险和公开新闻",
            )
        )
        result = await runtime.run(task.task_id)
        assert result is not None
        assert result.status == TaskStatus.COMPLETED
        assert result.result is not None
        assert result.result.artifact_type == "analysis_report"
        assert result.result.evidence
        assert all("tenant-b" not in e.source_id for e in result.result.evidence)
        event_types = [event.event_type for event in await events.list(task.task_id)]
        assert "PlanCreated" in event_types
        assert "RunCompleted" in event_types

    asyncio.run(scenario())


def test_high_impact_task_stops_for_approval() -> None:
    async def scenario():
        repo, events, runtime = build_runtime()
        task = await repo.create(
            TaskCreate(
                tenant_id="tenant-a",
                user_id="u1",
                query="暂停采购并分析供应商风险",
            )
        )
        result = await runtime.run(task.task_id)
        assert result is not None
        assert result.status == TaskStatus.WAITING_APPROVAL
        assert result.approval_status == ApprovalStatus.PENDING
        assert [e.event_type for e in await events.list(task.task_id)] == ["ApprovalRequested"]

    asyncio.run(scenario())


def test_budget_failure_is_fail_closed() -> None:
    async def scenario():
        repo, events, runtime = build_runtime()
        task = await repo.create(
            TaskCreate(
                tenant_id="tenant-a",
                user_id="u1",
                query="分析供应商风险",
                budget={"max_steps": 1, "max_model_calls": 8, "max_tool_calls": 12, "max_cost_usd": 1.0},
            )
        )
        result = await runtime.run(task.task_id)
        assert result is not None
        assert result.status == TaskStatus.FAILED
        assert "max_steps" in (result.error or "")

    asyncio.run(scenario())
