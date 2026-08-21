# Agent Engineering Skills

> 面向 Codex / Coding Agent / Engineering Agent 的可复用工程技能集。目标不是提供几个“万能提示词”，而是把 **从 0 到 1、新功能接入、半路改造、架构审查、故障排查、RAG、Multi-Agent、评测、安全、生产化与性能治理** 固化为可重复执行的工程流程。

每个 Skill 使用独立目录，并以 `SKILL.md` 作为入口：

```text
skills/
├─ README.md
├─ agent-project-orchestrator/
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
   └─ verification-report.md
```

## Skill 路由

| 用户任务 | 首选 Skill | 可组合 Skill |
|---|---|---|
| 从 0 到 1 新建 Agent | `agent-greenfield-builder` | RAG / Multi-Agent / Productionizer |
| 接手已有项目继续开发 | `agent-existing-project-modifier` | Architecture / Debugger / Eval |
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
| 任务描述模糊，不知道该走哪条路径 | `agent-project-orchestrator` | 自动选择其他 Skill |

## 统一工程原则

所有 Skill 都遵守以下约束：

1. **先理解，再修改**：已有项目必须先建立现状模型和 Baseline；禁止直接凭想象重写。
2. **确定性优先**：能用普通代码、规则、状态机解决的问题，不交给 LLM。
3. **Workflow 优先于自治**：固定流程优先 Workflow；动态决策才使用 Agent。
4. **Single Agent 优先于 Multi-Agent**：除非角色、权限、Context、工具或并发边界确实需要拆分。
5. **契约优先**：Agent / Tool / Worker / Queue / RAG 之间优先定义 Typed Contract / Schema。
6. **最小权限**：Tool 默认拒绝，显式 Allowlist / Scope 授权。
7. **有界执行**：必须限制 Step、Model Call、Tool Call、Token、Cost、Retry 与 Time。
8. **可恢复**：长任务需要 Task State、Checkpoint、Resume、Idempotency 与 Cancellation。
9. **可观测**：关键路径需要 Trace、Event、Metric、Error Category。
10. **评测先于上线**：功能完成不等于可发布；必须有 Regression / Eval Gate。
11. **安全失败**：不确定、高风险、越权、预算超限时优先 Fail Closed 或进入 HITL。
12. **不制造无关改动**：修改现有项目时禁止顺手格式化、升级依赖或改名大量无关代码。

## 推荐组合

### 从 0 到 1

```text
agent-project-orchestrator
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

### 半路接手 / 修改

```text
agent-existing-project-modifier
  ↓
建立 Baseline + Invariants
  ↓
分析 Blast Radius
  ↓
最小变更
  ↓
agent-debugger / agent-architecture-reviewer（按需）
  ↓
agent-eval-hardening
  ↓
回归与变更报告
```

## Skill 使用约定

每个 `SKILL.md` 都包含 YAML Frontmatter：

```yaml
---
name: skill-name
description: When and why the agent should use this skill.
---
```

然后按以下结构编写：

```text
Objective
When To Use
Do Not Use When
Non-Negotiable Rules
Workflow
Decision Rules
Required Outputs
Verification
Failure Handling
Completion Criteria
```

Skill 可以复制到 Agent 支持的 Skills 目录中使用，也可以直接作为仓库内 Engineering Playbook 被其他 Agent 引用。

## 三个模板

- `templates/project-intake.md`：建立项目现状、目标、约束与风险边界。
- `templates/change-impact.md`：已有项目修改前的影响面分析。
- `templates/verification-report.md`：修改后的测试、Eval、安全和残余风险记录。

## 核心思想

> 一个专业 Agent 工程 Skill 的价值，不在于告诉模型“你是资深工程师”，而在于约束它 **先看什么、后做什么、何时停止、哪些不能做、如何验证、失败后如何恢复**。
