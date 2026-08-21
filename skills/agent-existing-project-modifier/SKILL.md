---
name: agent-existing-project-modifier
description: Modify, extend, migrate, or refactor an existing Agent project without breaking unrelated behavior. Use when adding features, changing models or frameworks, introducing RAG or Multi-Agent, replacing infrastructure, fixing architectural debt, or continuing a partially completed Agent codebase. For architecture-impacting changes, establish the change boundary through agent-guided-builder before implementation.
---

# Agent Existing Project Modifier

## Objective

安全接手一个已经存在的 Agent 项目，在 **理解现状、保护既有行为、控制影响面** 的前提下完成新增、修改、迁移或重构。

这个 Skill 的核心不是“改得快”，而是 **不把一个局部需求变成全仓库事故**。

## Guided Change Rule

已有项目不意味着不需要引导，但引导的对象应该是 **变化本身**，而不是重新设计整个系统。

出现以下情况时，先使用 `agent-guided-builder` 的 Existing Project Mode：

- Single Agent → Multi-Agent；
- 新增高风险 Tool 或真实业务写操作；
- 新增长期 Memory；
- 引入 RAG / Agentic RAG 并改变数据边界；
- 更换 Runtime / Framework / Queue / Persistence；
- 权限、Identity、Tenant Model 变化；
- Workflow → 自治 Agent；
- 需要改变任务生命周期、Checkpoint、HITL；
- 用户只说“帮我升级一下”，但升级边界不清晰。

Guided Change 只讨论：

```text
Current Boundary
Requested Change
New Boundary
Trade-off
Compatibility
Migration
Rollback
Verification
```

能从代码和配置读取到的信息禁止再次问用户。

## Non-Negotiable Rules

1. **先读后改**：没有建立项目 Baseline 前禁止大规模修改。
2. **保留现有约束**：不覆盖无关配置、不删除无关能力、不擅自换技术栈。
3. **最小改动面**：优先局部适配，不为了“更优雅”重写整个项目。
4. **兼容优先**：公开 API、Schema、数据库、事件、Prompt Contract 的破坏性变化必须显式处理。
5. **先验证旧行为，再验证新行为**。
6. **修改与清理分开**：不要顺手格式化、改名、升级依赖或重排目录。
7. **迁移必须可回滚**。
8. **不依据 README 猜实现**：代码、配置、测试和运行行为优先。
9. 对架构级变化必须建立 Change Boundary 和 Decision Ledger。
10. 不允许“为了升级”无理由提升自治等级或 Multi-Agent 复杂度。

## Stage 1 — Repository Reconnaissance

先读取并建立结构图：

```text
Entry Points
Configuration
Agent / Graph / Workflow
Prompts
Tools
RAG / Memory
State / Checkpoint
API
Worker / Queue
Storage
Tests / Evals
Deployment
Observability
Security / Identity
```

优先检查：

- `README` / architecture docs；
- package manager / dependency file；
- main entry；
- Agent / Graph 构造位置；
- Prompt 和 Tool 注册位置；
- State / Schema；
- `.env.example` / config；
- tests / evals；
- Docker / CI。

## Stage 2 — Build Baseline

在修改前记录：

```text
Current behavior:
Current architecture level:
Current autonomy boundary:
Current tools / permissions:
Current state / memory:
Current tests:
Current runtime:
Current dependencies:
Current public contracts:
Current known failures:
```

如果项目能运行，先执行最小 Smoke Test。

如果项目已经坏掉，记录“修改前失败”，不要把旧问题误认为新改动造成。

## Stage 3 — Extract Invariants

识别不可破坏行为：

- API path / request / response；
- Task Status；
- Tool 名称和参数；
- Agent State key；
- Event type；
- 数据库字段；
- RAG metadata；
- Tenant isolation；
- Prompt 输出格式；
- User-visible behavior；
- Approval / Permission behavior；
- Resume semantics。

把这些视为 **Regression Contract**。

## Stage 4 — Change Boundary Canvas

架构级修改前必须形成：

```text
Why change:
What must change:
What must NOT change:
Current boundary:
Target boundary:
New permissions:
New side effects:
New state:
New dependencies:
New cost / latency:
Migration:
Rollback:
Acceptance:
```

如果用户还没有决定关键目标，进入 `agent-guided-builder`，每轮只处理一个关键变化。

## Stage 5 — Change Classification

将需求归类为：

- Feature Addition
- Behavioral Change
- Bug Fix
- Refactor
- Framework Migration
- Model / Provider Migration
- Storage Migration
- RAG Upgrade
- Memory Upgrade
- Multi-Agent Upgrade
- Runtime Upgrade
- Performance Optimization
- Security Hardening

不要混淆 Refactor 和 Feature：

> Refactor 应在外部行为基本不变的情况下改变内部结构。

## Stage 6 — Blast Radius Analysis

修改前列出：

```text
Directly changed files:
Direct dependencies:
State / Schema impact:
API impact:
Storage impact:
Prompt impact:
Tool impact:
Permission impact:
RAG / Memory impact:
Eval impact:
Deployment impact:
Rollback path:
```

如果 Blast Radius 明显超过用户目标，重新缩小方案。

## Stage 7 — Choose Change Strategy

优先级：

```text
Adapter
→ New isolated module
→ Extend existing interface
→ Local refactor
→ Compatibility layer
→ Migration
→ Major rewrite（最后选择）
```

### Framework Migration

例如 LangChain → LangGraph：

不要先删除旧实现。

推荐：

```text
Extract stable contracts
→ Build new runtime behind interface
→ Run parity tests
→ Switch traffic / entry
→ Remove legacy after verification
```

### Model Provider Migration

模型切换不得让业务层直接绑定新的 SDK。

使用 Model Gateway / Provider Adapter。

### RAG Upgrade

先保持 Evidence Contract 不变，再替换 Retriever / Reranker / Vector Store。

### Single Agent → Multi-Agent

必须先回答：

- 新 Agent 是否有独立权限？
- 是否有独立 Context？
- Tool Set 是否不同？
- 是否存在真实并行收益？
- Shared State 谁负责写？
- Handoff Contract 是什么？
- 一个 Agent 为什么不能完成？

不能回答时不要拆。

## Stage 8 — Implement Incrementally

每个 Patch 应尽量做到：

- 一个明确目的；
- 可独立验证；
- 不夹杂无关清理；
- 出错容易定位；
- 可以回退。

推荐顺序：

```text
Contract
→ Compatibility / Adapter
→ Core Logic
→ Wiring
→ Tests
→ Eval
→ Docs / Config
```

## Stage 9 — Agent-Specific Checks

### Prompt

- 是否改变结构化输出；
- 是否与 Tool 参数冲突；
- 是否增加无界上下文；
- 是否改变安全约束；
- Prompt Version 是否需要变化。

### State

- 新字段是否有默认值；
- Checkpoint 能否读取旧数据；
- Resume 是否兼容；
- 是否需要 State Migration。

### Tools

- Tool 名是否变化；
- Input Schema 是否兼容；
- 是否新增副作用；
- 权限是否同步调整；
- Idempotency 是否仍成立。

### RAG

- metadata filter 是否保持；
- tenant scope 是否保持；
- citation 是否丢失；
- Evidence Contract 是否兼容。

### Memory

- 新 Memory 是否改变数据生命周期；
- 是否有 Write Policy / TTL；
- 旧数据如何处理；
- 是否引入 Memory Poisoning 风险。

### Multi-Agent

- Handoff Contract 是否改变；
- Shared State 是否产生写冲突；
- 新 Agent 是否真的需要独立存在；
- Failure Propagation 是否定义。

### Runtime

- Task Status 是否变化；
- Retry 是否可能重复副作用；
- Worker Crash 能否恢复；
- Budget 是否保持有界。

## Stage 10 — Verification Ladder

按从小到大的顺序验证：

```text
Static / Import
→ Unit Test
→ Component Test
→ Existing Regression
→ New Feature Test
→ Eval
→ Integration
→ Failure / Resume
→ Security
→ Smoke
```

不要一上来只跑最慢的全量测试。

## Stage 11 — Migration Safety

涉及数据库、State、Checkpoint、Vector Index、Event Schema、Memory 时必须考虑：

- backward compatibility；
- dual read / dual write（必要时）；
- migration script；
- old data handling；
- rollback；
- version marker；
- canary / staged rollout。

## Required Change Report

完成后记录：

```text
Goal:
Baseline:
Accepted Decisions:
Changed:
Preserved:
Tests executed:
Eval executed:
Security checks:
Breaking changes:
Migration required:
Known limitations:
Rollback:
```

## Anti-Patterns

禁止：

- “项目有点乱，所以我全部重构了”；
- “为了新功能顺便升级所有依赖”；
- 未读测试就删除旧代码；
- 为了加一个 Tool 把 Single Agent 改成 Multi-Agent；
- 修改 State Schema 却不测试 Resume；
- 修改 RAG 却不验证 Tenant Filter；
- 新增 Memory 却不定义写入边界；
- 用新模型输出“看起来不错”代替 Regression；
- 用户要求一个局部修改却重新设计整个 Agent Platform。

## Completion Criteria

任务只有在以下条件满足后才结束：

- 原需求已经实现；
- Change Boundary 没有失控；
- 无关模块没有被不必要改动；
- Regression Contract 通过；
- 新行为有测试；
- 架构级变化已记录 Decision Ledger；
- 破坏性变化已显式说明或提供兼容层；
- 有可执行的回滚路径；
- 项目仍然可以从已有入口运行。
