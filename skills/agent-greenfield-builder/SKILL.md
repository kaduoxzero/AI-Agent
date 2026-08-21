---
name: agent-greenfield-builder
description: Build a new Agent system from zero to a working, testable engineering baseline. Use for greenfield Agent, RAG Agent, workflow Agent, assistant, research Agent, coding Agent, or business Agent projects where requirements must be translated into architecture, contracts, implementation phases, tests, evaluation, security, and deployment boundaries.
---

# Agent Greenfield Builder

## Objective

从 0 到 1 构建一个 **可运行、可测试、可评估、可扩展** 的 Agent 工程，而不是只生成 Prompt 或 Demo。

## Core Principle

先确定业务闭环，再确定是否真的需要 Agent。

复杂度顺序：

```text
Deterministic Code
→ Workflow
→ LLM Workflow
→ Single Agent
→ Agent + Tool / RAG / Memory
→ Multi-Agent
```

## Phase 0 — Requirement Compression

把需求压缩成：

```text
Actor:
Goal:
Input:
Output:
Knowledge:
Tools:
Actions:
Risk Level:
Latency Target:
Cost Constraint:
Human Approval:
Deployment Target:
```

不要从“选 LangGraph 还是 CrewAI”开始设计。

## Phase 1 — Define Business Loop

先画业务闭环：

```text
User / Event
  ↓
Task Create
  ↓
Context Build
  ↓
Decision / Plan
  ↓
Tool / Retrieval / Action
  ↓
Evaluation
  ↓
Artifact
  ↓
Persist / Notify / Human Review
```

必须明确：

- 谁启动任务；
- 谁决定下一步；
- 谁可以执行外部操作；
- 任务何时结束；
- 失败后如何恢复。

## Phase 2 — Choose Architecture

### Workflow

当步骤固定、条件清晰、要求高稳定时使用。

### Single Agent

当需要动态选择 Tool、检索路径或下一步时使用。

### Multi-Agent

只有出现以下至少一个明确边界才拆分：

- 不同角色需要不同权限；
- 不同角色需要隔离 Context；
- 子任务可以并行；
- 专业能力差异明显；
- 需要独立评审或对抗；
- 一个 Agent 的 Prompt / Tool 集已经不可维护。

## Phase 3 — Define Contracts First

至少定义：

- TaskRequest
- TaskRecord
- TaskStatus
- AgentState
- ToolInput / ToolOutput
- Evidence
- Artifact
- Event
- ErrorCategory

禁止让多个模块通过自由文本长期耦合。

## Phase 4 — Context Design

Context 应拆成：

```text
System Policy
Task Goal
Current State
Relevant Memory
Retrieved Evidence
Tool Results
Recent Messages
Budget
```

必须有长度上限和裁剪策略。

## Phase 5 — Tool Design

每个 Tool 必须定义：

- name；
- purpose；
- typed input；
- typed output；
- timeout；
- retry policy；
- permission scope；
- idempotency；
- side effect；
- audit fields。

高风险 Tool 默认进入 HITL。

## Phase 6 — RAG Decision

如果业务依赖外部或企业知识，定义：

```text
Ingestion
→ Chunk
→ Metadata
→ Embedding
→ Index
→ Retrieve
→ Filter
→ Rerank
→ Evidence
→ Generate
```

必须保留 source_id / citation / tenant scope。

## Phase 7 — State & Memory

区分：

- State：当前任务运行状态；
- Session：一次交互会话；
- Memory：跨任务长期信息；
- Checkpoint：恢复执行所需快照。

不要把完整聊天记录直接当长期 Memory。

## Phase 8 — Runtime Boundaries

长任务不要绑定同步 HTTP 生命周期。

推荐：

```text
API
→ Task Store
→ Queue
→ Worker
→ Agent Runtime
→ Checkpoint
→ Event Stream
→ Artifact Store
```

## Phase 9 — Safety

至少实现：

- Tool Allowlist；
- Tenant / User Identity；
- Scope Permission；
- Prompt Injection Boundary；
- Sensitive Action HITL；
- Step / Tool / Model / Cost Budget；
- Cancellation；
- Audit Event。

## Phase 10 — Evaluation Before Release

建立最小 Golden Set，至少覆盖：

- 正常任务；
- 无知识命中；
- Tool 失败；
- Tool 参数错误；
- Prompt Injection；
- 超预算；
- 长任务恢复；
- 用户取消；
- 高风险审批；
- 多租户隔离。

指标至少包括：

```text
Task Success
Groundedness
Tool Success
Trajectory Correctness
Latency
Token
Cost
Safety Violations
```

## Phase 11 — Implementation Order

推荐严格按顺序：

```text
M1 Typed Contracts
M2 Minimal Workflow / Agent Loop
M3 Tool Runtime
M4 RAG（如需要）
M5 Persistent Task State
M6 Queue + Worker
M7 Checkpoint / Resume
M8 HITL
M9 Event / Streaming
M10 Eval
M11 Observability
M12 Production Deployment
```

## Non-Negotiable Rules

- 不先搭十几个 Agent 再找业务用途；
- 不把数据库 CRUD 包一层 LLM 就称为 Agent；
- 不让 LLM 决定确定性权限规则；
- 不允许无限循环；
- 不允许 Tool 无 Schema；
- 不允许生产任务只存在内存；
- 不允许没有 Eval 就宣称“生产可用”。

## Required Outputs

完成后应具备：

- 清晰目录结构；
- 可运行入口；
- Typed Contract；
- 至少一个完整任务闭环；
- 单元 / 集成测试；
- Eval Dataset；
- 环境配置示例；
- README 运行方式；
- 已知限制与下一阶段 Roadmap。

## Completion Criteria

只有同时满足以下条件才算完成：

1. 新环境能启动；
2. 核心任务可端到端执行；
3. Tool / RAG / State 行为可测试；
4. 错误不会静默吞掉；
5. 有边界和预算；
6. 有至少一组回归测试；
7. 输出可追溯；
8. 下一步扩展不需要推翻核心契约。
