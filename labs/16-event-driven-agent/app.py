from __future__ import annotations

from collections import deque
from dataclasses import dataclass, replace
from typing import Deque
from uuid import uuid4


@dataclass(frozen=True)
class Event:
    event_id: str
    trace_id: str
    event_type: str
    payload: dict[str, object]


@dataclass(frozen=True)
class Task:
    event: Event
    attempt: int = 1


class EventGateway:
    def __init__(self, queue: Deque[Task]) -> None:
        self.queue = queue
        self.seen_event_ids: set[str] = set()

    def ingest(self, event: Event) -> bool:
        if event.event_id in self.seen_event_ids:
            print("DEDUP:", event.event_id)
            return False
        self.seen_event_ids.add(event.event_id)
        self.queue.append(Task(event=event))
        return True


class Worker:
    def __init__(self, queue: Deque[Task], dlq: Deque[Task], max_attempts: int = 3) -> None:
        self.queue = queue
        self.dlq = dlq
        self.max_attempts = max_attempts
        self.processed_effects: set[str] = set()
        self.fail_event_ids: set[str] = set()

    def run_until_empty(self) -> None:
        while self.queue:
            task = self.queue.popleft()
            self._process(task)

    def _process(self, task: Task) -> None:
        event = task.event
        try:
            self._handle_idempotently(event)
            print(f"DONE event={event.event_id} attempt={task.attempt}")
        except RuntimeError as exc:
            print(f"FAIL event={event.event_id} attempt={task.attempt}: {exc}")
            if task.attempt >= self.max_attempts:
                self.dlq.append(task)
                print("DLQ:", event.event_id)
            else:
                self.queue.append(replace(task, attempt=task.attempt + 1))

    def _handle_idempotently(self, event: Event) -> None:
        # 事件可能被 MQ 重复投递，业务副作用必须自己幂等。
        effect_key = f"{event.event_type}:{event.event_id}"
        if effect_key in self.processed_effects:
            print("IDEMPOTENT SKIP:", effect_key)
            return

        if event.event_id in self.fail_event_ids:
            raise RuntimeError("simulated downstream failure")

        # 在真正执行副作用成功后再记录完成。
        self.processed_effects.add(effect_key)

    def replay_dlq(self) -> None:
        while self.dlq:
            task = self.dlq.popleft()
            self.queue.append(Task(event=task.event, attempt=1))


def make_event(event_id: str, event_type: str) -> Event:
    return Event(
        event_id=event_id,
        trace_id=str(uuid4()),
        event_type=event_type,
        payload={"supplier_id": "s-001"},
    )


def main() -> None:
    queue: Deque[Task] = deque()
    dlq: Deque[Task] = deque()
    gateway = EventGateway(queue)
    worker = Worker(queue, dlq, max_attempts=3)

    normal = make_event("evt-001", "supplier.alert")
    broken = make_event("evt-002", "supplier.alert")
    worker.fail_event_ids.add("evt-002")

    print("=== ingest normal + duplicate + broken ===")
    gateway.ingest(normal)
    gateway.ingest(normal)  # duplicate delivery
    gateway.ingest(broken)
    worker.run_until_empty()

    print("\nDLQ size:", len(dlq))

    print("\n=== repair downstream and replay DLQ ===")
    worker.fail_event_ids.remove("evt-002")
    worker.replay_dlq()
    worker.run_until_empty()
    print("DLQ size after replay:", len(dlq))


if __name__ == "__main__":
    main()
