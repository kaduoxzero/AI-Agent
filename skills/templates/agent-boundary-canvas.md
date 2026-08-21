# Agent Boundary Canvas

> 用于在设计或修改 Agent 前，系统地确认“它能做什么、不能做什么、能访问什么、能决定什么、什么时候必须停下来”。

## 1. Goal Boundary

- Primary Goal:
- Business Outcome:
- Explicit Out-of-Scope:
- Non-Goals:

## 2. User Boundary

- Intended Users:
- Disallowed Users:
- Tenant Model:
- Identity Source:

## 3. Input Boundary

- Accepted Inputs:
- Untrusted Inputs:
- File / Image / Audio / Web Inputs:
- Max Input Size:

## 4. Output Boundary

- Output Artifact:
- Structured Schema:
- Citation Required: Yes / No
- Human Editable: Yes / No

## 5. Autonomy Boundary

### Agent may decide

- [ ] Whether to retrieve
- [ ] Which Tool to call
- [ ] Tool order
- [ ] Retry
- [ ] Task decomposition
- [ ] Delegation
- [ ] Other:

### Agent may NOT decide

- Permission policy:
- Budget increase:
- High-risk approval:
- Security bypass:
- Other:

Autonomy Level: A0 / A1 / A2 / A3 / A4

## 6. Knowledge Boundary

| Source | Read | Write | Trust Level | Tenant Filter | Citation | Notes |
|---|---|---|---|---|---|---|
| Model Knowledge | | | | | | |
| Enterprise KB | | | | | | |
| Database | | | | | | |
| Web | | | | | | |
| User Files | | | | | | |
| Memory | | | | | | |

## 7. Tool / Capability Boundary

| Tool | Type | Permission Scope | Side Effect | Idempotent | HITL | Timeout | Retry |
|---|---|---|---|---|---|---|---|
| | Read / Write / Destructive | | | | | | |

## 8. Data & Permission Boundary

- User Identity:
- Agent Identity:
- Tool Identity:
- Credential Source:
- RBAC / ABAC / Scope:
- Cross-Tenant Isolation:
- Secrets Handling:
- PII / Sensitive Data:

## 9. State / Session / Memory / Checkpoint

- Task State:
- Session State:
- Long-term Memory Needed: Yes / No
- Memory Write Policy:
- Memory TTL:
- Checkpoint Needed: Yes / No
- Resume Semantics:

## 10. Multi-Agent Boundary

Multi-Agent Needed: Yes / No / Deferred

Reason:

- [ ] Different permissions
- [ ] Different context
- [ ] Different tool sets
- [ ] Independent expertise
- [ ] Parallelizable work
- [ ] Independent reviewer
- [ ] Different lifecycle
- [ ] Different model requirements

Shared State Ownership:
Handoff / Artifact Contract:
Failure Propagation:

## 11. Time / Budget Boundary

- Max Steps:
- Max Model Calls:
- Max Tool Calls:
- Max Retry:
- Max Wall Clock:
- Token Budget:
- Cost Budget:
- Cancellation:

## 12. Safety / HITL Boundary

Human Approval Required For:

- [ ] Destructive actions
- [ ] Financial impact
- [ ] External communication
- [ ] Account / permission changes
- [ ] Sensitive data operations
- [ ] Low-confidence decisions
- [ ] Other:

Approval outcomes:

- Approve
- Reject
- Edit
- Escalate
- Timeout

Timeout behavior:

## 13. Failure Boundary

| Failure | Detect | Retry | Fallback | Resume | Escalate | Rollback |
|---|---|---|---|---|---|---|
| Model failure | | | | | | |
| Tool failure | | | | | | |
| Retrieval failure | | | | | | |
| Worker crash | | | | | | |
| Budget exceeded | | | | | | |
| Approval timeout | | | | | | |
| Security violation | | | | | | |

## 14. Evaluation Boundary

- Golden Cases:
- Failure Cases:
- Security Cases:
- Tool / Trajectory Rules:
- Groundedness Requirement:
- Latency Target:
- Cost Target:
- Release Gate:

## 15. Observability Boundary

Required fields:

- [ ] Task ID
- [ ] Trace ID
- [ ] Agent Version
- [ ] Prompt Version
- [ ] Model Route
- [ ] Tool Calls
- [ ] Retrieval Evidence
- [ ] Events
- [ ] Latency
- [ ] Token
- [ ] Cost
- [ ] Approval
- [ ] Error Category
- [ ] Artifact

## Final Boundary Statement

> This Agent is allowed to ______, may autonomously decide ______, may access ______, must request human approval before ______, must stop when ______, and is considered successful when ______.
