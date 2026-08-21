from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    text: str


DOCUMENTS = {
    "delivery": Evidence("ev-delivery", "供应商A最近30天发生3次延迟交付，其中2次超过5天。"),
    "policy": Evidence("ev-policy", "规则要求：30天内3次及以上延迟交付，需要进入人工风险复核。"),
    "quality": Evidence("ev-quality", "供应商A最近一次质量抽检通过率为98.7%。"),
}


class Retriever:
    def search(self, query: str) -> list[Evidence]:
        results: list[Evidence] = []
        if any(word in query for word in ["延迟", "交付", "供应商A"]):
            results.append(DOCUMENTS["delivery"])
        if any(word in query for word in ["规则", "阈值", "复核", "风险"]):
            results.append(DOCUMENTS["policy"])
        if "质量" in query:
            results.append(DOCUMENTS["quality"])
        return results


class AgenticRAG:
    def __init__(self, retriever: Retriever, max_retrieval_rounds: int = 2) -> None:
        self.retriever = retriever
        self.max_retrieval_rounds = max_retrieval_rounds
        self.trajectory: list[dict[str, object]] = []

    def run(self, user_query: str) -> dict[str, object]:
        evidence: dict[str, Evidence] = {}
        query = self._rewrite(user_query, round_no=1)

        for round_no in range(1, self.max_retrieval_rounds + 1):
            self.trajectory.append(
                {"event": "RetrievalStarted", "round": round_no, "query": query}
            )
            found = self.retriever.search(query)
            for item in found:
                evidence[item.evidence_id] = item

            self.trajectory.append(
                {
                    "event": "RetrievalCompleted",
                    "round": round_no,
                    "evidence_ids": list(evidence),
                }
            )

            if self._sufficient(user_query, list(evidence.values())):
                return {
                    "status": "ok",
                    "answer": self._answer(list(evidence.values())),
                    "evidence_ids": list(evidence),
                    "trajectory": self.trajectory,
                }

            if round_no < self.max_retrieval_rounds:
                query = self._rewrite(user_query, round_no=round_no + 1)

        return {
            "status": "evidence_insufficient",
            "answer": "达到检索预算后，现有证据仍不足以支持结论。",
            "evidence_ids": list(evidence),
            "trajectory": self.trajectory,
        }

    @staticmethod
    def _rewrite(user_query: str, round_no: int) -> str:
        if round_no == 1:
            return f"{user_query} 延迟交付"
        return f"{user_query} 风险规则 复核阈值"

    @staticmethod
    def _sufficient(user_query: str, evidence: list[Evidence]) -> bool:
        # 此案例要求同时具备“事实证据”和“规则证据”，才允许得出风险处置结论。
        ids = {item.evidence_id for item in evidence}
        return {"ev-delivery", "ev-policy"}.issubset(ids)

    @staticmethod
    def _answer(evidence: list[Evidence]) -> str:
        facts = "；".join(item.text for item in evidence)
        return f"根据证据：{facts} 因此该供应商应进入人工风险复核。"


def main() -> None:
    agent = AgenticRAG(Retriever(), max_retrieval_rounds=2)
    result = agent.run("供应商A目前是否需要升级风险处理？")

    print("STATUS:", result["status"])
    print("ANSWER:", result["answer"])
    print("EVIDENCE:", result["evidence_ids"])
    print("\nTRAJECTORY:")
    for event in result["trajectory"]:
        print(event)


if __name__ == "__main__":
    main()
