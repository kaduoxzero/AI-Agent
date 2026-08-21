from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CircuitState(str, Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class DependencyError(RuntimeError):
    pass


@dataclass
class Metrics:
    requests: int = 0
    successes: int = 0
    dependency_failures: int = 0
    fallbacks: int = 0

    def report(self) -> dict[str, float | int]:
        success_rate = self.successes / self.requests if self.requests else 0.0
        return {
            "requests": self.requests,
            "successes": self.successes,
            "dependency_failures": self.dependency_failures,
            "fallbacks": self.fallbacks,
            "task_success_rate": round(success_rate, 4),
        }


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 2) -> None:
        self.failure_threshold = failure_threshold
        self.failures = 0
        self.state = CircuitState.CLOSED

    def before_call(self) -> None:
        if self.state == CircuitState.OPEN:
            raise DependencyError("circuit is open")

    def record_success(self) -> None:
        self.failures = 0
        self.state = CircuitState.CLOSED

    def record_failure(self) -> None:
        self.failures += 1
        if self.failures >= self.failure_threshold:
            self.state = CircuitState.OPEN

    def probe(self) -> None:
        """教学版：人工进入 HALF_OPEN，允许一次恢复探测。"""
        if self.state == CircuitState.OPEN:
            self.state = CircuitState.HALF_OPEN


class PublicSearch:
    def __init__(self) -> None:
        self.fail = False

    def search(self, query: str) -> str:
        if self.fail:
            raise DependencyError("public search unavailable")
        return f"public evidence for: {query}"


class InternalRAG:
    def search(self, query: str) -> str:
        return f"internal evidence for: {query}"


class ResearchService:
    def __init__(self) -> None:
        self.public = PublicSearch()
        self.internal = InternalRAG()
        self.breaker = CircuitBreaker(failure_threshold=2)
        self.metrics = Metrics()

    def run(self, query: str) -> dict[str, str]:
        self.metrics.requests += 1
        internal = self.internal.search(query)

        try:
            self.breaker.before_call()
            public = self.public.search(query)
            self.breaker.record_success()
            self.metrics.successes += 1
            return {
                "mode": "full",
                "evidence": f"{internal}; {public}",
                "warning": "",
            }
        except DependencyError as exc:
            self.metrics.dependency_failures += 1
            self.breaker.record_failure()
            self.metrics.fallbacks += 1
            self.metrics.successes += 1  # 降级后任务仍完成，但能力受限。
            return {
                "mode": "degraded",
                "evidence": internal,
                "warning": f"public search unavailable; evidence scope reduced: {exc}",
            }


def main() -> None:
    service = ResearchService()

    print("=== healthy ===")
    print(service.run("supplier s-001 risk"))

    print("\n=== inject public search failure ===")
    service.public.fail = True
    print(service.run("supplier s-001 risk"))
    print(service.run("supplier s-001 risk"))
    print("circuit:", service.breaker.state.value)

    print("\n=== circuit already open: immediate degraded mode ===")
    print(service.run("supplier s-001 risk"))

    print("\n=== repair dependency and half-open probe ===")
    service.public.fail = False
    service.breaker.probe()
    print(service.run("supplier s-001 risk"))
    print("circuit:", service.breaker.state.value)

    print("\n=== SLI metrics ===")
    print(service.metrics.report())


if __name__ == "__main__":
    main()
