from __future__ import annotations

from typing import Any, Literal, TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt


class WorkflowState(TypedDict, total=False):
    supplier_id: str
    risk_level: Literal["low", "medium", "high"]
    proposed_action: str
    approved: bool
    reviewer: str
    execution_result: str


def analyze(state: WorkflowState) -> WorkflowState:
    return {
        "risk_level": "high",
        "proposed_action": f"block supplier {state['supplier_id']}",
    }


def approval(state: WorkflowState) -> WorkflowState:
    decision: dict[str, Any] = interrupt(
        {
            "type": "supplier_action_approval",
            "supplier_id": state["supplier_id"],
            "risk_level": state["risk_level"],
            "proposed_action": state["proposed_action"],
            "question": "是否批准执行高风险供应商处置？",
        }
    )
    return {
        "approved": bool(decision.get("approved", False)),
        "reviewer": str(decision.get("reviewer", "unknown")),
    }


def route_after_approval(state: WorkflowState) -> Literal["execute", "reject"]:
    return "execute" if state.get("approved") else "reject"


def execute(state: WorkflowState) -> WorkflowState:
    # 实际项目中这里应调用受权限控制、支持幂等和审计的 Write Tool。
    return {
        "execution_result": (
            f"EXECUTED by {state.get('reviewer')}: {state['proposed_action']}"
        )
    }


def reject(state: WorkflowState) -> WorkflowState:
    return {
        "execution_result": (
            f"REJECTED by {state.get('reviewer')}: {state['proposed_action']}"
        )
    }


def build_graph():
    builder = StateGraph(WorkflowState)
    builder.add_node("analyze", analyze)
    builder.add_node("approval", approval)
    builder.add_node("execute", execute)
    builder.add_node("reject", reject)

    builder.add_edge(START, "analyze")
    builder.add_edge("analyze", "approval")
    builder.add_conditional_edges(
        "approval",
        route_after_approval,
        {
            "execute": "execute",
            "reject": "reject",
        },
    )
    builder.add_edge("execute", END)
    builder.add_edge("reject", END)

    return builder.compile(checkpointer=InMemorySaver())


def main() -> None:
    graph = build_graph()
    config = {"configurable": {"thread_id": "supplier-review-demo-001"}}

    print("=== FIRST RUN: expected to interrupt ===")
    first = graph.invoke({"supplier_id": "s-001"}, config)
    print(first)

    print("\n=== RESUME: approve ===")
    resumed = graph.invoke(
        Command(resume={"approved": True, "reviewer": "alice"}),
        config,
    )
    print(resumed)


if __name__ == "__main__":
    main()
