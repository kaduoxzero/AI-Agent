# Agent Engineering Master — Dynamic Skill Registry

本文件是 `agent-engineering-master/SKILL.md` 的能力注册表。

Master Skill 可以在同一个用户任务中按需加载、退出、重新进入其他 Skill，而不是只在任务开头选择一次。

---

## Mandatory Bootstrap

在调用任何专项 Skill 之前，Master **必须先执行项目状态引导流程**。

引导流程、模板只读约束、Project Root Resolution、多项目隔离与并发写入规则，唯一权威来源：

```text
PROJECT-STATE-POLICY.md
```

核心模型：

```text
skills/templates/                  Shared + Read Only
        ↓ instantiate
Project A/.agent-engineering/      Project A State
Project B/.agent-engineering/      Project B State
```

两个项目之间不得自动共享 Decision、Boundary、Session 或 Verification。如果用户明确要求跨项目比较或迁移，可以读取其他项目状态作为输入，但不得隐式合并。

---

## Capability Registry

| Capability | Skill | Trigger Examples |
|---|---|---|
| Requirement Grilling | `../agent-grill-me/SKILL.md` | 需求模糊、不完整、多方案歧义、隐藏边界条件 |
| Guided Design | `../agent-guided-builder/SKILL.md` | 目标/边界不清、需要用户参与架构决策 |
| Task Routing | `../agent-project-orchestrator/SKILL.md` | 任务跨多个领域或初始意图模糊 |
| Greenfield | `../agent-greenfield-builder/SKILL.md` | 新项目从 0 到 1 |
| Existing Project Change | `../agent-existing-project-modifier/SKILL.md` | 已有项目新增、重构、迁移、兼容修改 |
| Enterprise Handover | `../agent-enterprise-handover/SKILL.md` | 项目交接、离职/轮岗移交、模块交接、项目接手、交接审计、Agent-to-Agent handover |
| Architecture | `../agent-architecture-reviewer/SKILL.md` | 职责混乱、过度 Agent 化、结构耦合 |
| Debugging | `../agent-debugger/SKILL.md` | 死循环、Tool 不调用、State 错乱、异常轨迹 |
| RAG | `../agent-rag-engineer/SKILL.md` | Retrieval、Rerank、Citation、ACL、Agentic RAG |
| Multi-Agent | `../agent-multi-agent-designer/SKILL.md` | Supervisor、Handoff、并行 Worker、A2A |
| Evaluation | `../agent-eval-hardening/SKILL.md` | Regression、Golden Set、Trajectory、Release Gate |
| Security | `../agent-security-reviewer/SKILL.md` | Injection、权限、Identity、敏感 Tool、HITL |
| Performance | `../agent-performance-cost-optimizer/SKILL.md` | Token、Latency、Concurrency、Cost |
| Production | `../agent-productionizer/SKILL.md` | Queue、Worker、Checkpoint、Deploy、SRE |

---

## Requirement Gate

需求存在歧义、不完整、多方案或隐藏边界时，**先进 `agent-grill-me` 澄清，再决定后续路由**：

```text
需求模糊 / 不完整
    ↓
agent-grill-me（最少高价值问题 + 边界扫描）
    ↓
澄清后任务属于 Agent 系统建设？
├─ 是 → agent-guided-builder 深化架构边界
└─ 否 → 直接实现，或移交对应专项 Skill
```

grill-me 产出的已确认决策写入当前项目 `决策记录.md`，边界结论写入 `边界画布.md`；后续 Skill 禁止重复询问这些内容。

对于明确的“交接 / 接手 / 移交 / takeover / ownership transfer”请求，不需要因为交接内容很多就强制进入 Guided Builder。应优先进入 `agent-enterprise-handover`，由其先做 Scope Freeze 和 Asset Discovery；只有交接范围本身存在关键歧义时，才临时调用 `agent-grill-me`。

---

## Runtime Skill Switching

Master 应在执行过程中持续观察以下信号：

```text
Architecture Signal
Debug Signal
RAG Signal
Multi-Agent Signal
Security Signal
Evaluation Signal
Performance Signal
Production Signal
Handover Signal
```

任一信号被触发时，可以暂停当前专项流程，加载对应 Skill 处理，再返回原流程。

### Handover Signal

出现以下信号时优先切换到 `agent-enterprise-handover`：

- 用户要求项目交接、离职交接、模块交接、临时移交；
- 用户要“接手别人项目”并检查缺什么；
- 当前任务即将结束，需要形成可被下一负责人继续执行的正式交接包；
- 发现项目存在强烈 Bus Factor / Knowledge SPOF；
- Agent-to-Agent 需要把复杂任务状态、验证证据和 Next Exact Action 传给下一 Agent；
- 用户要求审查现有交接文档是否真正可执行。

`agent-enterprise-handover` 是聚合型 Primary Skill。它可以按阶段调用 Architecture / Existing Project / Evaluation / Security / Production 等专项 Skill，但任一时刻仍必须遵守 Primary Skill = 1、Supporting Skills <= 2 的加载策略。

例如：

```text
Existing Project Modifier
    ↓
新增 Tool
    ↓
发现 Tool 可执行删除操作
    ↓
Security Reviewer
    ↓
加入 Scope + HITL + Audit
    ↓
返回 Existing Project Modifier
    ↓
完成代码
    ↓
Eval Hardening
```

或者：

```text
Greenfield Builder
    ↓
企业知识库阶段
    ↓
RAG Engineer
    ↓
发现 Retrieval 延迟过高
    ↓
Performance Optimizer
    ↓
返回 RAG Engineer
    ↓
完成 RAG
    ↓
返回 Greenfield Builder
```

交接场景示例：

```text
Enterprise Handover
    ↓
Repository / Architecture Discovery
    ↓
Architecture Reviewer
    ↓
返回 Handover 聚合架构证据
    ↓
Productionizer 验证 Runbook / Release / Rollback
    ↓
返回 Handover
    ↓
Eval Hardening 验证 Smoke / Regression Evidence
    ↓
Acceptance Gates + Final Handover Report
```

---

## Context Passing Contract

Skill 切换时至少传递：

```text
Project ID
Project Root
Goal
Current Stage
Confirmed Boundaries
Relevant Decisions
Current Baseline
Changed Components
Known Risks
Open Questions
Verification Evidence
Return Point
```

这些信息应优先来自当前项目：

```text
<project>/.agent-engineering/
```

禁止仅把用户最初一句需求传给下一个 Skill，否则会丢失已经做出的架构决定。

禁止从另一个项目的 `.agent-engineering/` 自动继承状态。

交接任务额外传递：

```text
Handover Mode
Handover Scope
Current Owner
Target Owner
Evidence Levels
Critical Gaps
Acceptance Gates
Handover Return Point
```

---

## State Write Routing

专项 Skill 返回 Master 后，结果按类型写回当前项目：

```text
Boundary changed
→ .agent-engineering/边界画布.md

Architecture decision
→ .agent-engineering/决策记录.md

Current task progress
→ .agent-engineering/当前会话.md

Blast Radius / Migration impact
→ .agent-engineering/影响分析.md

Verification / Eval / Security evidence
→ .agent-engineering/验证报告.md

Completed task summary
→ .agent-engineering/history/
```

交接专项产物默认写入：

```text
.agent-engineering/交接/
```

交接中产生的长期有效架构决策、验证结论和风险不能只留在交接目录；仍应同步到对应长期项目状态文件。

实例文件中文命名的映射规则见 `resources/PROJECT-DOCUMENT-NAMING.md`。

`skills/templates/` 永远不作为写入目标。

---

## Return Contract

专项 Skill 返回 Master 时至少提供：

```text
Skill Used:
Problem Addressed:
Decision / Change:
Boundary Impact:
Files / Components Affected:
Verification Performed:
New Risks:
Unresolved Items:
Recommended Next Capability:
```

`agent-enterprise-handover` 额外返回：

```text
Handover Mode:
Handover Scope:
Evidence Level Summary:
Handover Score:
Acceptance Gates:
Critical Gaps:
Ownership Changes:
Handover Status:
Next Exact Action:
```

Master 根据结果继续调度，而不是机械返回原 Skill。
