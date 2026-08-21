# Production Reference Architecture：生产级 Agent 参考架构

> 目标：给整套知识库提供一张统一的生产架构蓝图。不是要求所有项目完全照搬，而是用于设计评审时检查是否遗漏关键能力。

## 1. 总体架构

```text
                              User / Client
                                   │
                              AG-UI / API
                                   │
                              API Gateway
                                   │
                    AuthN / AuthZ / Tenant / Policy
                                   │
                              Task Service
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
                 Sync Path                     Queue
                    │                             │
                    └──────────────┬──────────────┘
                                   ↓
                            Agent Runtime Fleet
                     ┌─────────────┼─────────────┐
                     │             │             │
                 Context       Planner        Executor
                 Builder          │             │
                     │            ↓             ↓
                     │      Workflow / DAG   Tool Gateway
                     │                          │
                     │                ┌─────────┼─────────┐
                     │                ↓         ↓         ↓
                     │               MCP       API      Sandbox
                     │
                     ├──────── Model Gateway
                     ├──────── RAG / Retrieval
                     ├──────── Memory
                     ├──────── Checkpoint Store
                     ├──────── Artifact / Evidence Store
                     └──────── Agent Identity / Credential Broker
                                   │
                                   ↓
                         Evaluator / Policy / HITL
                                   │
                                   ↓
                              Final Artifact
```

外围能力：

```text
Tracing / Metrics / Logging
Eval / Regression / Simulation
Security / Audit / Governance
Cost / Budget / Quota
CI/CD / Canary / Rollback
SRE / Incident / Runbook
```

## 2. Control Plane

```text
Agent Registry
Tool Registry
Skill Registry
Prompt Registry
Model Catalog
Policy
Identity
Release
Eval Results
Fleet Health
```

Control Plane 不直接负责每次 Tool Call，而是决定“什么版本和策略应该被执行”。

## 3. Data Plane

真正执行：

```text
Task → Runtime → Model / Tool / RAG / Agent → Artifact
```

原则：

- Worker 可水平扩展；
- 状态外置；
- Task 可恢复；
- Tool 权限最小化；
- 所有执行可 Trace。

## 4. 核心数据对象

建议整个平台围绕以下对象统一：

```text
AgentDefinition
Task
Plan
RuntimeEvent
ToolCall
Evidence
Artifact
Approval
Checkpoint
EvalResult
Trace
```

这些对象应在 `schemas/` 中维护正式契约。

## 5. Identity Flow

```text
User Identity
      ↓
Agent Identity
      ↓ Policy / Delegation
Credential Broker
      ↓
Tool / Resource
```

模型永远不应该直接看到长期 Credential。

## 6. Communication Boundaries

```text
Frontend ↔ Agent     AG-UI / event model
Agent ↔ Tool         MCP / internal Tool contract
Agent ↔ Agent        A2A / internal artifact contract
```

协议选择取决于系统边界，不要为了使用协议而使用协议。

## 7. Artifact Flow

```text
Research → EvidenceSet
Data     → DataSnapshot
RAG      → KnowledgeEvidence
              ↓
          Risk Agent
              ↓
       RiskAssessment
              ↓
          Reviewer
              ↓
         ReviewResult
              ↓
            HITL
              ↓
         FinalReport
```

Agent 之间优先传 Artifact Reference，而不是完整聊天历史。

## 8. Runtime Budget

平台应强制：

```text
max_duration
max_turns
max_model_calls
max_tool_calls
max_handoffs
max_parallel_workers
max_tokens
max_cost
```

Budget 是 Runtime Policy，不是 Prompt 建议。

## 9. Deployment

```text
Load Balancer
├─ API Replica
├─ Task Service Replica
└─ Event Stream Service

Queue
├─ High Priority
├─ Normal
└─ Long Research

Worker Pools
├─ General Agent Worker
├─ Browser Worker
├─ Sandbox / Coding Worker
└─ Realtime Worker
```

不同 Worker Pool 可以有完全不同的安全和资源配置。

## 10. Storage

```text
PostgreSQL
  Task / Agent Definition / Approval / Metadata

Redis
  Cache / Rate Limit / Ephemeral Coordination

Object Storage
  Artifact / Large Evidence / Files

Vector DB / pgvector
  Knowledge Retrieval

Observability Backend
  Trace / Metrics / Logs
```

不要把所有数据都塞进一个 State JSON。

## 11. Security Zones

建议把能力按风险隔离：

```text
Zone 1: Public Read
Zone 2: Internal Read
Zone 3: Internal Write
Zone 4: Destructive / High Impact
Zone 5: Sandbox / Untrusted Code
```

跨 Zone 需要更严格 Policy / Approval。

## 12. Evaluation Pipeline

```text
Change
 ↓
Unit / Schema
 ↓
Component Eval
 ↓
Scenario / Simulation
 ↓
Security Eval
 ↓
Staging
 ↓
Canary
 ↓
Online Eval
```

没有 Eval Gate 的 Agent Release 不应自动进入生产。

## 13. Reliability

平台应提供：

```text
Circuit Breaker
Fallback
Degraded Mode
Admission Control
Backpressure
Checkpoint
Replay
DLQ
Runbook
Postmortem
```

## 14. 最小版本与完整版本

### MVP

```text
API
Agent Runtime
Tool
RAG
PostgreSQL
Trace
Basic Eval
```

### Production

再逐步增加：

```text
Queue
Checkpoint
Identity
Policy
HITL
Artifact Store
Model Gateway
Simulation Eval
SRE
Control Plane
```

不要在业务还没验证前一次性建设全部平台能力。

## 15. 架构评审问题

设计任何大型 Agent 项目时必须回答：

1. 谁控制下一步执行？
2. State 保存在哪里？
3. Context 如何构建和压缩？
4. Agent / Tool 身份是什么？
5. Credential 在哪里获取？
6. 高风险 Action 谁批准？
7. Task 如何取消、恢复和重放？
8. Agent 间传什么数据契约？
9. Tool / Model 故障如何降级？
10. 如何 Eval Output 与 Trajectory？
11. 如何限制 Token、Step 和 Cost？
12. 如何追踪到 Agent / Prompt / Model / Tool Version？
13. 如何部署和扩缩容？
14. 出事故如何止损、回滚和复盘？

能完整回答这些问题，才接近生产级 Agent 架构。