from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Evidence(BaseModel):
    model_config = ConfigDict(extra="forbid")
    evidence_id: str
    source: str
    claim: str


class EvidenceSet(BaseModel):
    model_config = ConfigDict(extra="forbid")
    schema_version: str = "1.0"
    items: list[Evidence]


class DataSnapshot(BaseModel):
    model_config = ConfigDict(extra="forbid")
    schema_version: str = "1.0"
    supplier_id: str
    late_deliveries_30d: int = Field(ge=0)
    incidents_90d: int = Field(ge=0)


class ReviewResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    schema_version: str = "1.0"
    risk_level: Literal["low", "medium", "high"]
    reasons: list[str]
    evidence_ids: list[str]


class ResearchWorker:
    def run(self, supplier_id: str) -> EvidenceSet:
        # Worker 只看到完成检索任务所需的 supplier_id。
        return EvidenceSet(
            items=[
                Evidence(
                    evidence_id="ev-news-001",
                    source="public-news",
                    claim=f"{supplier_id} 最近出现交付延迟相关公开信息。",
                )
            ]
        )


class DataWorker:
    def run(self, supplier_id: str) -> DataSnapshot:
        # Worker 只返回结构化业务指标，不做最终风险结论。
        return DataSnapshot(
            supplier_id=supplier_id,
            late_deliveries_30d=3,
            incidents_90d=1,
        )


class Reviewer:
    def run(self, evidence: EvidenceSet, data: DataSnapshot) -> ReviewResult:
        score = data.late_deliveries_30d * 12 + data.incidents_90d * 25
        level: Literal["low", "medium", "high"]
        level = "high" if score >= 60 else "medium" if score >= 30 else "low"

        return ReviewResult(
            risk_level=level,
            reasons=[
                f"late_deliveries_30d={data.late_deliveries_30d}",
                f"incidents_90d={data.incidents_90d}",
                "public evidence available" if evidence.items else "no public evidence",
            ],
            evidence_ids=[item.evidence_id for item in evidence.items],
        )


class Supervisor:
    def __init__(self, max_workers: int = 2, max_steps: int = 5) -> None:
        self.max_workers = max_workers
        self.max_steps = max_steps
        self.steps = 0
        self.events: list[dict[str, object]] = []
        self.research = ResearchWorker()
        self.data = DataWorker()
        self.reviewer = Reviewer()

    def run(self, supplier_id: str) -> ReviewResult:
        if self.max_workers < 2:
            raise RuntimeError("this workflow requires at least two parallel workers")

        self._step("SupervisorStarted")

        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            research_future = pool.submit(self.research.run, supplier_id)
            data_future = pool.submit(self.data.run, supplier_id)
            evidence = research_future.result()
            snapshot = data_future.result()

        self._step(
            "WorkersCompleted",
            artifact_types=[type(evidence).__name__, type(snapshot).__name__],
        )

        result = self.reviewer.run(evidence, snapshot)
        self._step("ReviewerCompleted", risk_level=result.risk_level)
        return result

    def _step(self, event: str, **payload: object) -> None:
        self.steps += 1
        if self.steps > self.max_steps:
            raise RuntimeError("max_steps exceeded")
        self.events.append({"event": event, "step": self.steps, **payload})


def main() -> None:
    supervisor = Supervisor(max_workers=2, max_steps=5)
    result = supervisor.run("s-001")

    print("FINAL ARTIFACT:")
    print(result.model_dump_json(indent=2))

    print("\nEVENTS:")
    for event in supervisor.events:
        print(event)


if __name__ == "__main__":
    main()
