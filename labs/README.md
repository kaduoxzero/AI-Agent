# Hands-on Labs：Agent 全能工程师实训体系

> 这里不是概念复习，而是把知识库中的每一层能力转化为可验收的工程任务。

## 1. 实训原则

每个 Lab 都应包含四部分：

```text
Concept Lab      最小理解实验
Engineering Lab  工程实现
Failure Lab      故障 / 边界实验
Acceptance       验收标准
```

不要只写一个 Happy Path Demo。

## 2. Lab 目录规划

```text
labs/
├─ L01-model-gateway/
├─ L02-structured-agent/
├─ L03-tool-runtime/
├─ L04-mcp-server/
├─ L05-rag-pipeline/
├─ L06-agentic-rag/
├─ L07-agent-memory/
├─ L08-react-planner/
├─ L09-langgraph-runtime/
├─ L10-multi-agent/
├─ L11-agent-identity/
├─ L12-ag-ui-console/
├─ L13-sandbox-coding-agent/
├─ L14-eval-harness/
├─ L15-security-redteam/
├─ L16-event-driven-agent/
├─ L17-agent-sre/
└─ L18-agent-platform/
```

## 3. L01｜Model Gateway

### 任务

实现统一模型调用层：

```text
Agent → ModelGateway → Provider A / Provider B
```

### 必须完成

- Provider Adapter；
- task_type 路由；
- fallback；
- Token / Cost 统计；
- Trace ID；
- Tenant quota。

### Failure Lab

- Provider A 429；
- Provider A timeout；
- Provider B 不支持 Tool Calling。

### 验收

- [ ] 业务代码没有直接依赖 Provider SDK；
- [ ] Fallback 不会把 Tool Task 路由到不支持 Tool 的模型；
- [ ] 每次 Call 可追踪成本。

## 4. L02｜Structured Agent

实现：

```text
Prompt
+ Structured Output
+ State
+ Session
```

要求 Router 返回 Typed Decision，不允许自由文本路由。

Failure Lab：模型返回非法 JSON、字段缺失、Enum 越界。

## 5. L03｜Tool Runtime

实现 Tool Registry + Executor。

Tool 分级：

```text
READ_ONLY
WRITE
DESTRUCTIVE
```

要求：

- Schema；
- timeout；
- retry；
- idempotency；
- approval hook；
- audit event。

## 6. L04｜MCP Server

实现一个业务 MCP Server，至少提供：

```text
2 Tools
1 Resource
Authorization
Health / Error handling
```

测试恶意参数、权限不足、Server timeout。

## 7. L05｜Enterprise RAG

构建：

```text
Parse → Chunk → Metadata → Embedding → Hybrid Retrieval → Rerank → Citation
```

必须加入：

- tenant_id；
- ACL filter；
- document version；
- citation validation。

## 8. L06｜Agentic RAG

Agent 自主决定：

```text
是否检索
query rewrite
是否二次检索
何时停止
```

必须限制 retrieval budget。

## 9. L07｜Memory

实现：

- short-term；
- long-term；
- memory write policy；
- TTL；
- conflict handling。

安全实验：恶意网页内容不能自动进入长期 Memory。

## 10. L08｜ReAct / Planner

比较：

```text
Single Agent Baseline
ReAct
Plan & Execute
```

Eval：Quality / Steps / Cost / Latency。

目标不是证明复杂模式一定更好，而是学会用数据选型。

## 11. L09｜LangGraph Runtime

实现：

```text
State
Node
Conditional Edge
Send
Checkpoint
interrupt / resume
```

故障实验：Worker crash 后从 Checkpoint 恢复。

## 12. L10｜Multi-Agent

实现：

```text
Supervisor
├─ Research
├─ Data
└─ Reviewer
```

Agent 间只交换 Typed Artifact。

必须限制：

```text
max_handoffs
max_workers
max_steps
```

## 13. L11｜Agent Identity

实现简化 Credential Broker：

```text
User + Agent + Tool + Resource
 ↓ Policy
Short-lived scoped credential
```

验证 Agent B 不能继承 Agent A 未被委派的权限。

## 14. L12｜AG-UI Console

实现前端：

```text
Task Timeline
Tool Calls
State Delta
Approval Card
Artifact Panel
Cancel / Resume
```

刷新页面后必须恢复状态。

## 15. L13｜Sandbox Coding Agent

实现隔离 Workspace：

```text
clone repo
read/search
patch
shell
test
diff
```

限制：CPU、Memory、Network、Execution Time。

## 16. L14｜Eval Harness

建立 Scenario Runner：

```text
Scenario YAML
 ↓
Fake Environment
 ↓
Agent
 ↓
Trajectory Assertions
```

至少 20 个回归 Scenario。

## 17. L15｜Security Red Team

覆盖：

- direct prompt injection；
- indirect injection；
- tool result poisoning；
- memory poisoning；
- excessive agency；
- tenant leakage；
- unsafe handoff。

Critical Case 必须全部阻止。

## 18. L16｜Event-Driven Agent

实现：

```text
Webhook / Cron → Event Gateway → Task Queue → Agent
```

必须有 dedup、idempotency、DLQ、replay。

## 19. L17｜Agent SRE

完成：

- SLI / SLO；
- Dashboard；
- Circuit Breaker；
- Degraded Mode；
- 5 次 Failure Drill；
- 1 份 Postmortem。

## 20. L18｜Agent Platform

将所有内容组合：

```text
Agent Registry
Tool Registry
Prompt Version
Policy
Model Gateway
Runtime
Eval Gate
Release
```

支持两个 Agent Version 并行运行和 Canary。

## 21. 最终实训规则

完成一个 Lab 不以“代码跑通”为验收，而要同时回答：

```text
失败怎么办？
如何恢复？
如何测试？
如何 Trace？
权限在哪里判断？
成本怎么限制？
如何版本化？
生产如何扩展？
```

如果回答不了，就还没有完成这个 Lab。