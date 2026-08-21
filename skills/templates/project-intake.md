# Agent Project Intake Template

> 用于从 0 到 1、新项目接手、重大改造前快速建立工程上下文。能从仓库直接推断的信息优先自动填写，不要反复询问用户。

## 1. Project Identity

```text
Project name:
Repository:
Current stage: idea / prototype / MVP / production
Primary language:
Framework:
Model provider:
Deployment target:
```

## 2. Business Goal

```text
Primary actor:
Primary goal:
Trigger:
Input:
Expected output:
Business value:
```

## 3. Execution Model

```text
Current architecture: function / workflow / single-agent / multi-agent
Who decides the next step:
Long-running task: yes / no
Async worker: yes / no
Human approval: yes / no
```

## 4. Agent Capabilities

```text
Prompt:
Structured Output:
Tools:
RAG:
Memory:
State:
Checkpoint:
Multi-Agent:
Browser / Computer Use:
Code / Shell execution:
```

## 5. Data & Knowledge

```text
Primary data sources:
Vector store:
Relational store:
Cache:
Artifact store:
Tenant isolation:
Knowledge freshness requirement:
```

## 6. Contracts

记录当前已有或计划中的：

```text
TaskRequest:
TaskRecord:
AgentState:
ToolInput / ToolOutput:
Evidence:
Artifact:
Event:
Error model:
```

## 7. Reliability

```text
Timeout:
Retry:
Fallback:
Max steps:
Max model calls:
Max tool calls:
Max cost:
Cancellation:
Resume:
Idempotency:
```

## 8. Security

```text
Identity source:
Permission model:
Tool scopes:
Sensitive actions:
Prompt injection boundary:
Secrets:
HITL:
Audit:
```

## 9. Quality & Evaluation

```text
Existing tests:
Existing evals:
Golden dataset:
Known failure cases:
Quality target:
Latency target:
Cost target:
Safety target:
```

## 10. Constraints

```text
Must preserve:
Cannot change:
Required compatibility:
Infrastructure constraints:
Deadline / scope constraints:
```

## 11. Current Risks

| Risk | Severity | Evidence | Mitigation |
|---|---|---|---|
| | | | |

## 12. Definition of Done

- [ ] Core business loop works end-to-end
- [ ] Public contracts are defined
- [ ] Tests pass
- [ ] Relevant evals pass
- [ ] Permission boundaries are enforced
- [ ] Failure behavior is bounded
- [ ] Observability is sufficient
- [ ] Deployment / rollback path is known
