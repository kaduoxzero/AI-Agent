# Agent Engineering Skills

> 面向 Codex / Coding Agent / Engineering Agent 的可复用工程技能集。目标不是提供几个“万能提示词”，而是把 **引导式需求澄清、从 0 到 1、新功能接入、半路改造、架构审查、故障排查、RAG、Multi-Agent、评测、安全、生产化与性能治理** 固化为可重复执行的工程流程。

仓库整体采用根目录 `LICENSE` 中的 **GNU GPL v3.0**；`skills/` 作为本仓库组成部分遵循同一仓库级许可。

## 核心变化：Guided Agent Engineering

这套 Skills 不再要求 Agent “收到需求就直接写代码”。

对于需求尚未形成清晰边界的场景，优先使用：

```text
agent-project-orchestrator
  ↓
agent-guided-builder
  ↓
Boundary Canvas + Decision Ledger
  ↓
agent-greenfield-builder / agent-existing-project-modifier
  ↓
专项 Skill
  ↓
Implementation + Eval + Production
```

`agent-guided-builder` 会让 Agent 像架构师 / 教练一样逐步带用户做关键决策：

- 一次只推进一个主要决策阶段；
- 优先提供 A/B/C/D 选项；
- 明确推荐项；
- 解释推荐原因和 Trade-off；
- 说明选择会新增什么边界、权限、成本和故障面；
- 已确认的信息进入 Decision Ledger，不重复询问；
- 普通代码细节由 Agent 自主决定，不频繁打断用户。

## 目录

```text
skills/
├─ README.md
├─ agent-project-orchestrator/
│  └─ SKILL.md
├─ agent-guided-builder/
│  └─ SKILL.md
├─ agent-greenfield-builder/
│  └─ SKILL.md
├─ agent-existing-project-modifier/
│  └─ SKILL.md
├─ agent-architecture-reviewer/
│  └─ SKILL.md
├─ agent-debugger/
│  └─ SKILL.md
├─ agent-rag-engineer/
│  └─ SKILL.md
├─ agent-multi-agent-designer/
│  └─ SKILL.md
├─ agent-eval-hardening/
│  └─ SKILL.md
├─ agent-productionizer/
│  └─ SKILL.md
├─ agent-security-reviewer/
│  └─ SKILL.md
├─ agent-performance-cost-optimizer/
│  └─ SKILL.md
└─ templates/
   ├─ project-intake.md
   ├─ change-impact.md
   ├─ verification-report.md
   ├─ agent-boundary-canvas.md
   ├─ decision-ledger.md
   └─ guided-session-state.md
```

## Skill 路由

| 用户任务 | 首选 Skill | 可组合 Skill |
|---|---|---|
| “一步步带我设计一个 Agent” | `agent-guided-builder` | Greenfield / RAG / Multi-Agent |
| “帮我考虑 Agent 边界” | `agent-guided-builder` | Architecture / Security |
| 需求模糊，不知道 Agent 怎么拆 | `agent-project-orchestrator` → `agent-guided-builder` | 按结果继续路由 |
| 从 0 到 1 新建 Agent，需求已明确 | `agent-greenfield-builder` | RAG / Multi-Agent / Productionizer |
| 从 0 到 1，但关键决策未明确 | `agent-guided-builder` → `agent-greenfield-builder` | 按需 |
| 接手已有项目继续开发 | `agent-existing-project-modifier` | Architecture / Debugger / Eval |
| 已有项目进行架构级升级 | `agent-guided-builder` → `agent-existing-project-modifier` | Architecture / Eval |
| 加新功能但不能破坏现有逻辑 | `agent-existing-project-modifier` | Eval / Security |
| LangChain → LangGraph、模型或 Provider 迁移 | `agent-existing-project-modifier` | Architecture / Eval |
| 项目结构混乱，需要重构 | `agent-architecture-reviewer` | Existing Modifier |
| Agent 不调用工具、死循环、状态错乱 | `agent-debugger` | Eval / Architecture |
| 企业知识库、RAG、Agentic RAG | `agent-rag-engineer` | Eval / Security / Productionizer |
| Supervisor、Handoff、Swarm 等 | `agent-multi-agent-designer` | Eval / Architecture |
| “能跑但不稳定” | `agent-eval-hardening` | Debugger / Productionizer |
| 从 Demo 推到生产 | `agent-productionizer` | Security / Performance / Eval |
| Prompt Injection、越权、Tool 风险 | `agent-security-reviewer` | Productionizer |
| Token、延迟、并发、成本太高 | `agent-performance-cost-optimizer` | Eval / Architecture |

## Agent Boundary Canvas

Guided Builder 固定检查 13 类边界：

```text
1. Goal Boundary
2. User Boundary
3. Input Boundary
4. Output Boundary
5. Autonomy Boundary
6. Knowledge Boundary
7. Tool Boundary
8. Side-Effect / Permission Boundary
9. State / Session / Memory / Checkpoint
10. Multi-Agent Boundary
11. Time / Token / Cost Boundary
12. Safety / HITL Boundary
13. Failure / Recovery Boundary
```

每类边界必须被判断为：

```text
Required
Not Required
Deferred
Unknown
```

目标不是把系统设计得复杂，而是避免关键边界因为“没想到”而缺失。

## Guided Workshop 的 14 个阶段

```text
Stage 0  Problem Framing
Stage 1  Success / Failure / Acceptance
Stage 2  Need Agent or Not
Stage 3  Autonomy Boundary
Stage 4  Knowledge Boundary
Stage 5  Tool / Side-Effect Boundary
Stage 6  State / Memory / Checkpoint
Stage 7  Multi-Agent Boundary
Stage 8  Runtime / Reliability
Stage 9  Identity / Security / HITL
Stage 10 Evaluation
Stage 11 Observability / Operations
Stage 12 Architecture Freeze
Stage 13 Incremental Build
```

### 每轮交互标准

推荐形式：

```text
当前阶段：Tool / Side-Effect Boundary

为什么现在要决定：
这个选择会影响权限、审计、HITL、幂等和恢复。

A. 只读
B. 低风险写操作
C. 高风险操作必须审批
D. 高风险自治执行

推荐：C
原因：既保留自动化能力，又避免模型直接执行不可逆动作。

Trade-off：增加 Approval 流程和状态管理。
Boundary Impact：Permission / HITL / Audit / Rollback

请选择 A/B/C/D，或直接描述你的约束。
```

禁止一次性向用户抛 20 个问题。

## Decision Ledger

每个关键架构决定都持续记录：

```text
Decision ID
Topic
Status
Options Considered
Decision
Why
Trade-offs
New Risks
Affected Components
Verification
```

这样后续 Agent 不会因为上下文变长而忘记：

- 为什么没有使用 Multi-Agent；
- 为什么某个 Tool 需要审批；
- 为什么选择 RAG 而不是长期 Memory；
- 为什么使用 Queue + Worker；
- 为什么限制某个模型或成本预算。

## 用户说“直接做”怎么办

Guided 模式不是强制一直提问。

如果用户明确说：

> 不需要再问我，按最佳方案直接做。

Agent 应：

```text
读取已有信息
→ 内部填写 Boundary Canvas
→ 按安全默认值做关键决策
→ Decision Ledger 标记 Agent Recommended Decision
→ 直接执行
```

只有遇到无法安全推断、会产生不可逆高风险后果的决策才暂停。

## 统一工程原则

所有 Skill 都遵守：

1. **先理解，再修改**：已有项目先建立 Baseline。
2. **边界先于框架**：先定义职责、自治、权限、数据和失败边界，再决定 LangGraph / SDK。
3. **确定性优先**：能用普通代码、规则、状态机解决的问题，不交给 LLM。
4. **Workflow 优先于自治**：固定流程优先 Workflow；动态决策才使用 Agent。
5. **Single Agent 优先于 Multi-Agent**：除非角色、权限、Context、工具或并发边界确实需要拆分。
6. **契约优先**：模块之间优先 Typed Contract / Schema / Artifact。
7. **最小权限**：Tool 默认拒绝，显式 Allowlist / Scope 授权。
8. **有界执行**：限制 Step、Model Call、Tool Call、Token、Cost、Retry 与 Time。
9. **可恢复**：长任务需要 Task State、Checkpoint、Resume、Idempotency 与 Cancellation。
10. **可观测**：关键路径需要 Trace、Event、Metric、Error Category。
11. **评测先于上线**：必须有 Regression / Eval Gate。
12. **安全失败**：不确定、高风险、越权、预算超限时 Fail Closed 或进入 HITL。
13. **不制造无关改动**：已有项目不顺手重构无关代码。
14. **不重复询问**：已经由用户或代码解决的问题不得重复问。

## 推荐组合

### 从 0 到 1，引导式

```text
agent-project-orchestrator
  ↓
agent-guided-builder
  ↓
Architecture Freeze
  ↓
agent-greenfield-builder
  ↓
[RAG?] agent-rag-engineer
  ↓
[Multi-Agent?] agent-multi-agent-designer
  ↓
agent-eval-hardening
  ↓
agent-security-reviewer
  ↓
agent-productionizer
```

### 从 0 到 1，需求已经非常明确

```text
agent-greenfield-builder
  ↓
专项 Skill
  ↓
Eval / Security / Production
```

### 半路接手 / 修改

```text
Repository Reconnaissance
  ↓
Baseline + Invariants
  ↓
[架构变化未决?] agent-guided-builder
  ↓
Change Boundary Freeze
  ↓
agent-existing-project-modifier
  ↓
agent-debugger / agent-architecture-reviewer（按需）
  ↓
agent-eval-hardening
  ↓
Regression + Change Report
```

## Skill 使用约定

每个 `SKILL.md` 包含 YAML Frontmatter：

```yaml
---
name: skill-name
description: When and why the agent should use this skill.
---
```

正文通常包含：

```text
Objective
When To Use
Non-Negotiable Rules
Workflow
Decision Rules
Boundary Rules
Required Outputs
Verification
Failure Handling
Completion Criteria
```

## Templates

- `templates/project-intake.md`：项目现状、目标、约束与风险。
- `templates/change-impact.md`：修改前影响面分析。
- `templates/verification-report.md`：测试、Eval、安全和残余风险记录。
- `templates/agent-boundary-canvas.md`：系统化检查 Agent 的职责、自治、知识、Tool、权限、State、Memory、Budget、安全和失败边界。
- `templates/decision-ledger.md`：持续记录重要架构选择及 Trade-off。
- `templates/guided-session-state.md`：多轮引导中保存阶段进度、已解决信息和下一项关键决策。

## 核心思想

> 一个专业 Agent 工程 Skill 的价值，不是告诉模型“你是资深工程师”，而是让它知道 **现在应该问什么、哪些不该问、如何给选项、怎么考虑边界、什么时候才能开始编码、如何验证，以及发生失败时如何恢复**。
