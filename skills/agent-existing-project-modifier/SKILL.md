---
name: agent-existing-project-modifier
description: Modify, extend, migrate, or refactor an existing Agent project without breaking unrelated behavior. Use when adding features, changing models or frameworks, introducing RAG or Multi-Agent, replacing infrastructure, fixing architectural debt, or continuing a partially completed Agent codebase.
---

# Agent Existing Project Modifier

## Objective

安全接手一个已经存在的 Agent 项目，在 **理解现状、保护既有行为、控制影响面** 的前提下完成新增、修改、迁移或重构。

这个 Skill 的核心不是“改得快”，而是 **不把一个局部需求变成全仓库事故**。

## Non-Negotiable Rules

1. **先读后改**：没有建立项目 Baseline 前禁止大规模修改。
2. **保留现有约束**：不覆盖无关配置、不删除无关能力、不擅自换技术栈。
3. **最小改动面**：优先局部适配，不为了“更优雅”重写整个项目。
4. **兼容优先**：公开 API、Schema、数据库、事件、Prompt Contract 的破坏性变化必须显式处理。
5. **先验证旧行为，再验证新行为**。
6. **修改与清理分开**：不要顺手格式化、改名、升级依赖或重排目录。
7. **迁移必须可回滚**。
8. **不依据 README 猜实现**：代码、配置、测试和运行行为优先。

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
- User-visible behavior。

把这些视为 **Regression Contract**。

## Stage 4 — Change Classification

将需求归类为：

- Feature Addition
- Behavioral Change
- Bug Fix
- Refactor
- Framework Migration
- Model / Provider Migration
- Storage Migration
- RAG Upgrade
- Multi-Agent Upgrade
- Performance Optimization
- Security Hardening

不要混淆 Refactor 和 Feature：

> Refactor 应在外部行为基本不变的情况下改变内部结构。

## Stage 5 — Blast Radius Analysis

修改前列出：

```text
Directly changed files:
Direct dependencies:
State / Schema impact:
API impact:
Storage impact:
Prompt impact:
Tool impact:
Eval impact:
Deployment impact:
Rollback path:
```

如果 Blast Radius 明显超过用户目标，重新缩小方案。

## Stage 6 — Choose Change Strategy

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

## Stage 7 — Implement Incrementally

每个 Patch 应尽量做到：

- 一个明确目的；
- 可独立验证；
- 不夹杂无关清理；
- 出错容易定位；
- 可以回退。

推荐顺序：

```text
Contract
→ Adapter
→ Core Logic
→ Wiring
→ Tests
→ Docs / Config
```

## Stage 8 — Agent-Specific Checks

修改 Agent 时重点检查：

### Prompt

- 是否改变结构化输出；
- 是否与 Tool 参数冲突；
- 是否增加无界上下文；
- 是否改变安全约束。

### State

- 新字段是否有默认值；
- Checkpoint 能否读取旧数据；
- Resume 是否兼容。

### Tools

- Tool 名是否变化；
- Input Schema 是否兼容；
- 是否新增副作用；
- 权限是否同步调整。

### RAG

- metadata filter 是否保持；
- tenant scope 是否保持；
- citation 是否丢失。

### Multi-Agent

- Handoff Contract 是否改变；
- Shared State 是否产生写冲突；
- 新 Agent 是否真的需要独立存在。

## Stage 9 — Verification Ladder

按从小到大的顺序验证：

```text
Static / Import
→ Unit Test
→ Component Test
→ Existing Regression
→ New Feature Test
→ Eval
→ Integration
→ Smoke
```

不要一上来只跑最慢的全量测试。

## Stage 10 — Migration Safety

涉及数据库、State、Checkpoint、Vector Index、Event Schema 时必须考虑：

- backward compatibility；
- dual read / dual write（必要时）；
- migration script；
- old data handling；
- rollback；
- version marker。

## Required Change Report

完成后记录：

```text
Goal:
Baseline:
Changed:
Preserved:
Tests executed:
Eval executed:
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
- 用新模型输出“看起来不错”代替 Regression。

## Completion Criteria

任务只有在以下条件满足后才结束：

- 原需求已经实现；
- 无关模块没有被不必要改动；
- Regression Contract 通过；
- 新行为有测试；
- 破坏性变化已显式说明或提供兼容层；
- 有可执行的回滚路径；
- 项目仍然可以从已有入口运行。
