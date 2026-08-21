from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Protocol
from uuid import uuid4


class ProviderError(RuntimeError):
    pass


class RateLimited(ProviderError):
    pass


class QuotaExceeded(RuntimeError):
    pass


@dataclass(frozen=True)
class Capabilities:
    tool_calling: bool
    structured_output: bool
    reasoning: bool


@dataclass(frozen=True)
class ModelRequest:
    tenant_id: str
    task_type: Literal["chat", "tool", "reasoning"]
    prompt: str
    require_structured_output: bool = False


@dataclass(frozen=True)
class ModelResponse:
    trace_id: str
    provider: str
    model: str
    text: str
    input_tokens: int
    output_tokens: int
    estimated_cost: float


class Provider(Protocol):
    name: str
    model: str
    capabilities: Capabilities
    price_per_1k_tokens: float

    def complete(self, prompt: str) -> tuple[str, int, int]:
        ...


class FakeProvider:
    def __init__(
        self,
        name: str,
        model: str,
        capabilities: Capabilities,
        price_per_1k_tokens: float,
        *,
        fail_with_429: bool = False,
    ) -> None:
        self.name = name
        self.model = model
        self.capabilities = capabilities
        self.price_per_1k_tokens = price_per_1k_tokens
        self.fail_with_429 = fail_with_429

    def complete(self, prompt: str) -> tuple[str, int, int]:
        if self.fail_with_429:
            raise RateLimited(f"{self.name}/{self.model} simulated 429")
        input_tokens = max(1, len(prompt) // 4)
        output = f"[{self.name}/{self.model}] processed: {prompt[:60]}"
        output_tokens = max(1, len(output) // 4)
        return output, input_tokens, output_tokens


class QuotaStore:
    def __init__(self, limits: dict[str, int]) -> None:
        self.limits = limits
        self.usage: dict[str, int] = {}

    def consume(self, tenant_id: str, tokens: int) -> None:
        used = self.usage.get(tenant_id, 0)
        limit = self.limits.get(tenant_id, 10_000)
        if used + tokens > limit:
            raise QuotaExceeded(
                f"tenant={tenant_id} quota exceeded: {used + tokens} > {limit}"
            )
        self.usage[tenant_id] = used + tokens


class ModelGateway:
    def __init__(self, providers: list[Provider], quota: QuotaStore) -> None:
        self.providers = providers
        self.quota = quota
        self.usage_log: list[dict[str, object]] = []

    def complete(self, request: ModelRequest) -> ModelResponse:
        trace_id = str(uuid4())
        candidates = [p for p in self.providers if self._supports(p, request)]
        if not candidates:
            raise ProviderError("no provider satisfies requested capabilities")

        errors: list[str] = []
        for provider in candidates:
            try:
                text, input_tokens, output_tokens = provider.complete(request.prompt)
                total_tokens = input_tokens + output_tokens
                self.quota.consume(request.tenant_id, total_tokens)
                cost = total_tokens / 1000 * provider.price_per_1k_tokens
                response = ModelResponse(
                    trace_id=trace_id,
                    provider=provider.name,
                    model=provider.model,
                    text=text,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    estimated_cost=round(cost, 6),
                )
                self.usage_log.append(
                    {
                        "trace_id": trace_id,
                        "tenant_id": request.tenant_id,
                        "provider": provider.name,
                        "model": provider.model,
                        "tokens": total_tokens,
                        "estimated_cost": response.estimated_cost,
                    }
                )
                return response
            except RateLimited as exc:
                errors.append(str(exc))
                continue

        raise ProviderError(f"all eligible providers failed: {errors}")

    @staticmethod
    def _supports(provider: Provider, request: ModelRequest) -> bool:
        if request.task_type == "tool" and not provider.capabilities.tool_calling:
            return False
        if request.task_type == "reasoning" and not provider.capabilities.reasoning:
            return False
        if request.require_structured_output and not provider.capabilities.structured_output:
            return False
        return True


def main() -> None:
    cheap = FakeProvider(
        "provider-a",
        "fast-model",
        Capabilities(tool_calling=False, structured_output=True, reasoning=False),
        price_per_1k_tokens=0.001,
    )
    primary_tool = FakeProvider(
        "provider-b",
        "tool-model-primary",
        Capabilities(tool_calling=True, structured_output=True, reasoning=True),
        price_per_1k_tokens=0.01,
        fail_with_429=True,
    )
    fallback_tool = FakeProvider(
        "provider-c",
        "tool-model-fallback",
        Capabilities(tool_calling=True, structured_output=True, reasoning=True),
        price_per_1k_tokens=0.012,
    )

    gateway = ModelGateway(
        providers=[cheap, primary_tool, fallback_tool],
        quota=QuotaStore({"tenant-a": 500}),
    )

    print("=== chat task → cheap model ===")
    print(
        gateway.complete(
            ModelRequest(
                tenant_id="tenant-a",
                task_type="chat",
                prompt="总结今天的供应链异常",
            )
        )
    )

    print("\n=== tool task → primary 429 → compatible fallback ===")
    print(
        gateway.complete(
            ModelRequest(
                tenant_id="tenant-a",
                task_type="tool",
                prompt="查询 supplier s-001 并返回结构化风险",
                require_structured_output=True,
            )
        )
    )

    print("\n=== usage log ===")
    for item in gateway.usage_log:
        print(item)


if __name__ == "__main__":
    main()
