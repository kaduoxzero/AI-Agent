from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Literal


AgentStatus = Literal["draft", "active", "retired"]


@dataclass(frozen=True)
class AgentDefinition:
    agent_id: str
    version: str
    prompt_version: str
    model: str
    allowed_tools: tuple[str, ...]
    skills: tuple[str, ...]
    max_steps: int
    status: AgentStatus = "active"


@dataclass(frozen=True)
class Release:
    release_id: str
    agent_id: str
    stable_version: str
    canary_version: str | None
    canary_percent: int


class AgentRegistry:
    def __init__(self) -> None:
        self._definitions: dict[tuple[str, str], AgentDefinition] = {}

    def register(self, definition: AgentDefinition) -> None:
        key = (definition.agent_id, definition.version)
        if key in self._definitions:
            raise ValueError(f"agent version already exists: {key}")
        self._definitions[key] = definition

    def get(self, agent_id: str, version: str) -> AgentDefinition:
        try:
            definition = self._definitions[(agent_id, version)]
        except KeyError as exc:
            raise KeyError(f"agent version not found: {agent_id}@{version}") from exc
        if definition.status != "active":
            raise RuntimeError(f"agent version not active: {agent_id}@{version}")
        return definition


class ReleaseResolver:
    def __init__(self, registry: AgentRegistry, release: Release) -> None:
        if not 0 <= release.canary_percent <= 100:
            raise ValueError("canary_percent must be 0..100")
        if release.canary_version is None and release.canary_percent != 0:
            raise ValueError("canary_percent requires canary_version")
        self.registry = registry
        self.release = release

    def resolve(self, routing_key: str) -> AgentDefinition:
        bucket = self._bucket(routing_key)
        use_canary = (
            self.release.canary_version is not None
            and bucket < self.release.canary_percent
        )
        version = (
            self.release.canary_version
            if use_canary
            else self.release.stable_version
        )
        assert version is not None
        return self.registry.get(self.release.agent_id, version)

    @staticmethod
    def _bucket(routing_key: str) -> int:
        digest = hashlib.sha256(routing_key.encode("utf-8")).digest()
        return int.from_bytes(digest[:4], "big") % 100

    def rollback(self) -> None:
        self.release = Release(
            release_id=self.release.release_id + "-rollback",
            agent_id=self.release.agent_id,
            stable_version=self.release.stable_version,
            canary_version=None,
            canary_percent=0,
        )


def main() -> None:
    registry = AgentRegistry()

    registry.register(
        AgentDefinition(
            agent_id="supplier-risk",
            version="1.0.0",
            prompt_version="prompt-7",
            model="strong-model-v1",
            allowed_tools=("get_supplier", "search_kb"),
            skills=("risk-analysis@1",),
            max_steps=12,
        )
    )
    registry.register(
        AgentDefinition(
            agent_id="supplier-risk",
            version="1.1.0",
            prompt_version="prompt-8",
            model="strong-model-v2",
            allowed_tools=("get_supplier", "search_kb"),
            skills=("risk-analysis@2",),
            max_steps=10,
        )
    )

    release = Release(
        release_id="rel-2026-08-21",
        agent_id="supplier-risk",
        stable_version="1.0.0",
        canary_version="1.1.0",
        canary_percent=10,
    )
    resolver = ReleaseResolver(registry, release)

    print("=== deterministic canary routing ===")
    counts: dict[str, int] = {}
    for i in range(100):
        definition = resolver.resolve(f"tenant-a:task-{i}")
        counts[definition.version] = counts.get(definition.version, 0) + 1
    print(counts)

    key = "tenant-a:important-task"
    first = resolver.resolve(key)
    second = resolver.resolve(key)
    print("stable routing for same key:", first.version, second.version)

    print("\n=== rollback ===")
    resolver.rollback()
    after = resolver.resolve(key)
    print("version after rollback:", after.version)
    print("release:", resolver.release)


if __name__ == "__main__":
    main()
