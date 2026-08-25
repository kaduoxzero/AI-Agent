---
name: agent-greenfield-builder
version: 1.1.0
description: Build a new Agent system from zero to a working, testable engineering baseline. Use after requirements and key boundaries are resolved directly or through agent-guided-builder. Covers architecture, contracts, implementation phases, tests, evaluation, security, observability, runtime, and deployment boundaries.
---

# Agent Greenfield Builder

## Objective

从 0 到 1 构建一个 **可运行、可测试、可评估、可扩展、可恢复、可治理** 的 Agent 工程，而不是只生成 Prompt 或 Demo。

本 Skill 默认承接 `agent-guided-builder` 的设计结果。用户尚未明确关键边界时，应先进入 Guided Workshop；用户明确要求“直接做”时，Agent 可以采用推荐默认值，但仍必须内部完成 Boundary Canvas 和 Decision Ledger。

## Stage -1 — Guided Boundary Gate

开始编码前先判断以下项目是否已经明确：

```text
Problem Statement
Goal / Out-of-Scope
Architecture Level
Autonomy Contract
Knowledge Boundary
Tool / Side-Effect Boundary
State / Memory / Checkpoint
Multi-Agent Decision
Identity / Permission
HITL Rules
Runtime Budget
Eval / Acceptance
Deployment Target
```

处理方式：

```text
已明确 → 直接使用
可从上下文推断 → 记录推断
适合安全默认值 → 采用默认值
关键且未决 → agent-guided-builder 引导用户选择
用户授权直接做 → 采用推荐项并记录 Decision Ledger
```

不要为了“问完整”而重复询问已经知道的信息。

## Core Principle

先确定业务闭环，再确定是否真的需要 Agent。

复杂度顺序（统一复杂度阶梯）：

```text
Deterministic Code
→ State Machine
→ Deterministic Workflow
→ LLM Workflow
→ Single Agent
→ Agent + Tools / RAG / Memory
→ Multi-Agent
```

每升级一级，都必须能说明上一层为什么不足。

## Phase 0 — Requirement Compression

把需求压缩成：

```text
Actor:
Goal:
Out-of-Scope:
Trigger:
Input:
Output Artifact:
Knowledge:
Tools:
Actions:
Autonomy Level:
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
- 哪些步骤必须确定性执行；
- 谁可以执行外部操作；
- 任务何时结束；
- 失败后如何恢复；
- 哪些动作需要人确认。

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
- 一个 Agent 的 Prompt / Tool 集已经不可维护；
- 不同角色需要不同模型或独立生命周期。

必须能回答：

> 如果把两个 Agent 合并，具体会在哪个权限、Context、Tool、状态或职责边界上产生冲突？

回答不出来时默认不拆。

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

对于 Multi-Agent，还要定义：

- Handoff Contract
- Worker Result
- Review Result
- Shared State Ownership
- Failure Propagation

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

必须有：

- 长度上限；
- 选择策略；
- 不可信内容边界；
- 压缩 / Compaction；
- Evidence 与指令分离。

不要把所有历史、RAG 结果和 Tool 输出无差别塞入上下文。

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
- audit fields；
- HITL requirement。

Tool 按风险分类：

```text
Read-only
Write
Destructive
External Communication
Sensitive / High-impact
```

高风险 Tool 默认进入 HITL，不允许依赖 Prompt 自我约束。

## Phase 6 — RAG Decision

如果业务依赖外部或企业知识，定义：

```text
Ingestion
→ Parse / Clean
→ Chunk
→ Metadata
→ Embedding / Index
→ Retrieve
→ Permission Filter
→ Rerank
→ Evidence
→ Generate
→ Citation
```

必须保留：

- source_id；
- citation；
- tenant scope；
- source timestamp；
- trust level；
- retrieval trace。

## Phase 7 — State & Memory

区分：

- State：当前任务运行状态；
- Session：一次交互会话；
- Memory：跨任务长期信息；
- Checkpoint：恢复执行所需快照。

Memory 还必须定义：

```text
Write Policy
Trust Source
TTL
Conflict Handling
Deletion
Tenant / User Scope
```

不要把完整聊天记录直接当长期 Memory。

## Phase 8 — Runtime Boundaries

短同步任务和长任务使用不同运行模型。

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

必须定义：

```text
Max Steps
Max Model Calls
Max Tool Calls
Max Retry
Wall-clock Timeout
Token Budget
Cost Budget
Cancellation
Resume
```

## Phase 9 — Safety

至少实现：

- Tool Allowlist；
- Tenant / User Identity；
- Agent / Tool Scope Permission；
- Prompt Injection Boundary；
- Sensitive Action HITL；
- Step / Tool / Model / Token / Cost Budget；
- Cancellation；
- Audit Event；
- Secret isolation；
- Fail Closed policy。

主动考虑：

- Direct / Indirect Prompt Injection；
- Tool Poisoning；
- Memory Poisoning；
- Cross-Tenant Data Leak；
- Excessive Agency；
- Credential Leakage。

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

同时定义发布 Gate，而不是只记录分数。

## Phase 11 — Observability

至少能够回答：

```text
哪个 Task？
哪个 Agent Version？
哪个 Prompt Version？
哪个 Model Route？
调用了什么 Tool？
用了哪些 Evidence？
为什么进入 HITL？
花了多少 Token / Cost？
在哪里失败？
是否从 Checkpoint 恢复？
```

建议统一：

- Task ID
- Trace ID
- Agent Version
- Event
- Tool Call
- Retrieval
- Model Usage
- Approval
- Artifact
- Error Category

## Phase 12 — Implementation Order

推荐严格按顺序：

```text
M1 Typed Contracts
M2 Minimal Happy Path
M3 Tool Runtime
M4 RAG（如需要）
M5 Persistent Task State
M6 Queue + Worker
M7 Checkpoint / Resume
M8 HITL / Security
M9 Event / Streaming
M10 Eval
M11 Observability
M12 Production Deployment
```

每个 Milestone 都必须有独立验收，禁止一次性把全部模块写完再统一调试。

## Non-Negotiable Rules

- 不先搭十几个 Agent 再找业务用途；
- 不把数据库 CRUD 包一层 LLM 就称为 Agent；
- 不让 LLM 决定确定性权限规则；
- 不允许无限循环；
- 不允许 Tool 无 Schema；
- 不允许生产任务只存在内存；
- 不允许高风险 Side Effect 没有审批或恢复策略；
- 不允许没有 Eval 就宣称“生产可用”；
- 不允许没有明确职责边界就拆 Multi-Agent。

## Required Outputs

完成后应具备：

- Agent Boundary Canvas；
- Decision Ledger；
- 清晰目录结构；
- 可运行入口；
- Typed Contract；
- 至少一个完整任务闭环；
- 单元 / 集成测试；
- Eval Dataset；
- 环境配置示例；
- README 运行方式；
- 已知限制与下一阶段 Roadmap。

## Report Back to Master

阶段完成或切换 Skill 时，按 `../agent-engineering-master/SKILL-REGISTRY.md` 的 Return Contract 返回。Boundary Canvas、Decision Ledger 与架构摘要由 Master 写入当前项目 `.agent-engineering/`。

---

## Completion Criteria

只有同时满足以下条件才算完成：

1. 新环境能启动；
2. 核心任务可端到端执行；
3. Agent 的 Goal / Autonomy / Tool / Permission Boundary 明确；
4. Tool / RAG / State 行为可测试；
5. 错误不会静默吞掉；
6. 有明确终止条件和预算；
7. 有至少一组回归 / Eval；
8. 输出可追溯；
9. 高风险动作有安全控制；
10. 下一步扩展不需要推翻核心契约。
