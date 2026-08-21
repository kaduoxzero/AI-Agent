from __future__ import annotations

from prometheus_client import Counter, Histogram


TASKS_CREATED = Counter(
    "agent_tasks_created_total",
    "Created Agent tasks",
    ["agent_id", "agent_version"],
)
TASK_RUNS = Counter(
    "agent_task_runs_total",
    "Agent run terminal outcomes",
    ["agent_id", "agent_version", "status"],
)
MODEL_CALLS = Counter(
    "agent_model_calls_total",
    "Model calls by operation and route",
    ["agent_id", "agent_version", "operation", "model_route"],
)
TOOL_CALLS = Counter(
    "agent_tool_calls_total",
    "Tool calls by tool name",
    ["agent_id", "agent_version", "tool"],
)
APPROVALS = Counter(
    "agent_approval_total",
    "Human approval decisions",
    ["decision"],
)
TASK_DURATION = Histogram(
    "agent_task_run_duration_seconds",
    "Duration of a worker Agent run attempt",
    ["agent_id", "agent_version", "status"],
    buckets=(0.01, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10, 30, 60, 120, 300),
)
TASK_COST = Histogram(
    "agent_task_estimated_cost_usd",
    "Estimated cumulative model cost at run completion",
    ["agent_id", "agent_version"],
    buckets=(0.0001, 0.001, 0.01, 0.05, 0.1, 0.5, 1, 2, 5, 10),
)
