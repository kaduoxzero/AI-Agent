# Hands-on Labs：Agent 全能工程师实训体系

> 18 个 Lab 已全部建立实际实现。目标不是“运行一个 Demo”，而是沿着 Contract → Runtime → RAG → Multi-Agent → Security → SRE → Platform 的路径形成生产工程能力。

## 1. 实训原则

每个 Lab 都遵循：

```text
Concept
  ↓
Runnable Baseline
  ↓
Engineering Constraint
  ↓
Failure / Security Case
  ↓
Eval / Test
  ↓
Acceptance Criteria
```

判断一个 Lab 是否真正学会，不只看代码能不能运行，还要回答：

```text
失败怎么办？
权限在哪里判断？
状态保存在哪里？
如何 Retry / Resume？
如何 Trace？
如何限制 Step / Token / Cost？
如何做回归测试？
如何上线和扩缩容？
```

## 2. 18 个 Lab 总览

| # | Lab | 状态 | 核心能力 |
|---:|---|---|---|
| 01 | [Structured Output](01-structured-output/) | ✅ | Schema、Validation、Fail Closed |
| 02 | [Tool Runtime](02-tool-runtime/) | ✅ | Scope、Timeout、Idempotency、Audit |
| 03 | [MCP Server](03-mcp-server/) | ✅ + Test | MCP v2、Tool、Resource、In-memory Client |
| 04 | [Enterprise RAG](04-enterprise-rag/) | ✅ | Tenant ACL、Retrieval、Rerank、Citation |
| 05 | [Agent Loop](05-agent-loop/) | ✅ | Action、Observation、Budget、Trajectory |
| 06 | [LangGraph HITL](06-langgraph-hitl/) | ✅ | Checkpoint、interrupt、resume |
| 07 | [Agent Eval](07-agent-eval/) | ✅ + Gate | Golden Dataset、Trajectory、Forbidden Tool |
| 08 | [Model Gateway](08-model-gateway/) | ✅ | Capability Routing、Fallback、Quota、Cost |
| 09 | [Agentic RAG](09-agentic-rag/) | ✅ | Query Rewrite、Evidence Sufficiency、Retrieval Budget |
| 10 | [Memory Engineering](10-memory-engineering/) | ✅ | Write Policy、TTL、Version、Poisoning Protection |
| 11 | [Multi-Agent + Artifact](11-multi-agent-artifacts/) | ✅ | Supervisor、Parallel Worker、Typed Artifact |
| 12 | [Agent Identity](12-agent-identity/) | ✅ | Delegation、Scoped Credential、OBO 思维 |
| 13 | [AG-UI Console](13-ag-ui-console/) | ✅ + Test | Run/Tool/State/Text Event、UI State |
| 14 | [Sandbox Coding Agent](14-sandbox-coding-agent/) | ✅ | Workspace、Path Boundary、Command Policy |
| 15 | [Security Red Team](15-security-redteam/) | ✅ + Gate | Injection、Tenant、Memory、Agency、Handoff |
| 16 | [Event-Driven Agent](16-event-driven-agent/) | ✅ | Dedup、Retry、DLQ、Replay、Idempotency |
| 17 | [Agent SRE](17-agent-sre/) | ✅ | Circuit Breaker、Degraded Mode、SLI/SLO |
| 18 | [Agent Platform](18-agent-platform/) | ✅ | Registry、Version、Canary、Rollback |

GitHub Actions：

```text
.github/workflows/labs.yml
```

负责自动运行全部 18 个 Lab 的脚本/测试，以及 Reference Starter API Test。

## 3. 推荐学习阶段

### Stage A｜Agent 基础执行契约

按顺序完成：

```text
01 Structured Output
 ↓
02 Tool Runtime
 ↓
03 MCP Server
```

完成后应理解：

> Model 负责决策，代码负责契约、权限和真正执行。

### Stage B｜Knowledge + Runtime

```text
04 Enterprise RAG
 ↓
05 Agent Loop
 ↓
06 LangGraph HITL
 ↓
07 Agent Eval
```

完成后应能从零解释：

```text
State
Action
Observation
Checkpoint
HITL
Trajectory
Eval Gate
```

### Stage C｜大型 Agent 核心能力

```text
08 Model Gateway
 ↓
09 Agentic RAG
 ↓
10 Memory Engineering
 ↓
11 Multi-Agent Artifact
 ↓
12 Agent Identity
```

这一阶段结束后，不应再把大型 Agent 项目理解为“Prompt + Tool 列表”。

### Stage D｜产品、安全与运行环境

```text
13 AG-UI
 ↓
14 Sandbox
 ↓
15 Security Red Team
 ↓
16 Event-Driven Agent
```

重点从“Agent 会不会做”转向：

```text
用户能不能看懂执行过程？
不可信代码在哪里运行？
Agent 会不会越权？
没有聊天请求时系统怎么自动工作？
```

### Stage E｜Production / Platform

```text
17 Agent SRE
 ↓
18 Agent Platform
 ↓
Reference Architecture Starter
```

最终学习：

```text
Reliability
Control Plane
Release
Canary
Rollback
Platform Governance
```

## 4. 每个 Lab 的工程要求

### 01 Structured Output

必须掌握：

- Typed Schema；
- Local Validation；
- Unknown Field Reject；
- Enum / Range；
- Fail Closed。

### 02 Tool Runtime

必须掌握：

- Tool Registry；
- Read / Write；
- Scope；
- Timeout；
- Idempotency；
- Audit Event。

### 03 MCP

必须掌握：

- Server；
- Tool；
- Resource；
- Client；
- Integration Test；
- Production Auth 边界。

### 04 Enterprise RAG

必须掌握：

```text
Identity → ACL → Retrieval → Rerank → Evidence → Citation
```

### 05 Agent Loop

必须能够自己实现：

```text
Model → Action → Tool → Observation → State → Next Turn
```

并由 Runtime 强制 Budget。

### 06 LangGraph HITL

必须理解：

```text
thread_id
checkpoint
interrupt
resume
```

### 07 Eval

至少同时评：

- Output；
- Required Tool；
- Forbidden Tool；
- Steps；
- Security Case。

### 08 Model Gateway

业务代码不得直接依赖单一 Provider。

必须覆盖：

- capability；
- fallback；
- quota；
- usage；
- cost。

### 09 Agentic RAG

Agent 可以决定下一轮 Query，但 Runtime 决定最大 Retrieval Budget。

### 10 Memory

外部不可信数据不得自动进入长期 Memory。

### 11 Multi-Agent

Agent 之间优先交换：

```text
EvidenceSet
DataSnapshot
ReviewResult
```

而不是共享完整 Conversation。

### 12 Identity

理解：

```text
User → Delegation → Agent → Scoped Credential → Tool
```

### 13 AG-UI

理解：

```text
RUN
TOOL
STATE
TEXT
```

四类核心前端事件，并区分 Protocol 与 Transport。

### 14 Sandbox

必须明确：

> 应用层 Path / Command Policy 不等于强 OS Sandbox。

### 15 Security

Critical Security Cases 失败时必须阻断 CI / Release。

### 16 Event-Driven

必须支持：

```text
Dedup
Idempotency
Retry
DLQ
Replay
```

### 17 SRE

依赖失败不能导致 Agent 无限重试和雪崩。

必须有：

```text
Circuit Breaker
Fallback
Degraded Mode
SLI
SLO
```

### 18 Platform

必须理解：

```text
Control Plane
  Registry / Release / Policy

Data Plane
  Runtime / Worker / Tool / Model
```

## 5. Reference Platform

完成 Lab 01~18 后进入：

[Reference Agent Platform Starter](../reference-architecture/starter/)

Starter 当前提供：

- FastAPI Task API；
- Typed Task Contract；
- Task Status；
- In-Memory Repository Adapter；
- Dockerfile；
- PostgreSQL；
- Redis；
- API Tests。

继续按以下路线演进：

```text
In-Memory API
 ↓
PostgreSQL Repository
 ↓
Redis / MQ Worker
 ↓
Agent Runtime
 ↓
Checkpoint / Resume
 ↓
Model Gateway / MCP / RAG / Memory
 ↓
AG-UI / HITL
 ↓
Eval / Security / Trace
 ↓
SRE / Canary / Platform Control Plane
```

## 6. 最终毕业标准

完成全部实验后，应能从空仓库独立设计：

```text
Frontend / AG-UI
 ↓
Task API
 ↓
Queue
 ↓
Agent Runtime / LangGraph
 ↓
Model Gateway
 ↓
Tool Gateway / MCP
 ↓
RAG / Memory
 ↓
Multi-Agent / A2A
 ↓
Artifact / Evidence
 ↓
Policy / Identity / HITL
 ↓
Eval / Trace / Security / SRE
 ↓
Deployment / Canary / Rollback / Control Plane
```

并能够解释：每一层为什么存在、状态放在哪里、失败怎么恢复、权限由谁判断、成本如何限制，以及哪些事情绝不能交给 LLM 自己决定。
