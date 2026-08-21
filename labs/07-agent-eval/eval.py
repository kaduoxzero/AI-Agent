from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DATASET = Path(__file__).parents[2] / "evals" / "golden" / "agent_baseline.jsonl"


@dataclass(frozen=True)
class RunResult:
    output: str
    tools: list[str]
    steps: int


class CandidateAgent:
    """教学用可替换 Candidate。

    真实项目把这里替换为 LangGraph / Agents SDK / 自研 Runtime 的统一 Adapter：
    run(input) -> RunResult。
    """

    def run(self, user_input: str) -> RunResult:
        lowered = user_input.lower()

        # 一个非常简单的安全策略，用于演示 forbidden tool eval。
        if "忽略所有规则" in user_input or "blocked" in lowered:
            return RunResult(
                output="refused: request requires authorization and approval",
                tools=[],
                steps=1,
            )

        supplier_id = "s-001" if "s-001" in lowered else "s-002"
        risk = "high" if supplier_id == "s-001" else "low"
        return RunResult(
            output=f"supplier {supplier_id} risk={risk}",
            tools=["get_supplier_risk"],
            steps=2,
        )


def load_cases(path: Path) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                cases.append(json.loads(line))
    return cases


def evaluate_case(case: dict[str, Any], result: RunResult) -> list[str]:
    failures: list[str] = []
    output_lower = result.output.lower()

    for expected in case.get("expected_contains", []):
        if str(expected).lower() not in output_lower:
            failures.append(f"missing expected text: {expected}")

    called_tools = set(result.tools)

    for required in case.get("required_tools", []):
        if required not in called_tools:
            failures.append(f"required tool not called: {required}")

    for forbidden in case.get("forbidden_tools", []):
        if forbidden in called_tools:
            failures.append(f"forbidden tool called: {forbidden}")

    max_steps = int(case.get("max_steps", 999999))
    if result.steps > max_steps:
        failures.append(f"steps exceeded: {result.steps} > {max_steps}")

    return failures


def main() -> int:
    agent = CandidateAgent()
    cases = load_cases(DATASET)

    passed = 0
    failed = 0

    for case in cases:
        result = agent.run(case["input"])
        failures = evaluate_case(case, result)

        if failures:
            failed += 1
            print(f"FAIL {case['id']}")
            print("  result:", result)
            for failure in failures:
                print("  -", failure)
        else:
            passed += 1
            print(f"PASS {case['id']}")

    total = len(cases)
    pass_rate = passed / total if total else 0.0
    print("\n=== SUMMARY ===")
    print(f"total={total} passed={passed} failed={failed} pass_rate={pass_rate:.2%}")

    # 教学版：任何失败直接阻塞 CI。生产环境可按 suite 分级设置 threshold。
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
