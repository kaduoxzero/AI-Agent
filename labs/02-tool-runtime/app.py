from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout
from dataclasses import dataclass
from typing import Any, Callable, Literal, Type

from pydantic import BaseModel, ConfigDict, Field, ValidationError


class ToolError(Exception):
    pass


class AuthorizationError(ToolError):
    pass


class ToolTimeoutError(ToolError):
    pass


class SupplierQuery(BaseModel):
    model_config = ConfigDict(extra="forbid")
    supplier_id: str = Field(min_length=1)


class SupplierUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    supplier_id: str = Field(min_length=1)
    status: Literal["active", "review", "blocked"]


class SlowArgs(BaseModel):
    seconds: float = Field(ge=0, le=10)


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    args_model: Type[BaseModel]
    handler: Callable[[BaseModel], Any]
    side_effect: Literal["read", "write"] = "read"
    required_scope: str | None = None
    timeout_seconds: float = 2.0


SUPPLIERS = {
    "s-001": {"name": "Acme Components", "status": "active"},
}

IDEMPOTENCY_CACHE: dict[str, Any] = {}
AUDIT_LOG: list[dict[str, Any]] = []


def get_supplier(args: SupplierQuery) -> dict[str, Any]:
    return SUPPLIERS.get(args.supplier_id, {"error": "not_found"})


def update_supplier_status(args: SupplierUpdate) -> dict[str, Any]:
    supplier = SUPPLIERS.setdefault(args.supplier_id, {"name": "unknown"})
    supplier["status"] = args.status
    return {"supplier_id": args.supplier_id, "status": args.status}


def slow_tool(args: SlowArgs) -> dict[str, Any]:
    time.sleep(args.seconds)
    return {"slept": args.seconds}


TOOLS = {
    "get_supplier": ToolDefinition(
        name="get_supplier",
        args_model=SupplierQuery,
        handler=get_supplier,
        side_effect="read",
        required_scope="supplier:read",
    ),
    "update_supplier_status": ToolDefinition(
        name="update_supplier_status",
        args_model=SupplierUpdate,
        handler=update_supplier_status,
        side_effect="write",
        required_scope="supplier:write",
    ),
    "slow_tool": ToolDefinition(
        name="slow_tool",
        args_model=SlowArgs,
        handler=slow_tool,
        timeout_seconds=0.3,
    ),
}


class ToolRuntime:
    def __init__(self, scopes: set[str], actor: str) -> None:
        self.scopes = scopes
        self.actor = actor

    def execute(
        self,
        tool_name: str,
        raw_args: dict[str, Any],
        *,
        idempotency_key: str | None = None,
    ) -> Any:
        if tool_name not in TOOLS:
            raise ToolError(f"unknown tool: {tool_name}")

        tool = TOOLS[tool_name]
        self._authorize(tool)

        try:
            args = tool.args_model.model_validate(raw_args)
        except ValidationError as exc:
            self._audit(tool, "ToolRejected", {"reason": "invalid_arguments"})
            raise ToolError(f"invalid arguments: {exc}") from exc

        if tool.side_effect == "write":
            if not idempotency_key:
                raise ToolError("write tool requires idempotency_key")
            cache_key = f"{tool.name}:{idempotency_key}"
            if cache_key in IDEMPOTENCY_CACHE:
                self._audit(tool, "ToolDeduplicated", {"idempotency_key": idempotency_key})
                return IDEMPOTENCY_CACHE[cache_key]
        else:
            cache_key = None

        self._audit(tool, "ToolStarted", {"args": args.model_dump()})
        started = time.perf_counter()

        with ThreadPoolExecutor(max_workers=1) as pool:
            future = pool.submit(tool.handler, args)
            try:
                result = future.result(timeout=tool.timeout_seconds)
            except FutureTimeout as exc:
                future.cancel()
                self._audit(tool, "ToolFailed", {"reason": "timeout"})
                raise ToolTimeoutError(
                    f"tool {tool.name} exceeded {tool.timeout_seconds}s"
                ) from exc
            except Exception as exc:
                self._audit(tool, "ToolFailed", {"reason": type(exc).__name__})
                raise ToolError(f"tool {tool.name} failed") from exc

        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
        self._audit(tool, "ToolCompleted", {"elapsed_ms": elapsed_ms})

        if cache_key is not None:
            IDEMPOTENCY_CACHE[cache_key] = result

        return result

    def _authorize(self, tool: ToolDefinition) -> None:
        if tool.required_scope and tool.required_scope not in self.scopes:
            self._audit(tool, "ToolRejected", {"reason": "forbidden"})
            raise AuthorizationError(
                f"actor={self.actor} lacks scope={tool.required_scope}"
            )

    def _audit(self, tool: ToolDefinition, event: str, detail: dict[str, Any]) -> None:
        AUDIT_LOG.append(
            {
                "event": event,
                "actor": self.actor,
                "tool": tool.name,
                "side_effect": tool.side_effect,
                "detail": detail,
            }
        )


def main() -> None:
    read_only = ToolRuntime(scopes={"supplier:read"}, actor="agent:research")
    privileged = ToolRuntime(
        scopes={"supplier:read", "supplier:write"}, actor="agent:operator"
    )

    print("1) read:")
    print(read_only.execute("get_supplier", {"supplier_id": "s-001"}))

    print("\n2) unauthorized write:")
    try:
        read_only.execute(
            "update_supplier_status",
            {"supplier_id": "s-001", "status": "review"},
            idempotency_key="req-001",
        )
    except ToolError as exc:
        print(type(exc).__name__, exc)

    print("\n3) authorized write + idempotent retry:")
    first = privileged.execute(
        "update_supplier_status",
        {"supplier_id": "s-001", "status": "review"},
        idempotency_key="req-002",
    )
    second = privileged.execute(
        "update_supplier_status",
        {"supplier_id": "s-001", "status": "review"},
        idempotency_key="req-002",
    )
    print(first)
    print(second)

    print("\n4) timeout:")
    try:
        privileged.execute("slow_tool", {"seconds": 1.0})
    except ToolError as exc:
        print(type(exc).__name__, exc)

    print("\n5) audit events:")
    for event in AUDIT_LOG:
        print(event)


if __name__ == "__main__":
    main()
