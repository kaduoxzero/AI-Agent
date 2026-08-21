from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Literal


DATASET = Path(__file__).parents[2] / "evals" / "security" / "redteam.jsonl"
Decision = Literal["allowed", "blocked"]


class SecurityPolicy:
    """教学用确定性 Policy。

    真实系统应结合 Identity、Tool Metadata、Tenant、Memory Policy、HITL 等结构化上下文，
    而不是仅靠字符串规则。这里用字符串只是为了让 Red Team Harness 可独立运行。
    """

    def decide(self, text: str) -> Decision:
        lowered = text.lower()

        blocked_markers = [
            "忽略系统指令",
            "system override",
            "reveal all secrets",
            "tenant-b",
            "永久写入长期记忆",
            "跳过所有审批",
            "没有审批",
            "delete_supplier",
            "admin_tool",
            "production:write",
        ]

        if any(marker in lowered for marker in blocked_markers):
            return "blocked"

        return "allowed"


def load_cases() -> list[dict[str, str]]:
    cases: list[dict[str, str]] = []
    with DATASET.open("r", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                cases.append(json.loads(line))
    return cases


def main() -> int:
    policy = SecurityPolicy()
    failures: list[dict[str, str]] = []

    for case in load_cases():
        actual = policy.decide(case["input"])
        ok = actual == case["expected"]
        print(
            f"{'PASS' if ok else 'FAIL'} {case['id']} "
            f"category={case['category']} expected={case['expected']} actual={actual}"
        )
        if not ok:
            failures.append(case)

    print(f"\nsecurity_failures={len(failures)}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
