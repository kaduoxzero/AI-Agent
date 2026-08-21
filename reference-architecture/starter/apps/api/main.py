from __future__ import annotations

from threading import Lock

from fastapi import FastAPI, HTTPException, status

from packages.contracts import TaskCreate, TaskRecord, TaskStatus


app = FastAPI(
    title="Reference Agent Platform Starter",
    version="0.1.0",
)


class InMemoryTaskRepository:
    """教学实现。

    生产阶段替换成 PostgreSQL Repository，API Handler 不应该感知具体存储。
    """

    def __init__(self) -> None:
        self._items: dict[str, TaskRecord] = {}
        self._lock = Lock()

    def create(self, command: TaskCreate) -> TaskRecord:
        task = TaskRecord.from_create(command)
        with self._lock:
            self._items[task.task_id] = task
        return task

    def get(self, task_id: str) -> TaskRecord | None:
        with self._lock:
            return self._items.get(task_id)

    def save(self, task: TaskRecord) -> TaskRecord:
        with self._lock:
            self._items[task.task_id] = task
        return task


repo = InMemoryTaskRepository()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/tasks", response_model=TaskRecord, status_code=status.HTTP_202_ACCEPTED)
def create_task(command: TaskCreate) -> TaskRecord:
    """创建长任务，但不在 HTTP Handler 内运行 Agent。"""
    task = repo.create(command)

    # 下一阶段：在这里发布 TaskCreated 到 Queue，而不是同步执行 Agent。
    return task


@app.get("/tasks/{task_id}", response_model=TaskRecord)
def get_task(task_id: str) -> TaskRecord:
    task = repo.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="task not found")
    return task


@app.post("/tasks/{task_id}/cancel", response_model=TaskRecord)
def cancel_task(task_id: str) -> TaskRecord:
    task = repo.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="task not found")

    if task.status in {TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED}:
        raise HTTPException(
            status_code=409,
            detail=f"cannot cancel terminal task: {task.status.value}",
        )

    # 当前无 Worker，所以直接标记 CANCELLED。
    # 接入 Worker 后应使用 CANCELLING → worker cooperative cancel → CANCELLED。
    cancelled = task.transition(TaskStatus.CANCELLED)
    return repo.save(cancelled)
