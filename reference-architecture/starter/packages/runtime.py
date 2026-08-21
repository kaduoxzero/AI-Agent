from __future__ import annotations

from packages.checkpoints import CheckpointStore
from packages.contracts import (
    ApprovalStatus,
    Artifact,
    RuntimeCheckpoint,
    TaskRecord,
    TaskStatus,
)
from packages.events import EventStore
from packages.model_gateway import ModelGateway
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
        model_gateway: ModelGateway,
        retriever: ReferenceRetriever,
        tools: ToolGateway,
        policy: PolicyEngine,
    ) -> None:
        self.repository = repository
        self.events = events
        self.checkpoints = checkpoints
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
            return await self._save(
                task,
                "ApprovalRequested",
                reason=task.approval_reason,
            )

        checkpoint = await self.checkpoints.get(task.task_id)

        try:
            task = task.transition(TaskStatus.RUNNING)
            if checkpoint is None:
                task = await self._save(task, "RunStarted", trace_id=task.trace_id)
                task = task.patch(
                    step_count=task.step_count + 1,
                    model_calls=task.model_calls + 1,
                )
                self._check_budget(task)
                plan = await self.model_gateway.plan(task)
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

            if "retrieve_internal_knowledge" in checkpoint.plan and "retrieve_internal_knowledge" not in completed:
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

            if "search_public_sources" in checkpoint.plan and "search_public_sources" not in completed:
                task = task.patch(
                    step_count=task.step_count + 1,
                    tool_calls=task.tool_calls + 1,
                )
                self._check_budget(task)
                evidence.extend(await self.tools.call(task, "search_public_sources", {}, scopes))
                task = await self._save(task, "ToolCompleted", tool="search_public_sources")
                checkpoint = await self._checkpoint_action(
                    checkpoint, "search_public_sources", evidence
                )

            cancelled = await self._cancel_if_requested(task)
            if cancelled is not None:
                return cancelled

            if "load_structured_metrics" in checkpoint.plan and "load_structured_metrics" not in completed:
                task = task.patch(
                    step_count=task.step_count + 1,
                    tool_calls=task.tool_calls + 1,
                )
                self._check_budget(task)
                evidence.extend(
                    await self.tools.call(
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

            task = task.patch(
                step_count=task.step_count + 1,
                model_calls=task.model_calls + 1,
            )
            self._check_budget(task)
            content = await self.model_gateway.synthesize(task, evidence)
            artifact = Artifact(
                artifact_type="analysis_report",
                content=content,
                evidence=evidence,
            )
            task = task.transition(TaskStatus.COMPLETED, result=artifact)
            await self.checkpoints.delete(task.task_id)
            return await self._save(
                task,
                "RunCompleted",
                artifact_id=artifact.artifact_id,
                evidence_count=len(evidence),
            )
        except BudgetExceeded as exc:
            task = task.transition(TaskStatus.FAILED, error=str(exc))
            return await self._save(task, "RunFailed", error=str(exc), category="budget")
        except Exception as exc:
            task = task.transition(TaskStatus.FAILED, error=f"{type(exc).__name__}: {exc}")
            return await self._save(task, "RunFailed", error=task.error, category="runtime")
