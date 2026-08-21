from __future__ import annotations

from dataclasses import dataclass

from packages.artifacts import ArtifactStore, FileArtifactStore, InMemoryArtifactStore
from packages.checkpoints import (
    CheckpointStore,
    InMemoryCheckpointStore,
    RedisCheckpointStore,
)
from packages.config import Settings
from packages.events import EventStore, InMemoryEventStore, RedisEventStore
from packages.model_gateway import DeterministicProvider, ModelGateway
from packages.policy import PolicyEngine
from packages.queueing import InMemoryTaskQueue, RedisTaskQueue, TaskQueue
from packages.rag import ReferenceRetriever
from packages.repositories import InMemoryTaskRepository, PostgresTaskRepository, TaskRepository
from packages.runtime import AgentRuntime
from packages.tools import ToolGateway


@dataclass
class Container:
    settings: Settings
    repository: TaskRepository
    queue: TaskQueue
    events: EventStore
    checkpoints: CheckpointStore
    artifacts: ArtifactStore
    runtime: AgentRuntime

    async def initialize(self) -> None:
        await self.repository.initialize()
        await self.queue.initialize()

    async def close(self) -> None:
        await self.repository.close()
        await self.queue.close()
        await self.events.close()
        await self.checkpoints.close()
        await self.artifacts.close()


def build_container(settings: Settings | None = None) -> Container:
    settings = settings or Settings.from_env()

    if settings.database_url:
        repository: TaskRepository = PostgresTaskRepository(settings.database_url)
    else:
        repository = InMemoryTaskRepository()

    if settings.redis_url:
        queue: TaskQueue = RedisTaskQueue(settings.redis_url, settings.task_queue_name)
        events: EventStore = RedisEventStore(settings.redis_url, settings.event_key_prefix)
        checkpoints: CheckpointStore = RedisCheckpointStore(settings.redis_url)
    else:
        queue = InMemoryTaskQueue()
        events = InMemoryEventStore()
        checkpoints = InMemoryCheckpointStore()

    artifacts: ArtifactStore
    if settings.artifact_dir:
        artifacts = FileArtifactStore(settings.artifact_dir)
    else:
        artifacts = InMemoryArtifactStore()

    runtime = AgentRuntime(
        repository=repository,
        events=events,
        checkpoints=checkpoints,
        artifacts=artifacts,
        model_gateway=ModelGateway(DeterministicProvider()),
        retriever=ReferenceRetriever(),
        tools=ToolGateway(),
        policy=PolicyEngine(),
    )
    return Container(settings, repository, queue, events, checkpoints, artifacts, runtime)


container = build_container()
