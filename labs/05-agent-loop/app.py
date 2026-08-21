from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, Protocol


class BudgetExceeded(RuntimeError):
    pass


@dataclass(frozen=True)
class Decision:
    kind: Literal["tool", "final"]
    tool_name: str | None = None
    arguments: dict[str, Any] | None = None
    final_text: str | None = None


@dataclass
class AgentState:
    user_query: str
    observations: list[dict[str, Any]] = field(default_factory=list)
    final_answer: str | None = None


@dataclass(frozen=True)
class RuntimeBudget:
    max_turns: int = 5
    max_tool_calls: int = 3


class Model(Protocol):
    def decide(self, state: AgentState) -> Decision:
        ...


class DeterministicModel:
    """教学用 Model Adapter。

    第一次看到任务时调用 supplier tool；拿到 Observation 后输出 final。
    """

    def decide(self, state: AgentState) -> Decision:
        if not state.observations:
            return Decision(
                kind="tool",
                tool_name="get_supplier_risk",
                arguments={"supplier_id": "s-001"},
            )

        observation = state.observations[-1]
        return Decision(
            kind="final",
            final_text=(
                f"供应商 {observation['supplier_id']} 当前风险等级为 "
                f"{observation['risk_level']}，score={observation['score']}。"
            ),
        )


class ToolRegistry:
    def __init__(self) -> None:
        self._tools = {
            "get_supplier_risk": self._get_supplier_risk,
        }

    def call(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if name not in self._tools:
            raise KeyError(f"unknown tool: {name}")
        return self._tools[name](arguments)

    @staticmethod
    def _get_supplier_risk(arguments: dict[str, Any]) -> dict[str, Any]:
        supplier_id = str(arguments["supplier_id"])
        return {
            "supplier_id": supplier_id,
            "risk_level": "high",
            "score": 72,
            "evidence_ids": ["ev-001", "ev-002"],
        }


class AgentRuntime:
    def __init__(
        self,
        model: Model,
        tools: ToolRegistry,
        budget: RuntimeBudget,
    ) -> None:
        self.model = model
        self.tools = tools
        self.budget = budget
        self.events: list[dict[str, Any]] = []

    def run(self, query: str) -> AgentState:
        state = AgentState(user_query=query)
        tool_calls = 0

        for turn in range(1, self.budget.max_turns + 1):
            self._emit("TurnStarted", turn=turn)
            decision = self.model.decide(state)
            self._emit("ModelDecided", turn=turn, kind=decision.kind)

            if decision.kind == "final":
                state.final_answer = decision.final_text or ""
                self._emit("RunCompleted", turn=turn)
                return state

            if decision.kind != "tool" or not decision.tool_name:
                raise RuntimeError(f"invalid decision: {decision}")

            if tool_calls >= self.budget.max_tool_calls:
                self._emit("BudgetExceeded", budget="max_tool_calls")
                raise BudgetExceeded("max_tool_calls exceeded")

            tool_calls += 1
            self._emit(
                "ToolStarted",
                turn=turn,
                tool=decision.tool_name,
                arguments=decision.arguments or {},
            )
            observation = self.tools.call(
                decision.tool_name,
                decision.arguments or {},
            )
            state.observations.append(observation)
            self._emit(
                "ToolCompleted",
                turn=turn,
                tool=decision.tool_name,
                observation=observation,
            )

        self._emit("BudgetExceeded", budget="max_turns")
        raise BudgetExceeded("max_turns exceeded")

    def _emit(self, event: str, **payload: Any) -> None:
        self.events.append({"event": event, **payload})


def main() -> None:
    runtime = AgentRuntime(
        model=DeterministicModel(),
        tools=ToolRegistry(),
        budget=RuntimeBudget(max_turns=5, max_tool_calls=3),
    )

    state = runtime.run("请判断供应商 s-001 的风险")
    print("FINAL:", state.final_answer)
    print("\nTRAJECTORY:")
    for event in runtime.events:
        print(event)


if __name__ == "__main__":
    main()
