from __future__ import annotations

import hashlib
from dataclasses import dataclass

from packages.contracts import AgentDefinition, EvalResult, ReleaseRoute


class ReleaseRejected(RuntimeError):
    pass


@dataclass
class AgentRegistry:
    min_eval_score: float = 0.8

    def __post_init__(self) -> None:
        self.definitions: dict[tuple[str, str], AgentDefinition] = {}
        self.routes: dict[str, ReleaseRoute] = {}
        self.evals: dict[tuple[str, str], list[EvalResult]] = {}

    def register(self, definition: AgentDefinition) -> AgentDefinition:
        self.definitions[(definition.agent_id, definition.version)] = definition
        return definition

    def record_eval(self, result: EvalResult) -> EvalResult:
        self.evals.setdefault((result.agent_id, result.version), []).append(result)
        return result

    def release(self, route: ReleaseRoute) -> ReleaseRoute:
        stable = self.definitions.get((route.agent_id, route.stable_version))
        if stable is None or not stable.enabled:
            raise ReleaseRejected("stable version is missing or disabled")
        if route.canary_version:
            canary = self.definitions.get((route.agent_id, route.canary_version))
            if canary is None or not canary.enabled:
                raise ReleaseRejected("canary version is missing or disabled")
            self._require_eval_gate(route.agent_id, route.canary_version)
        self.routes[route.agent_id] = route
        return route

    def _require_eval_gate(self, agent_id: str, version: str) -> None:
        results = self.evals.get((agent_id, version), [])
        if not results:
            raise ReleaseRejected("canary has no eval result")
        if not any(result.passed and result.score >= self.min_eval_score for result in results):
            raise ReleaseRejected(
                f"canary eval gate failed: required score >= {self.min_eval_score}"
            )

    def resolve(self, agent_id: str, routing_key: str) -> AgentDefinition:
        route = self.routes.get(agent_id)
        if route is None:
            candidates = [
                definition
                for (registered_id, _), definition in self.definitions.items()
                if registered_id == agent_id and definition.enabled
            ]
            if not candidates:
                raise KeyError(f"unknown agent: {agent_id}")
            return sorted(candidates, key=lambda item: item.version)[-1]

        version = route.stable_version
        if route.canary_version and route.canary_percent > 0:
            bucket = int(hashlib.sha256(routing_key.encode("utf-8")).hexdigest()[:8], 16) % 100
            if bucket < route.canary_percent:
                version = route.canary_version
        definition = self.definitions.get((agent_id, version))
        if definition is None or not definition.enabled:
            raise KeyError(f"unavailable agent release: {agent_id}@{version}")
        return definition

    def list_agents(self) -> list[AgentDefinition]:
        return sorted(self.definitions.values(), key=lambda item: (item.agent_id, item.version))


def build_default_registry(min_eval_score: float = 0.8) -> AgentRegistry:
    registry = AgentRegistry(min_eval_score=min_eval_score)
    registry.register(
        AgentDefinition(
            agent_id="research-platform",
            version="1.0.0",
            prompt_version="research-v1",
            model_route="default",
            allowed_tools=["search_public_sources", "get_supplier_metrics"],
        )
    )
    registry.release(ReleaseRoute(agent_id="research-platform", stable_version="1.0.0"))
    return registry
