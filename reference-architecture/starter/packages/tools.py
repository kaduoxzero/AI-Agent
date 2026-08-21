from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Awaitable, Callable

from packages.contracts import Evidence, TaskRecord


class ToolRisk(str, Enum):
    READ_ONLY = "READ_ONLY"
    WRITE = "WRITE"
    DESTRUCTIVE = "DESTRUCTIVE"


@dataclass(frozen=True)
class ToolSpec:
    name: str
    risk: ToolRisk
    required_scope: str
    handler: Callable[[TaskRecord, dict[str, Any]], Awaitable[list[Evidence]]]


async def get_supplier_metrics(task: TaskRecord, args: dict[str, Any]) -> list[Evidence]:
    supplier = str(args.get("supplier", "supplier-a"))
    return [
        Evidence(
            source_type="structured_data",
            source_id=f"metrics:{task.tenant_id}:{supplier}",
            content="on_time_delivery_rate=0.82, incidents_30d=3",
            confidence=0.98,
        )
    ]


async def search_public_sources(task: TaskRecord, args: dict[str, Any]) -> list[Evidence]:
    return [
        Evidence(
            source_type="public_search",
            source_id="offline-public-source",
            content="离线 Starter 使用模拟公开来源；生产实现应接 Search/MCP Provider 并保留 Citation。",
            confidence=0.7,
        )
    ]


class ToolGateway:
    def __init__(self) -> None:
        self.tools = {
            "get_supplier_metrics": ToolSpec(
                "get_supplier_metrics", ToolRisk.READ_ONLY, "data:read", get_supplier_metrics
            ),
            "search_public_sources": ToolSpec(
                "search_public_sources", ToolRisk.READ_ONLY, "web:read", search_public_sources
            ),
        }

    async def call(
        self,
        task: TaskRecord,
        name: str,
        args: dict[str, Any],
        granted_scopes: set[str],
    ) -> list[Evidence]:
        spec = self.tools.get(name)
        if spec is None:
            raise ValueError(f"unknown tool: {name}")
        if spec.required_scope not in granted_scopes:
            raise PermissionError(f"missing scope: {spec.required_scope}")
        return await spec.handler(task, args)
