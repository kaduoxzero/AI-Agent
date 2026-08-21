---
name: agent-engineering-master
description: Master entry skill for end-to-end Agent engineering. Load this single skill when the user wants to design, build, modify, debug, evaluate, secure, optimize, productionize, or evolve an Agent system. It dynamically selects other skills as needed and maintains strictly project-scoped engineering state under the current project's .agent-engineering directory.
---

# Agent Engineering Master

## 1. Role

这是整个 `skills/` 目录的 **唯一推荐入口（Master / Aggregation Skill）**。

用户只需要调用本 Skill。后续由 Master 根据当前项目、任务阶段、风险和问题类型，自主选择、加载、组合和切换其他专项 Skill。

```text
User Goal
   ↓
Agent Engineering Master
   ↓
Project State Bootstrap
   ↓
识别阶段 / 风险 / 缺失决策
   ↓
按需加载专项 Skill
   ↓
执行 + 验证
   ↓
更新当前项目 .agent-engineering/
   ↓
重新路由
   ↓
直到完成
```

专项 Skill 负责某类专业工作；Master 对整个任务生命周期、一致性、状态隔离和最终验收负责。

---

# 2. Mandatory Bootstrap — 必须先确定项目状态

在加载任何专项 Skill 前，Master **必须先读取**：

```text
PROJECT-STATE-POLICY.md
SKILL-REGISTRY.md
```

然后执行：

```text
Resolve Project Root
        ↓
检查 <project>/.agent-engineering/project.yaml
        ↓
存在？
├─ 是 → 加载当前项目状态
└─ 否 → 从 ../templates/ 初始化当前项目状态
```

## 2.1 模板永远只读

`../templates/` 是共享模板库，不是 State Store。

允许：

- Read
- Copy
- Instantiate

禁止：

- 把当前项目决策写回模板；
- 把 Session State 写进模板；
- 用模板目录保存多个项目状态；
- 因为模板更新而覆盖已有项目实例。

最终规则：

```text
Template is immutable.
Project State is project-scoped.
Session State is task-scoped.
Cross-project state sharing is opt-in, never implicit.
```

## 2.2 当前项目状态目录

每个业务项目独立维护：

```text
<project>/.agent-engineering/
├─ project.yaml
├─ boundary-canvas.md
├─ decision-ledger.md
├─ current-session.md
├─ project-intake.md
├─ architecture.md
├─ change-impact.md
├─ verification-report.md
└─ history/
```

多个项目同时运行时必须形成：

```text
Project A/.agent-engineering/
Project B/.agent-engineering/
```

不得自动共享或合并状态。

## 2.3 Project Root Resolution

优先级：

1. 用户明确指定的项目目录；
2. 当前 Git Repository Root；
3. 当前工作目录中包含主要构建 / 依赖文件的根目录；
4. 只有多个候选代表不同项目且无法安全判断时，才询问用户。

禁止把 Skills 安装目录本身当业务 Project Root。

---

# 3. Core Principles

## 3.1 用户不需要知道 Skill 名称

不要要求用户自己判断：

- Greenfield 还是 Existing Modifier；
- 是否需要 RAG Skill；
- 何时进入 Security / Eval / Production；
- Multi-Agent 是否应该拆；
- Bug 应该交给 Debugger 还是 Architecture Reviewer。

这些由 Master 判断。

## 3.2 动态调用，而不是固定流水线

不要机械执行全部 Skill。

```text
当前问题是什么
→ 当前最需要哪个能力
→ 加载对应 Skill
→ 完成本阶段
→ 验证
→ 更新项目状态
→ 重新判断
→ 决定下一 Skill
```

## 3.3 边界先于框架

先确定：

- Goal Boundary
- Autonomy Boundary
- Knowledge Boundary
- Tool / Action Boundary
- Data / Permission Boundary
- State / Memory Boundary
- Multi-Agent Boundary
- Budget / Termination Boundary
- HITL Boundary
- Security Boundary
- Evaluation Boundary
- Production Boundary

再决定 LangGraph、SDK、MCP、Vector DB 等实现。

## 3.4 复杂度逐级升级

```text
Deterministic Code
→ Workflow
→ LLM Workflow
→ Single Agent
→ Agent + Tools / RAG / Memory
→ Multi-Agent
```

只有上一层明确无法满足需求时才升级。

---

# 4. Skill Registry

Master 可以按需调用：

| Skill | Path | 使用时机 |
|---|---|---|
| Guided Builder | `../agent-guided-builder/SKILL.md` | 一步步设计、边界不清、需要关键决策 |
| Project Orchestrator | `../agent-project-orchestrator/SKILL.md` | 初始任务模糊、跨领域编排 |
| Greenfield Builder | `../agent-greenfield-builder/SKILL.md` | 从 0 到 1 |
| Existing Project Modifier | `../agent-existing-project-modifier/SKILL.md` | 已有项目新增、迁移、重构 |
| Architecture Reviewer | `../agent-architecture-reviewer/SKILL.md` | 职责混乱、耦合、复杂度失控 |
| Debugger | `../agent-debugger/SKILL.md` | Tool / State / Graph / Loop / RAG 异常 |
| RAG Engineer | `../agent-rag-engineer/SKILL.md` | Retrieval、Rerank、Citation、ACL、Agentic RAG |
| Multi-Agent Designer | `../agent-multi-agent-designer/SKILL.md` | Supervisor、Handoff、并行 Worker、A2A |
| Eval Hardening | `../agent-eval-hardening/SKILL.md` | Golden Set、Trajectory、Regression、Gate |
| Security Reviewer | `../agent-security-reviewer/SKILL.md` | Injection、权限、Identity、HITL |
| Performance Optimizer | `../agent-performance-cost-optimizer/SKILL.md` | Token、Latency、Concurrency、Cost |
| Productionizer | `../agent-productionizer/SKILL.md` | Queue、Worker、Checkpoint、Deploy、SRE |

详细动态路由规则见 `SKILL-REGISTRY.md`。

---

# 5. Project-Scoped Shared State

Master 必须维护统一的 **当前项目状态**，但所有持久化只发生在：

```text
<project>/.agent-engineering/
```

至少维护：

```text
Project ID
Project Mode
Current Stage
Business Goal
In Scope
Out of Scope
Architecture
Autonomy Level
Knowledge Boundary
Tool Boundary
Permission Boundary
State / Memory Boundary
Multi-Agent Boundary
Runtime Boundary
Budget / Termination
HITL Boundary
Security Constraints
Evaluation Criteria
Production Constraints
Known Risks
Open Decisions
Completed Decisions
Current Baseline
Current Changes
Verification Status
Next Recommended Skill
```

## 5.1 文件职责

```text
project.yaml
→ 项目身份与当前阶段

boundary-canvas.md
→ 长期系统边界

decision-ledger.md
→ 长期重要架构决策

current-session.md
→ 当前任务 / 当前引导阶段的短期状态

project-intake.md
→ 项目现状、目标和约束

architecture.md
→ 当前确认架构摘要

change-impact.md
→ Blast Radius / Migration Impact

verification-report.md
→ Test / Eval / Security / Production 验证

history/
→ 已完成任务归档
```

## 5.2 状态更新路由

专项 Skill 返回后：

```text
Boundary changed
→ boundary-canvas.md

Architecture decision
→ decision-ledger.md

Current task progress
→ current-session.md

Existing project impact
→ change-impact.md

Verification evidence
→ verification-report.md

Completed task
→ history/
```

## 5.3 Session 不得无限膨胀

任务结束时：

1. 长期边界写入 `boundary-canvas.md`；
2. 长期决定写入 `decision-ledger.md`；
3. 验证结论写入 `verification-report.md`；
4. 当前任务摘要归档到 `history/`；
5. 重置或更新 `current-session.md`。

---

# 6. Master Execution Loop

每个重要阶段执行：

```text
1. OBSERVE
   当前项目和任务处于什么状态？

2. IDENTIFY GAP
   当前最关键的缺失决策 / 能力 / 故障是什么？

3. BOUNDARY CHECK
   是否触及新的权限、数据、状态、Tool、副作用或架构边界？

4. SELECT SKILL
   哪个专项 Skill 最适合当前问题？

5. LOAD MINIMALLY
   只加载当前需要的 Skill。

6. EXECUTE
   执行当前阶段。

7. VERIFY
   有什么证据证明完成？

8. UPDATE PROJECT STATE
   只更新当前项目 .agent-engineering/。

9. RE-ROUTE
   继续当前 Skill、切换 Skill，还是完成？
```

---

# 7. Guided Mode

当用户说：

- “帮我设计一个 Agent”；
- “一步一步带我做”；
- “我不知道怎么拆”；
- “帮我考虑边界”；
- “这个智能体应该怎么设计”；

优先进入 `agent-guided-builder`。

每轮最多处理 1~3 个强相关关键决策，优先给 2~5 个选项、推荐项、原因、Trade-off 和 Boundary Impact。

不要一次询问几十个问题。

如果用户明确说“直接做”，则内部完成 Boundary Canvas 和 Decision Ledger，只在不可安全推断或不可逆高风险决定时询问。

---

# 8. Greenfield Routing

新项目通常：

```text
Master
 ↓
Project State Bootstrap
 ↓
Guided Builder
 ↓
Greenfield Builder
 ↓
按需：RAG / Multi-Agent / Security / Performance
 ↓
Eval Hardening
 ↓
Productionizer
 ↓
Architecture Review
```

新项目第一次进入时创建 `.agent-engineering/`，并记录初始目标、边界和架构决策。

---

# 9. Existing Project Routing

已有项目：

```text
Master
 ↓
加载已有 .agent-engineering/（如存在）
 ↓
Existing Project Modifier
 ↓
Baseline + Invariants + Blast Radius
 ↓
按需：Debugger / Architecture / RAG / Multi-Agent / Security / Performance
 ↓
Eval Hardening
 ↓
Productionizer（如果涉及上线）
```

如果已有项目没有 `.agent-engineering/`，只初始化缺失状态文件，不修改业务代码。

禁止没有 Baseline 就做大范围改造。

---

# 10. Automatic Skill Escalation

## Security Reviewer

自动追加条件：

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

## Eval Hardening

自动追加条件：

- 修改 Prompt；
- 修改模型；
- 修改 Router；
- 修改 Tool；
- 修改 RAG；
- 修改 State；
- 修改 Multi-Agent 协作；
- 准备发布。

## Productionizer

自动追加条件：

- 长任务；
- API 服务；
- 多用户；
- Queue / Worker；
- Retry / DLQ；
- Checkpoint；
- Docker / Kubernetes；
- 高可用；
- 上生产。

## Performance Optimizer

自动追加条件：

- Token 高；
- 延迟高；
- 并发瓶颈；
- 模型成本高；
- Tool 串行；
- Context 过长。

## Architecture Reviewer

自动追加条件：

- Agent 数量持续增加；
- Shared State 混乱；
- Prompt 超大；
- Tool 数量失控；
- 模块职责重叠；
- 局部修改不断波及全系统。

---

# 11. Skill Composition

同一阶段建议：

- 1 个 Primary Skill；
- 最多 2 个 Supporting Skills。

例如：

```text
Primary: Existing Project Modifier
Support: Debugger + Eval Hardening
```

或者：

```text
Primary: RAG Engineer
Support: Security Reviewer + Eval Hardening
```

不要一次加载全部 Skill。

---

# 12. Conflict Resolution

不同 Skill 冲突时优先级：

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

任何“更优雅”的方案都不能越过安全和业务边界。

---

# 13. User Interaction Policy

不要把 Skill 调度变成用户负担。

不要频繁说“现在我要调用 XXX Skill”。对用户正常呈现为连续工程协作。

只有关键业务 / 架构决定才使用 Guided 选项式交互。

已经由用户、代码、配置、日志、测试确定的信息不得重复询问。

---

# 14. Autonomous Execution Policy

如果用户约束已经充分，或者说“直接做”，Master 应自主完成能从项目中安全推断的决策。

只有这些情况需要用户决策：

- 方案代表不同业务目标；
- 不可逆操作；
- 权限 / 合规 / 高风险；
- 无法判断 Project Root 或关键边界；
- 选择会显著改变成本、交付或用户体验。

---

# 15. Multi-Project Isolation

Master 必须假设不同 Project Root 是不同项目。

```text
Project A
└─ .agent-engineering/

Project B
└─ .agent-engineering/
```

禁止：

- A 自动继承 B 的 Decision；
- A 自动读取 B 的 Session；
- 使用一个全局可写文件存所有项目状态；
- 因项目名相似就合并状态。

只有用户明确要求跨项目比较、迁移、复用时才可以读取另一项目状态；读取不等于合并。

---

# 16. Concurrent Task Safety

同一项目可能同时有多个 Agent / 任务。

长期状态：

```text
boundary-canvas.md
decision-ledger.md
```

任务记录优先进入：

```text
history/<task-id-or-date>-<topic>.md
```

写长期状态前：

- 读取最新内容；
- 避免无条件覆盖；
- 冲突决策必须显式合并；
- 不得静默覆盖另一个任务刚写入的 Decision。

---

# 17. Verification Gate

“代码写完”不是完成。

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
Deployment Readiness（如相关）
Rollback（已有项目 / 生产变更）
```

未执行必须记录 `NOT VERIFIED`。

---

# 18. Completion Gate

只有满足以下条件才结束：

1. 用户目标已实现；
2. Scope 未被无意扩大；
3. 当前项目 Boundary Canvas 无阻塞项；
4. 关键决策进入当前项目 Decision Ledger；
5. 必要专项 Skill 已执行；
6. 功能有验证证据；
7. Agent 行为有 Eval / Test；
8. 高风险行为有安全控制；
9. 未验证项被显式记录；
10. 已有项目有兼容 / Rollback；
11. 生产项目具备最小可观测和恢复能力；
12. 项目状态已经正确写入当前 Project Root，而不是共享模板目录。

---

# 19. Anti-Patterns

禁止：

- 每个任务都加载全部 Skill；
- 把 Skill 路由变成用户负担；
- 为了“高级”强行 Multi-Agent；
- 已有项目未建立 Baseline 就重构；
- 只写代码不验证；
- 忽略 Side Effect / Permission / Identity；
- 修改 Prompt / Router 后不 Regression；
- 专项 Skill 完成后不回写项目状态；
- 新阶段静默推翻之前 Decision；
- **修改 `skills/templates/` 保存项目状态**；
- **把两个 Project Root 的 `.agent-engineering/` 混合**；
- **用全局共享 Session 文件同时服务多个项目**；
- **模板升级直接覆盖项目实例**；
- 在 `.agent-engineering/` 中记录 API Key、Token、密码或私钥。

---

# 20. One-Skill Usage Model

推荐用户或上层 Agent 只加载：

```text
skills/agent-engineering-master/SKILL.md
```

Master 的第一步永远不是直接编码，而是：

```text
读取 Project State Policy
→ Resolve Project Root
→ 加载 / 初始化当前项目 .agent-engineering/
→ 再进行动态 Skill Orchestration
```

之后由 Master 自行读取其他 `skills/*/SKILL.md`。

最终使用方式：

```text
用户
 ↓
Agent Engineering Master
 ↓
Project-Scoped State
 ↓
Dynamic Skill Orchestration
 ↓
Guided Design / Build / Modify / Debug / RAG / Multi-Agent / Eval / Security / Optimize / Production
 ↓
Verification
 ↓
Update Current Project State
 ↓
完成真实 Agent 工程任务
```
