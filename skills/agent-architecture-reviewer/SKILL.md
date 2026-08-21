---
name: agent-architecture-reviewer
description: Review an Agent system architecture for unnecessary complexity, coupling, state problems, tool boundaries, RAG design, Multi-Agent misuse, reliability, observability, security, and production readiness. Use before major refactors, migrations, scaling work, or when an Agent project feels structurally unstable.
---

# Agent Architecture Reviewer

## Objective

判断一个 Agent 项目的问题到底是局部 Bug，还是架构边界本身错误，并给出 **可以逐步落地** 的改造顺序。

## Review Order

必须按以下顺序审查，不要先看框架：

```text
Business Goal
→ Execution Model
→ Contracts
→ State / Context
→ Tool / RAG
→ Agent Boundaries
→ Runtime
→ Reliability
→ Security
→ Observability
→ Deployment
```

## 1. Business / Complexity Fit

回答：

- 这个系统真的需要 Agent 吗？
- Workflow 是否足够？
- Single Agent 是否足够？
- Multi-Agent 是否存在真实职责边界？
- LLM 是否被用于本可由规则完成的判断？

发现过度智能化时，优先建议降复杂度。

## 2. Contract Review

检查：

- API Contract；
- Task / State Schema；
- Tool Input / Output；
- Artifact / Evidence；
- Agent Handoff；
- Event Schema；
- Error Model。

危险信号：

- 模块之间大量传自由文本；
- 同一字段在多个层含义不同；
- Prompt 里隐式约定替代正式 Schema；
- 状态字段没有版本。

## 3. State & Context Review

检查：

- State 是否与 Context 混在一起；
- Session / Memory / Checkpoint 是否混用；
- Context 是否无限增长；
- Resume 是否依赖临时内存；
- Shared State 是否有并发写冲突；
- 是否保存了真正可恢复所需的数据。

## 4. Tool Boundary Review

每个 Tool 应满足：

- 单一职责；
- Typed Contract；
- 明确副作用；
- Timeout；
- Retry Policy；
- Permission Scope；
- Audit；
- 幂等性策略。

危险信号：

- Tool 内部又偷偷做复杂 Agent 推理；
- 所有 Tool 都向所有 Agent 开放；
- Tool 参数完全由模型自由拼接；
- 数据库写操作没有权限和审批边界。

## 5. RAG Review

检查：

```text
Ingestion
Chunking
Metadata
Embedding
Retrieval
Filtering
Reranking
Evidence
Citation
Freshness
Tenant Isolation
```

不要只评 Vector DB。

## 6. Multi-Agent Review

每个 Agent 必须能回答：

```text
Why separate?
Own goal?
Own tools?
Own permissions?
Own context?
Input contract?
Output artifact?
Failure behavior?
```

如果两个 Agent 只是 Prompt 不同，但共享全部工具、状态和职责，通常应该合并。

## 7. Runtime Review

检查是否存在：

- API 与长任务解耦；
- Queue / Worker；
- Persistent Task Store；
- Checkpoint / Resume；
- Cancellation；
- Idempotency；
- Dead Letter / Retry Boundary；
- Event Stream；
- Artifact Store。

## 8. Reliability Review

检查：

- max_steps；
- max_model_calls；
- max_tool_calls；
- timeout；
- retry；
- fallback；
- circuit breaker；
- degraded mode；
- fail closed；
- worker crash recovery。

## 9. Security Review

检查：

- Identity；
- Tenant Isolation；
- Tool Scope；
- Prompt Injection；
- Secret Boundary；
- HITL；
- Audit；
- Sensitive Data；
- External Content Trust Boundary。

## 10. Observability Review

必须能回答一次失败任务的：

```text
谁发起？
跑了哪个 Agent / Version？
用了哪个 Prompt / Model？
经过哪些节点？
调了哪些 Tool？
拿了哪些 Evidence？
花了多少 Token / Cost？
在哪一步失败？
是否 Retry / Resume？
```

无法回答说明可观测性不足。

## Severity

使用四级问题等级：

- **P0**：数据泄露、越权、不可逆错误、严重生产事故风险；
- **P1**：核心任务错误、状态丢失、恢复失败、架构阻塞扩展；
- **P2**：性能、维护性、测试性明显问题；
- **P3**：优化建议、命名、局部结构改善。

## Recommendation Format

每个架构问题必须包含：

```text
Severity:
Problem:
Evidence:
Impact:
Recommended change:
Migration path:
Verification:
```

不要只写“建议优化”。

## Refactor Priority

推荐顺序：

```text
Security / Data Correctness
→ Contract
→ State / Persistence
→ Tool Boundary
→ Runtime Reliability
→ RAG / Agent Topology
→ Observability
→ Performance
→ Cosmetic Structure
```

## Completion Criteria

架构审查完成时应给出：

- 当前架构模型；
- P0-P3 问题；
- 哪些复杂度应该删除；
- 哪些边界应该新增；
- 分阶段迁移顺序；
- 每阶段验收标准；
- 哪些部分不应修改。
