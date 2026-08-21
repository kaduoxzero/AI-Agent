from __future__ import annotations

import json
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError


class RiskAssessment(BaseModel):
    """Agent 的机器可消费输出，而不是面向用户的自由文本。"""

    model_config = ConfigDict(extra="forbid")

    risk_level: Literal["low", "medium", "high"]
    confidence: float = Field(ge=0.0, le=1.0)
    summary: str = Field(min_length=1, max_length=500)
    evidence_ids: list[str] = Field(default_factory=list, max_length=20)


def parse_model_output(raw: str) -> RiskAssessment:
    """先解析 JSON，再执行严格 Schema 校验；任何失败都向上抛出。"""
    payload = json.loads(raw)
    return RiskAssessment.model_validate(payload)


def main() -> None:
    samples = {
        "valid": json.dumps(
            {
                "risk_level": "high",
                "confidence": 0.91,
                "summary": "供应商出现连续交付异常，需要升级审核。",
                "evidence_ids": ["ev-001", "ev-002"],
            },
            ensure_ascii=False,
        ),
        "invalid_enum": '{"risk_level":"critical","confidence":0.8,"summary":"x"}',
        "invalid_range": '{"risk_level":"low","confidence":1.4,"summary":"x"}',
        "unknown_field": '{"risk_level":"medium","confidence":0.7,"summary":"x","admin":true}',
    }

    for name, raw in samples.items():
        print(f"\n=== {name} ===")
        try:
            result = parse_model_output(raw)
            print("PASS", result.model_dump())
        except (json.JSONDecodeError, ValidationError) as exc:
            print("REJECTED")
            print(exc)


if __name__ == "__main__":
    main()
