from __future__ import annotations

from dataclasses import dataclass

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
    runtime: AgentRuntime

    async def initialize(self) -> None:
        await self.repository.initialize()

    async def close(self) -> None:
        await self.repository.close()
        await self.queue.close()
        await self.events.close()


def build_container(settings: Settings | None = None) -> Container:
    settings = settings or Settings.from_env()

    if settings.database_url:
        repository: TaskRepository = PostgresTaskRepository(settings.database_url)
    else:
        repository = InMemoryTaskRepository()

    if settings.redis_url:
        queue: TaskQueue = RedisTaskQueue(settings.redis_url, settings.task_queue_name)
        events: EventStore = RedisEventStore(settings.redis_url, settings.event_key_prefix)
    else:
        queue = InMemoryTaskQueue()
        events = InMemoryEventStore()

    runtime = AgentRuntime(
        repository=repository,
        events=events,
        model_gateway=ModelGateway(DeterministicProvider()),
        retriever=ReferenceRetriever(),
        tools=ToolGateway(),
        policy=PolicyEngine(),
    )
    return Container(settings, repository, queue, events, runtime)


container = build_container()
