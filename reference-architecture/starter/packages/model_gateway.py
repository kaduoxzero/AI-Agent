from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from packages.contracts import Evidence, TaskRecord


class ModelProvider(Protocol):
    name: str
    async def plan(self, query: str) -> list[str]: ...
    async def synthesize(self, query: str, evidence: list[Evidence]) -> dict: ...


class DeterministicProvider:
    """Offline provider used by the reference implementation and CI.

    Replace this adapter with OpenAI/Anthropic/Gemini/DeepSeek etc. The runtime
    depends on ModelGateway, not on a vendor SDK.
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

    async def plan(self, task: TaskRecord) -> list[str]:
        return await self.provider.plan(task.query)

    async def synthesize(self, task: TaskRecord, evidence: list[Evidence]) -> dict:
        return await self.provider.synthesize(task.query, evidence)
