# Hands-on Labs：Agent 全能工程师实训体系

> 这里不是概念复习，而是把知识库中的能力转化成可运行、可测试、可验收的工程任务。

## 1. 当前进度

第一批核心实验已经真正实现，不再只是规划：

| Lab | 状态 | 核心能力 | 路径 |
|---|---|---|---|
| 01 Structured Output | ✅ 可运行 | Schema、Validation、Fail Closed | `01-structured-output/` |
| 02 Tool Runtime | ✅ 可运行 | Scope、Timeout、Idempotency、Audit | `02-tool-runtime/` |
| 03 MCP Server | ✅ 可运行 + Test | MCP Python SDK v2、Tool、Resource、Client Test | `03-mcp-server/` |
| 04 Enterprise RAG | ✅ 可运行 | Tenant ACL、Metadata、Retrieval、Rerank、Citation | `04-enterprise-rag/` |
| 05 Agent Loop | ✅ 可运行 | Action、Observation、Budget、Trajectory | `05-agent-loop/` |
| 06 LangGraph HITL | ✅ 可运行 | StateGraph、Checkpoint、interrupt/resume | `06-langgraph-hitl/` |
| 07 Agent Eval | ✅ 可运行 + Gate | Golden Dataset、Trajectory、Forbidden Tool、CI Exit Code | `07-agent-eval/` |

仓库根目录 `.github/workflows/labs.yml` 会自动执行这些实验和 Reference Starter 测试。

## 2. 实训原则

每个 Lab 最终都应包含：

```text
Concept
  ↓
Runnable Baseline
  ↓
Engineering Constraints
  ↓
Failure / Security Case
  ↓
Eval
  ↓
Acceptance Criteria
```

“代码能跑”只代表完成了第一步。

一个生产级实验还必须回答：

```text
失败怎么办？
权限在哪里判断？
如何 Retry / Resume？
如何 Trace？
如何限制预算？
如何测试 Trajectory？
如何部署和扩缩容？
```

## 3. 第一阶段推荐顺序

### Lab 01｜Structured Output

学习 Typed Output 和边界校验。

重点：

- Pydantic Schema；
- Enum / Range；
- Extra Field Reject；
- Fail Closed。

### Lab 02｜Tool Runtime

学习模型和业务执行层的边界。

重点：

- Tool Registry；
- read / write；
- scope；
- timeout；
- idempotency；
- audit。

### Lab 03｜MCP Server

把 Tool 能力升级成标准协议服务。

重点：

- `MCPServer`；
- Tool；
- Resource；
- MCP Client；
- In-memory integration test。

### Lab 04｜Enterprise RAG

重点不是 Vector DB API，而是：

```text
Identity
 ↓
ACL Filter
 ↓
Retrieval
 ↓
Rerank
 ↓
Evidence
 ↓
Citation
```

### Lab 05｜Agent Loop

不依赖框架实现：

```text
Model
 ↓ Action
Tool
 ↓ Observation
State
 ↓
Next Turn
```

并由 Runtime 强制 Budget。

### Lab 06｜LangGraph HITL

将人工审批做成可暂停恢复的工作流：

```text
Graph
 ↓
interrupt
 ↓
Checkpoint
 ↓
Human
 ↓
Command(resume=...)
```

### Lab 07｜Agent Eval

把质量要求变成机器可执行 Gate：

```text
Golden Dataset
 ↓
Agent
 ↓
Output Assertions
+ Trajectory Assertions
+ Security Assertions
 ↓
PASS / FAIL
```

## 4. 第二阶段：下一批要实现的实验

下面这些已经在知识库中有理论与架构章节，后续需要继续代码化。

### Lab 08｜Model Gateway

实现：

```text
Agent → Model Gateway → Provider A / Provider B / Local Model
```

必须覆盖：

- Capability Routing；
- Fallback；
- Retry；
- Quota；
- Token / Cost；
- Provider 429 / Timeout。

### Lab 09｜Agentic RAG

实现：

- Query Rewrite；
- 是否检索；
- 二次检索；
- Retrieval Budget；
- Evidence Sufficiency。

### Lab 10｜Memory Engineering

实现：

- short-term；
- long-term；
- write policy；
- TTL；
- conflict；
- memory poisoning protection。

### Lab 11｜Multi-Agent + Typed Artifact

实现：

```text
Supervisor
├─ Research
├─ Data
└─ Reviewer
```

Agent 之间只能通过 Typed Artifact / Evidence 协作。

必须有：

```text
max_handoffs
max_workers
max_steps
```

### Lab 12｜Agent Identity / Credential Broker

实现：

```text
User
 ↓ delegation
Agent Identity
 ↓ policy
Short-lived Credential
 ↓
Tool / Resource
```

验证 Agent B 无法继承 Agent A 未委派权限。

### Lab 13｜AG-UI Console

前端展示：

- Task Timeline；
- Tool Call；
- State Delta；
- Approval Card；
- Artifact；
- Cancel / Resume。

### Lab 14｜Sandbox Coding Agent

实现：

```text
Workspace
├─ read/search
├─ patch
├─ shell
├─ tests
└─ git diff
```

并限制 CPU、Memory、Network、Duration。

### Lab 15｜Security Red Team

至少覆盖：

- Direct Prompt Injection；
- Indirect Injection；
- Tool Result Poisoning；
- Memory Poisoning；
- Excessive Agency；
- Tenant Leakage；
- Unsafe Handoff。

Critical Security Cases 必须 100% 通过。

### Lab 16｜Event-Driven Agent

实现：

```text
Webhook / Cron
 ↓
Event Gateway
 ↓
Queue
 ↓
Agent Worker
```

必须支持 dedup、idempotency、DLQ、replay。

### Lab 17｜Agent SRE

完成：

- SLI / SLO；
- Circuit Breaker；
- Degraded Mode；
- Failure Drill；
- Runbook；
- Postmortem。

### Lab 18｜Agent Platform

最终组合：

```text
Agent Registry
Tool Registry
Prompt / Skill Version
Model Gateway
Policy / Identity
Runtime Fleet
Eval Gate
Canary / Rollback
```

## 5. Reference Platform

完成 Lab 01~07 后，进入：

`../reference-architecture/starter/`

Starter 已提供：

- FastAPI Task API；
- Typed Task Contract；
- Task State Machine 基础；
- Dockerfile；
- PostgreSQL；
- Redis；
- API Tests。

建议不要另起一个全新 Demo，而是持续升级这个 Starter，把各 Lab 的能力逐步接进去。

## 6. 最终验收标准

真正完成整套 Labs 后，应能够从空仓库独立实现：

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
Eval / Trace / SRE
 ↓
Deployment / Canary / Rollback
```

并能解释每一层为什么存在、失败后如何恢复、如何测试，以及哪些能力不应该交给 LLM 决定。
