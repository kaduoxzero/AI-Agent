from __future__ import annotations

from packages.artifacts import ArtifactStore
from packages.checkpoints import CheckpointStore
from packages.contracts import (
    ApprovalStatus,
    Artifact,
    RuntimeCheckpoint,
    TaskRecord,
    TaskStatus,
)
from packages.events import EventStore
from packages.model_gateway import ModelGateway, ModelUsage
from packages.policy import PolicyEngine
from packages.rag import ReferenceRetriever
from packages.repositories import TaskRepository
from packages.tools import ToolGateway


class BudgetExceeded(RuntimeError):
    pass


class AgentRuntime:
    def __init__(
        self,
        repository: TaskRepository,
        events: EventStore,
        checkpoints: CheckpointStore,
        artifacts: ArtifactStore,
        model_gateway: ModelGateway,
        retriever: ReferenceRetriever,
        tools: ToolGateway,
        policy: PolicyEngine,
    ) -> None:
        self.repository = repository
        self.events = events
        self.checkpoints = checkpoints
        self.artifacts = artifacts
        self.model_gateway = model_gateway
        self.retriever = retriever
        self.tools = tools
        self.policy = policy

    async def _save(self, task: TaskRecord, event_type: str, **data) -> TaskRecord:
        task = await self.repository.save(task)
        await self.events.publish(task.task_id, event_type, **data)
        return task

    def _check_budget(self, task: TaskRecord) -> None:
        if task.step_count > task.budget.max_steps:
            raise BudgetExceeded("max_steps exceeded")
        if task.model_calls > task.budget.max_model_calls:
            raise BudgetExceeded("max_model_calls exceeded")
        if task.tool_calls > task.budget.max_tool_calls:
            raise BudgetExceeded("max_tool_calls exceeded")
        if task.estimated_cost_usd > task.budget.max_cost_usd:
            raise BudgetExceeded("max_cost_usd exceeded")

    def _reserve_model_call(self, task: TaskRecord) -> None:
        if task.model_calls + 1 > task.budget.max_model_calls:
            raise BudgetExceeded("max_model_calls exceeded")

    async def _record_model_usage(
        self,
        task: TaskRecord,
        operation: str,
        usage: ModelUsage,
    ) -> TaskRecord:
        task = task.patch(
            model_calls=task.model_calls + 1,
            input_tokens=task.input_tokens + usage.input_tokens,
            output_tokens=task.output_tokens + usage.output_tokens,
            estimated_cost_usd=round(
                task.estimated_cost_usd + usage.estimated_cost_usd,
                8,
            ),
        )
        self._check_budget(task)
        return await self._save(
            task,
            "ModelCompleted",
            operation=operation,
            provider=usage.provider,
            model_route=usage.model_route,
            input_tokens=usage.input_tokens,
            output_tokens=usage.output_tokens,
            estimated_cost_usd=usage.estimated_cost_usd,
        )

    async def _cancel_if_requested(self, task: TaskRecord) -> TaskRecord | None:
        latest = await self.repository.get(task.task_id)
        if latest is None:
            raise RuntimeError("task disappeared during execution")
        if latest.cancel_requested or latest.status == TaskStatus.CANCELLING:
            latest = latest.transition(TaskStatus.CANCELLED)
            await self.checkpoints.delete(task.task_id)
            return await self._save(latest, "RunCancelled")
        return None

    async def _checkpoint_action(
        self,
        checkpoint: RuntimeCheckpoint,
        action: str,
        evidence,
    ) -> RuntimeCheckpoint:
        checkpoint = checkpoint.mark_action(action, evidence)
        await self.checkpoints.save(checkpoint)
        await self.events.publish(
            checkpoint.task_id,
            "CheckpointSaved",
            completed_actions=checkpoint.completed_actions,
        )
        return checkpoint

    async def _call_tool(
        self,
        task: TaskRecord,
        name: str,
        args: dict,
        scopes: set[str],
    ):
        if name not in set(task.allowed_tools):
            raise PermissionError(
                f"tool {name} is not allowed for {task.agent_id}@{task.agent_version}"
            )
        return await self.tools.call(task, name, args, scopes)

    async def run(self, task_id: str) -> TaskRecord | None:
        task = await self.repository.get(task_id)
        if task is None:
            return None
        if task.status in {TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED}:
            return task

        cancelled = await self._cancel_if_requested(task)
        if cancelled is not None:
            return cancelled

        if self.policy.requires_approval(task) and task.approval_status != ApprovalStatus.APPROVED:
            task = task.transition(
                TaskStatus.WAITING_APPROVAL,
                approval_status=ApprovalStatus.PENDING,
                approval_reason="high-impact request requires human approval",
            )
            return await self._save(task, "ApprovalRequested", reason=task.approval_reason)

        checkpoint = await self.checkpoints.get(task.task_id)

        try:
            task = task.transition(TaskStatus.RUNNING)
            if checkpoint is None:
                task = await self._save(
                    task,
                    "RunStarted",
                    trace_id=task.trace_id,
                    agent_id=task.agent_id,
                    agent_version=task.agent_version,
                    prompt_version=task.prompt_version,
                    model_route=task.model_route,
                )
                task = task.patch(step_count=task.step_count + 1)
                self._check_budget(task)
                self._reserve_model_call(task)
                plan_result = await self.model_gateway.plan(task)
                task = await self._record_model_usage(task, "plan", plan_result.usage)
                plan = plan_result.value
                task = await self._save(task, "PlanCreated", plan=plan)
                checkpoint = RuntimeCheckpoint(task_id=task.task_id, plan=plan)
                await self.checkpoints.save(checkpoint)
                await self.events.publish(task.task_id, "CheckpointSaved", completed_actions=[])
            else:
                task = await self._save(
                    task,
                    "RunResumed",
                    completed_actions=checkpoint.completed_actions,
                )

            evidence = list(checkpoint.evidence)
            completed = set(checkpoint.completed_actions)
            scopes = self.policy.scopes_for(task)

            if (
                "retrieve_internal_knowledge" in checkpoint.plan
                and "retrieve_internal_knowledge" not in completed
            ):
                task = task.patch(step_count=task.step_count + 1)
                self._check_budget(task)
                evidence.extend(await self.retriever.search(task.tenant_id, task.query))
                task = await self._save(task, "RetrievalCompleted", count=len(evidence))
                checkpoint = await self._checkpoint_action(
                    checkpoint, "retrieve_internal_knowledge", evidence
                )

            cancelled = await self._cancel_if_requested(task)
            if cancelled is not None:
                return cancelled

            if (
                "search_public_sources" in checkpoint.plan
                and "search_public_sources" not in completed
            ):
                task = task.patch(
                    step_count=task.step_count + 1,
                    tool_calls=task.tool_calls + 1,
                )
                self._check_budget(task)
                evidence.extend(await self._call_tool(task, "search_public_sources", {}, scopes))
                task = await self._save(task, "ToolCompleted", tool="search_public_sources")
                checkpoint = await self._checkpoint_action(
                    checkpoint, "search_public_sources", evidence
                )

            cancelled = await self._cancel_if_requested(task)
            if cancelled is not None:
                return cancelled

            if (
                "load_structured_metrics" in checkpoint.plan
                and "load_structured_metrics" not in completed
            ):
                task = task.patch(
                    step_count=task.step_count + 1,
                    tool_calls=task.tool_calls + 1,
                )
                self._check_budget(task)
                evidence.extend(
                    await self._call_tool(
                        task,
                        "get_supplier_metrics",
                        {"supplier": "supplier-a"},
                        scopes,
                    )
                )
                task = await self._save(task, "ToolCompleted", tool="get_supplier_metrics")
                checkpoint = await self._checkpoint_action(
                    checkpoint, "load_structured_metrics", evidence
                )

            task = task.patch(step_count=task.step_count + 1)
            self._check_budget(task)
            self._reserve_model_call(task)
            synthesis_result = await self.model_gateway.synthesize(task, evidence)
            task = await self._record_model_usage(task, "synthesize", synthesis_result.usage)
            artifact = Artifact(
                artifact_type="analysis_report",
                content={
                    **synthesis_result.value,
                    "agent_id": task.agent_id,
                    "agent_version": task.agent_version,
                    "prompt_version": task.prompt_version,
                    "model_route": task.model_route,
                    "usage": {
                        "input_tokens": task.input_tokens,
                        "output_tokens": task.output_tokens,
                        "estimated_cost_usd": task.estimated_cost_usd,
                    },
                },
                evidence=evidence,
            )
            artifact_uri = await self.artifacts.put(task.task_id, artifact)
            task = task.transition(
                TaskStatus.COMPLETED,
                artifact_uri=artifact_uri,
                result=artifact,
            )
            await self.checkpoints.delete(task.task_id)
            return await self._save(
                task,
                "RunCompleted",
                artifact_id=artifact.artifact_id,
                artifact_uri=artifact_uri,
                evidence_count=len(evidence),
                estimated_cost_usd=task.estimated_cost_usd,
            )
        except BudgetExceeded as exc:
            task = task.transition(TaskStatus.FAILED, error=str(exc))
            return await self._save(task, "RunFailed", error=str(exc), category="budget")
        except Exception as exc:
            task = task.transition(TaskStatus.FAILED, error=f"{type(exc).__name__}: {exc}")
            return await self._save(task, "RunFailed", error=task.error, category="runtime")
