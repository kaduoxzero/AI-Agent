# Agent Design Decision Ledger

> 用于记录 Guided Builder 过程中所有关键决策，避免 Agent 在后续实现时遗忘、漂移或重新解释用户选择。

## Session Metadata

- Project:
- Mode: Greenfield / Existing Project
- User Goal:
- Primary Skill:
- Started At:
- Last Updated:

## Decision Status

- `Proposed`：已提出，尚未确认
- `Accepted`：用户确认或明确授权 Agent 采用推荐项
- `Rejected`：明确不采用
- `Deferred`：当前不实现，但需要记录
- `Superseded`：被后续决策替代

## Decision Table

| ID | Topic | Status | Decision | Why | Trade-offs | Verification |
|---|---|---|---|---|---|---|
| D-001 | | | | | | |

---

## Decision Detail Template

### D-XXX — <Topic>

**Status:** Proposed / Accepted / Rejected / Deferred / Superseded

**Question**

需要解决什么工程决策？

**Options Considered**

- A.
- B.
- C.

**Recommended Option**

- Option:
- Reason:

**Final Decision**


**Why**


**Trade-offs**

- Complexity:
- Latency:
- Cost:
- Reliability:
- Security:
- Maintainability:

**New Boundaries Introduced**

- State:
- Context:
- Tool:
- Permission:
- Data:
- Runtime:

**Affected Components**


**Verification**


**Rollback / Revisit Trigger**

在什么条件下需要重新评估这个决策？

---

## Recommended Mandatory Decisions

至少应记录这些主题中的关键项：

- D-001 Business Goal / Out-of-Scope
- D-002 Architecture Level: Workflow / Single Agent / Multi-Agent
- D-003 Autonomy Level
- D-004 Knowledge Sources / RAG
- D-005 Tool and Side-Effect Model
- D-006 State / Memory / Checkpoint
- D-007 Multi-Agent Split Decision
- D-008 Identity / Permission
- D-009 HITL Policy
- D-010 Runtime / Queue / Worker
- D-011 Budget / Termination
- D-012 Eval / Release Gate
- D-013 Observability
- D-014 Deployment

## Architecture Freeze Summary

```text
Goal:
Out-of-Scope:
Architecture:
Autonomy:
Knowledge:
Tools:
State / Memory:
Multi-Agent:
Identity / Permission:
HITL:
Runtime:
Budget:
Eval:
Observability:
Deployment:
```

只有这里与 Agent Boundary Canvas 一致后，才进入大规模实现。
