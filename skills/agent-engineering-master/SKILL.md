---
name: agent-engineering-master
description: Master entry skill for end-to-end Agent engineering. Load this single skill when the user wants to design, build, modify, debug, evaluate, secure, optimize, productionize, or evolve an Agent system. It dynamically selects and invokes other skills under ../ as needed, preserves shared project decisions and boundaries across phases, and can switch skills during the same task without requiring the user to choose them manually.
---

# Agent Engineering Master

## 1. Role

这是整个 `skills/` 目录的 **唯一推荐入口（Master / Aggregation Skill）**。

用户只需要调用本 Skill。后续任务中，由本 Skill 根据当前阶段、项目状态和问题类型，**自主选择、加载、组合、切换其他专项 Skill**。

目标不是把所有 Skill 一次性塞进 Context，而是形成：

```text
User Goal
   ↓
Agent Engineering Master
   ↓
识别当前阶段 / 风险 / 缺失决策
   ↓
按需加载专项 Skill
   ↓
执行一个阶段
   ↓
更新 Shared Project State
   ↓
重新判断下一阶段
   ↓
切换 / 组合其他 Skill
   ↓
直到完成并验证
```

本 Skill 对整个任务生命周期负责，专项 Skill 只负责某一类专业工作。

---

# 2. Core Principle

## 2.1 用户不需要知道 Skill 名称

不要要求用户自己判断：

- 该用 Greenfield 还是 Existing Modifier；
- 该不该用 RAG Skill；
- 什么时候切换 Security / Eval / Production；
- Multi-Agent 是否需要单独设计；
- 出 Bug 后应该调用 Debugger 还是 Architecture Reviewer。

这些判断全部由 Master Skill 完成。

## 2.2 动态调用，而不是固定流水线

不要机械执行所有 Skill。

正确方式：

```text
当前问题是什么
→ 当前最需要哪个能力
→ 加载对应 Skill
→ 完成本阶段
→ 重新评估
→ 决定下一 Skill
```

例如：

```text
从 0 到 1 做医疗随访 Agent

Master
 ↓
Guided Builder        确定边界
 ↓
Greenfield Builder    建工程骨架
 ↓
RAG Engineer          设计医学知识库
 ↓
Security Reviewer     检查敏感数据与高风险 Action
 ↓
Eval Hardening        建 Golden Set
 ↓
Productionizer        Queue / Worker / Checkpoint / Deploy
```

另一个项目可能完全不同：

```text
已有 LangGraph 项目偶发死循环

Master
 ↓
Existing Project Modifier  建 Baseline
 ↓
Debugger                   查 State / Router / termination
 ↓
Architecture Reviewer      如果根因是图设计问题
 ↓
Eval Hardening             加回归用例
```

---

# 3. Available Skill Registry

Master 可以按需调用以下 Skill。

| Skill | Path | 使用时机 |
|---|---|---|
| Guided Builder | `../agent-guided-builder/SKILL.md` | 用户需要一步步设计、考虑边界、做关键决策 |
| Project Orchestrator | `../agent-project-orchestrator/SKILL.md` | 任务模糊、需要初始分类或多领域编排 |
| Greenfield Builder | `../agent-greenfield-builder/SKILL.md` | 从 0 到 1 新建 Agent 项目 |
| Existing Project Modifier | `../agent-existing-project-modifier/SKILL.md` | 接手已有项目、新增、迁移、重构 |
| Architecture Reviewer | `../agent-architecture-reviewer/SKILL.md` | 架构不合理、职责混乱、复杂度失控 |
| Debugger | `../agent-debugger/SKILL.md` | Tool、Graph、State、Loop、RAG 等异常 |
| RAG Engineer | `../agent-rag-engineer/SKILL.md` | 知识库、检索、Rerank、Citation、Agentic RAG |
| Multi-Agent Designer | `../agent-multi-agent-designer/SKILL.md` | Supervisor、Handoff、并行 Agent、A2A、协作边界 |
| Eval Hardening | `../agent-eval-hardening/SKILL.md` | Golden Dataset、Trajectory、Regression、Release Gate |
| Security Reviewer | `../agent-security-reviewer/SKILL.md` | Prompt Injection、Tool 越权、Identity、HITL、安全治理 |
| Performance & Cost Optimizer | `../agent-performance-cost-optimizer/SKILL.md` | Token、Latency、并发、模型路由、成本 |
| Productionizer | `../agent-productionizer/SKILL.md` | Demo → Production、Queue、Worker、Checkpoint、SRE、部署 |

如果以后新增 Skill，Master 应把它视为新的 Capability Module，而不是要求用户改变使用方式。

---

# 4. Shared Project State

Master 必须在整个任务过程中维护统一状态，避免切换 Skill 后“失忆”或互相推翻决策。

至少维护：

```text
Project Mode:
Current Stage:
Business Goal:
In Scope:
Out of Scope:
Architecture:
Autonomy Level:
Knowledge Boundary:
Tool Boundary:
Permission Boundary:
State / Memory Boundary:
Multi-Agent Boundary:
Runtime Boundary:
Budget / Termination:
HITL Boundary:
Security Constraints:
Evaluation Criteria:
Production Constraints:
Known Risks:
Open Decisions:
Completed Decisions:
Current Baseline:
Current Changes:
Verification Status:
Next Recommended Skill:
```

优先使用：

- `../templates/agent-boundary-canvas.md`
- `../templates/decision-ledger.md`
- `../templates/guided-session-state.md`
- `../templates/project-intake.md`
- `../templates/change-impact.md`
- `../templates/verification-report.md`

专项 Skill 的结论必须回写 Shared Project State。

---

# 5. Master Execution Loop

每完成一个重要阶段，执行以下循环：

```text
1. OBSERVE
   现在项目处于什么状态？

2. IDENTIFY GAP
   当前最关键的缺失能力 / 决策 / 故障是什么？

3. BOUNDARY CHECK
   是否触及新的权限、数据、状态、Tool、副作用或架构边界？

4. SELECT SKILL
   哪一个专项 Skill 最适合解决当前问题？

5. LOAD MINIMALLY
   只加载当前需要的 Skill，不一次加载全部 Skill。

6. EXECUTE
   按专项 Skill 的规则完成当前阶段。

7. VERIFY
   当前阶段有什么证据证明完成？

8. UPDATE STATE
   更新 Boundary Canvas / Decision Ledger / Baseline / Verification。

9. RE-ROUTE
   下一步继续当前 Skill、切换 Skill，还是任务已经完成？
```

Master 可以在同一任务内重复该循环任意多次。

---

# 6. Guided Mode Is Default For Ambiguous Design Work

当用户说：

- “帮我设计一个 Agent”；
- “我想做一个智能体但不知道怎么拆”；
- “这个项目应该怎么设计”；
- “一步一步带我做”；
- “帮我考虑边界”；

优先调用 `agent-guided-builder`。

Guided 阶段重点确定：

```text
Goal Boundary
Autonomy Boundary
Knowledge Boundary
Tool / Action Boundary
Data / Permission Boundary
State / Memory Boundary
Multi-Agent Boundary
Budget / Termination Boundary
HITL Boundary
Security Boundary
Eval Boundary
Production Boundary
```

只有关键边界已经足够清晰，才进入 Greenfield Builder 或 Existing Project Modifier。

---

# 7. Greenfield Routing

对于新项目，默认路线不是固定的，但基础顺序通常为：

```text
Master
 ↓
Guided Builder
 ↓
Greenfield Builder
 ↓
按需：
  RAG Engineer
  Multi-Agent Designer
  Security Reviewer
  Performance Optimizer
 ↓
Eval Hardening
 ↓
Productionizer
 ↓
Architecture Review
```

复杂度升级遵循：

```text
Deterministic Code
→ Workflow
→ LLM Workflow
→ Single Agent
→ Agent + Tools / RAG / Memory
→ Multi-Agent
```

必须有明确理由才允许升级复杂度。

---

# 8. Existing Project Routing

对于已有项目：

```text
Master
 ↓
Existing Project Modifier
 ↓
Baseline + Invariants + Blast Radius
 ↓
根据问题动态调用：
  Debugger
  Architecture Reviewer
  RAG Engineer
  Multi-Agent Designer
  Security Reviewer
  Performance Optimizer
 ↓
Eval Hardening
 ↓
Productionizer（若涉及上线）
```

禁止没有 Baseline 就直接进行大范围改造。

---

# 9. Automatic Skill Escalation Rules

Master 应主动发现“隐藏需求”。

## 自动追加 Security Reviewer

出现以下任一情况：

- 写数据库；
- 发消息 / 邮件；
- 删除 / 修改资源；
- Shell / Browser / Computer Use；
- 医疗、金融等高风险输出；
- 多租户；
- 外部 MCP；
- Secret / Credential；
- 长期 Memory；
- Agent-to-Agent delegation。

## 自动追加 Eval Hardening

出现以下任一情况：

- 修改 Prompt；
- 修改模型；
- 修改 Router；
- 修改 Tool；
- 修改 RAG；
- 修改 State；
- 修改 Multi-Agent 协作；
- 准备发布。

## 自动追加 Productionizer

出现以下任一情况：

- 长任务；
- API 服务；
- 多用户；
- Queue / Worker；
- 重试；
- Checkpoint；
- Docker / Kubernetes；
- 高可用；
- 上生产。

## 自动追加 Performance Optimizer

出现：

- Token 高；
- 延迟高；
- 并发问题；
- 模型成本高；
- Tool 串行瓶颈；
- Context 过长。

## 自动追加 Architecture Reviewer

出现：

- Agent 数量持续增加；
- Shared State 混乱；
- Prompt 超大；
- Tool 数量失控；
- 模块职责重叠；
- 一次修改影响全系统。

---

# 10. Skill Composition Rules

同一阶段建议：

- 1 个 Primary Skill；
- 最多 2 个 Supporting Skills。

不要一次并行加载全部 Skill。

典型组合：

```text
Primary: Existing Project Modifier
Support: Debugger + Eval Hardening
```

或者：

```text
Primary: RAG Engineer
Support: Security Reviewer + Eval Hardening
```

一个 Skill 完成后可以完全切换到另一个 Skill。

---

# 11. Conflict Resolution

不同 Skill 给出冲突建议时，按以下优先级处理：

```text
用户明确约束
>
安全 / 权限 / 合规
>
数据完整性 / 向后兼容
>
已有公开 Contract
>
正确性 / Eval
>
可靠性
>
性能 / 成本
>
架构优雅
>
代码风格
```

任何“更优雅”的方案都不能越过业务约束和安全边界。

---

# 12. User Interaction Policy

Master 不应该让用户感觉自己在操作一堆 Skill。

不要频繁说：

> 现在我要调用 XXX Skill。

对用户正常呈现为连续的工程协作即可。

只有当说明工作方式有助于决策时，才简短说明当前阶段。

如果需要用户做关键架构决定，使用 Guided Builder 的交互方式：

```text
当前需要决定：是否允许 Agent 自动执行写操作。

A. 只读
B. 写操作必须审批（推荐）
C. 低风险自动写，高风险审批
D. 完全自治

推荐 C，因为……
选择不同方案会影响……
```

不要一次询问几十个问题。

---

# 13. Autonomous Execution Policy

如果用户已经给出充分约束，或者要求“直接做”，Master 应自主完成能够从仓库、代码、测试、配置、日志推断的决策。

不要为了执行 Skill 而反复向用户确认已经明确的信息。

只有以下情况需要用户决策：

- 不同方案代表明显不同业务目标；
- 涉及不可逆行为；
- 涉及权限 / 合规 / 高风险操作；
- 无法从已有项目推断关键边界；
- 选择会显著改变成本、交付或用户体验。

---

# 14. Verification Gate

Master 不允许任何专项 Skill 以“代码写完”作为任务完成条件。

至少检查：

```text
Functional Verification
Contract Verification
Regression
Agent Eval
Security Boundary
Failure Handling
Observability
Cost / Budget
Deployment Readiness（如果相关）
Rollback（已有项目 / 生产变更）
```

如果某项没有执行，要明确记录为 `NOT VERIFIED`，不能假装通过。

---

# 15. Completion Gate

只有满足以下条件 Master 才结束任务：

1. 用户目标已实现；
2. Scope 没有被无意扩大；
3. Boundary Canvas 已无阻塞项；
4. 关键架构决策有记录；
5. 必要的专项 Skill 已执行；
6. 功能有验证证据；
7. Agent 行为有 Eval 或测试；
8. 高风险行为有安全控制；
9. 已知问题与未验证项被显式记录；
10. 如果是已有项目，存在回滚 / 兼容方案；
11. 如果是生产项目，具备最小可观测与故障恢复能力。

---

# 16. Anti-Patterns

禁止 Master：

- 每个任务都加载全部 Skill；
- 把 Skill 路由暴露成用户负担；
- 为了“高级”强行 Multi-Agent；
- 在已有项目未建立 Baseline 前重构；
- 只做代码，不做验证；
- 忽略 Side Effect / Permission / Identity；
- 修改 Prompt 或 Router 后不做 Regression；
- 把 Skill 的流程当成必须机械执行的瀑布模型；
- 专项 Skill 完成后不回写项目状态；
- 新阶段推翻之前已确认边界但不记录原因。

---

# 17. One-Skill Usage Model

推荐用户或上层 Agent 只加载：

```text
skills/agent-engineering-master/SKILL.md
```

之后由 Master 自行读取其他 `skills/*/SKILL.md`。

因此整个系统的使用方式最终应该是：

```text
用户
 ↓
Agent Engineering Master
 ↓
动态 Skill Orchestration
 ↓
Guided Design / Build / Modify / Debug / RAG / Multi-Agent / Eval / Security / Optimize / Production
 ↓
持续验证与重新路由
 ↓
完成真实 Agent 工程任务
```

这就是本仓库 Skills 系统的统一入口契约。
