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
| Guided Design | `../agent-guided-builder/SKILL.md` | 目标/边界不清、需要用户参与架构决策 |
| Task Routing | `../agent-project-orchestrator/SKILL.md` | 任务跨多个领域或初始意图模糊 |
| Greenfield | `../agent-greenfield-builder/SKILL.md` | 新项目从 0 到 1 |
| Existing Project Change | `../agent-existing-project-modifier/SKILL.md` | 已有项目新增、重构、迁移、兼容修改 |
| Architecture | `../agent-architecture-reviewer/SKILL.md` | 职责混乱、过度 Agent 化、结构耦合 |
| Debugging | `../agent-debugger/SKILL.md` | 死循环、Tool 不调用、State 错乱、异常轨迹 |
| RAG | `../agent-rag-engineer/SKILL.md` | Retrieval、Rerank、Citation、ACL、Agentic RAG |
| Multi-Agent | `../agent-multi-agent-designer/SKILL.md` | Supervisor、Handoff、并行 Worker、A2A |
| Evaluation | `../agent-eval-hardening/SKILL.md` | Regression、Golden Set、Trajectory、Release Gate |
| Security | `../agent-security-reviewer/SKILL.md` | Injection、权限、Identity、敏感 Tool、HITL |
| Performance | `../agent-performance-cost-optimizer/SKILL.md` | Token、Latency、Concurrency、Cost |
| Production | `../agent-productionizer/SKILL.md` | Queue、Worker、Checkpoint、Deploy、SRE |

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
```

任一信号被触发时，可以暂停当前专项流程，加载对应 Skill 处理，再返回原流程。

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

Master 根据结果继续调度，而不是机械返回原 Skill。
