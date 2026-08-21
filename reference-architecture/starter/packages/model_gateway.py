from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Protocol, TypeVar

from packages.contracts import Evidence, TaskRecord


T = TypeVar("T")


@dataclass(frozen=True)
class ModelUsage:
    provider: str
    model_route: str
    input_tokens: int
    output_tokens: int
    estimated_cost_usd: float


@dataclass(frozen=True)
class ModelResult(Generic[T]):
    value: T
    usage: ModelUsage


class ModelProvider(Protocol):
    name: str
    async def plan(self, query: str) -> list[str]: ...
    async def synthesize(self, query: str, evidence: list[Evidence]) -> dict: ...


class DeterministicProvider:
    """Offline provider used by the reference implementation and CI.

    Replace this adapter with a real Provider. The runtime depends on
    ModelGateway and receives usage metadata rather than importing vendor SDKs.
    """

    name = "deterministic-local"

    async def plan(self, query: str) -> list[str]:
        steps = ["retrieve_internal_knowledge"]
        if any(word in query.lower() for word in ["public", "新闻", "web", "公开"]):
            steps.append("search_public_sources")
        if any(word in query.lower() for word in ["risk", "风险", "supplier", "供应商", "指标"]):
            steps.append("load_structured_metrics")
        steps.append("review_and_synthesize")
        return steps

    async def synthesize(self, query: str, evidence: list[Evidence]) -> dict:
        confidence = 0.0 if not evidence else min(0.95, 0.55 + len(evidence) * 0.1)
        return {
            "query": query,
            "summary": "基于可追溯 Evidence 生成的参考结果。",
            "evidence_count": len(evidence),
            "confidence": round(confidence, 2),
            "recommendations": [
                "在真实业务中将 DeterministicProvider 替换为经过 Eval 的模型 Provider。",
                "高影响 Action 必须经过 Policy 与 HITL。",
            ],
        }


@dataclass
class ModelGateway:
    provider: ModelProvider

    # Reference prices are intentionally synthetic; real adapters should map the
    # provider's returned usage and configured price catalog into ModelUsage.
    route_price_per_1k: dict[str, float] | None = None

    def _usage(self, task: TaskRecord, prompt_chars: int, output_chars: int) -> ModelUsage:
        input_tokens = max(1, prompt_chars // 4)
        output_tokens = max(1, output_chars // 4)
        prices = self.route_price_per_1k or {"default": 0.005, "fast": 0.001, "reasoning": 0.02}
        price = prices.get(task.model_route, prices["default"])
        cost = (input_tokens + output_tokens) / 1000 * price
        return ModelUsage(
            provider=self.provider.name,
            model_route=task.model_route,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            estimated_cost_usd=round(cost, 8),
        )

    async def plan(self, task: TaskRecord) -> ModelResult[list[str]]:
        value = await self.provider.plan(task.query)
        output_text = "\n".join(value)
        return ModelResult(
            value=value,
            usage=self._usage(task, len(task.query), len(output_text)),
        )

    async def synthesize(
        self, task: TaskRecord, evidence: list[Evidence]
    ) -> ModelResult[dict]:
        value = await self.provider.synthesize(task.query, evidence)
        prompt_chars = len(task.query) + sum(len(item.content) for item in evidence)
        return ModelResult(
            value=value,
            usage=self._usage(task, prompt_chars, len(str(value))),
        )
