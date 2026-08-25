---
name: agent-guided-builder
version: 1.1.0
description: Guide a user step by step through designing or reshaping an Agent system. Use when the user wants to build an Agent from zero, is unsure about architecture or boundaries, wants interactive choices, or needs help deciding autonomy, tools, RAG, memory, Multi-Agent, permissions, runtime, evaluation, and production constraints before implementation.
---

# Agent Guided Builder

## Objective

把 Agent 设计从“用户说一句需求，模型直接开写”改造成一个 **可交互、分阶段、有决策记录、有边界检查、有阶段门禁（Stage Gate）** 的工程工作坊。

这个 Skill 的目标不是替用户做所有决定，而是让 Agent：

1. 识别当前真正缺失的关键决策；
2. 用开发人员能快速选择的方式给出 2~5 个选项；
3. 明确推荐项及原因；
4. 解释每个选择会增加什么复杂度、成本、权限和故障面；
5. 用户做出关键选择后再进入下一阶段；
6. 把所有决定持续记录到 Decision Ledger；
7. 把系统边界持续维护在 Agent Boundary Canvas；
8. 最终把决策转化为可执行的实现计划，再进入编码。

---

# 1. Default Interaction Mode

除非用户已经给出了足够完整的工程约束，否则默认进入 **Guided Workshop Mode**。

不要一开始连续抛出 20 个问题。

每次只处理 **一个决策阶段**，最多同时询问 1~3 个强相关问题。

推荐交互格式：

```text
当前阶段：Tool / Action Boundary

为什么现在要决定：
Agent 是否允许执行写操作会直接影响权限、HITL、审计和恢复设计。

请选择：
A. 只读 Tool
B. 允许低风险写操作
C. 允许高风险业务操作，但必须人工审批
D. 完全自治执行

推荐：C
原因：业务需要执行动作，但高影响操作不应直接交给模型。

这个选择会带来：
- Tool Scope
- Idempotency
- Audit Event
- HITL
- Rollback

请回复 A/B/C/D，或者直接描述你的约束。
```

## Interaction Rules

1. **优先给选项，不优先给大段开放题。**
2. 每个关键选择都提供一个推荐项，但必须说明为什么。
3. 不重复询问用户已经提供过的信息。
4. 能从现有仓库、配置、代码、日志推断的信息，先读取再判断。
5. 普通实现细节可以由 Agent 自主决定；架构、权限、破坏性行为、成本等级等关键决策必须显式暴露。
6. 用户说“你帮我选”时，Agent 可以选择推荐项，并记录为 `Agent Recommended Decision`。
7. 用户说“直接做”时，不再逐项打断，但仍必须内部完成 Boundary Canvas 和 Decision Ledger，再执行。
8. 不为了互动而互动；已明确的决策直接标记 `Resolved`。

---

# 2. Two Guidance Modes

## Mode A — Greenfield Workshop

用于从 0 到 1。

路由：

```text
agent-guided-builder
  ↓
完成关键设计决策
  ↓
agent-greenfield-builder
  ↓
专项 Skill
  ↓
实现 + Eval + Production
```

## Mode B — Existing Project Change Workshop

用于半路接手、重大改造或用户不知道该怎么改。

路由：

```text
读取现有项目
  ↓
建立 Baseline
  ↓
agent-guided-builder（只讨论未决的变化）
  ↓
确认 Change Boundary
  ↓
agent-existing-project-modifier
```

Existing Project 模式禁止重新询问已经能从代码中得到的事实。

---

# 3. Agent Boundary Canvas

整个引导过程中持续维护统一 **15 类 Agent Boundary Canvas**（权威模板：`../templates/agent-boundary-canvas.md`）。

```text
1. Goal Boundary          做什么 / 不做什么
2. User Boundary          谁使用 / 谁不能使用
3. Input Boundary         Agent 能接收什么输入
4. Output Boundary        输出什么 Artifact / Contract
5. Autonomy Boundary      哪些决定可由 Agent 自主完成
6. Knowledge Boundary     可以访问哪些知识和数据
7. Tool / Capability Boundary   可以调用哪些 Tool、有什么副作用
8. Data & Permission Boundary   User / Agent / Tool 各自权限与数据边界
9. State / Session / Memory / Checkpoint   什么保存、保存多久、谁可读取
10. Multi-Agent Boundary  是否拆分 Agent、如何协作
11. Time / Budget Boundary   Step / Token / Cost / Timeout / Retry
12. Safety & HITL Boundary   哪些情况必须停下并交给人
13. Failure Boundary      失败、恢复、回滚、降级和终止
14. Evaluation Boundary   如何评测输出、轨迹与安全
15. Observability Boundary   生产后必须能看到什么
```

设计完成前不要求每个边界都复杂，但每个边界都必须被明确判断为：

```text
Required
Not Required
Deferred
Unknown
```

不能让某个重要边界因为“没想到”而缺失。

---

# 4. Decision Ledger

每完成一个关键决策就记录：

```text
Decision ID:
Topic:
Status: Proposed / Accepted / Rejected / Deferred
Options Considered:
Decision:
Why:
Trade-offs:
New Risks:
Affected Components:
Verification:
```

例如：

```text
Decision ID: D-006
Topic: Multi-Agent
Status: Accepted
Options: Single Agent / Supervisor + Workers / Swarm
Decision: Single Agent
Why: 当前只有一类 Tool 与共享 Context，没有真正职责隔离。
Trade-offs: Prompt 会稍长，但系统复杂度和 Trace 成本更低。
New Risks: Prompt 继续增长后可能需要拆分。
Verification: Prompt/Tool 数量增长后重新执行 Architecture Review。
```

---

# 5. Step-by-Step Guided Workflow

## Stage 0 — Problem Framing

### Goal

先确定要解决的是一个真实业务问题，而不是“我想用 Agent”。

需要得到：

```text
Actor
Problem
Desired Outcome
Trigger
Current Manual Process
Success Signal
```

### 引导问题

优先让用户选择任务类型：

```text
A. 问答 / 知识助手
B. 研究 / 分析
C. 数据处理 / SQL / Python
D. 代码开发 / Coding Agent
E. 浏览器 / Computer Use
F. 业务流程自动化
G. 长任务 / Proactive Agent
H. 其他
```

### Boundary Check

明确：

- Agent 的最终业务结果是什么？
- 明确不属于这个 Agent 的职责是什么？

### Stage Gate

必须形成一句：

> 该 Agent 为【谁】在【什么触发条件】下完成【什么结果】，但不负责【明确排除项】。

---

## Stage 1 — Success, Failure and Acceptance

在讨论技术栈之前定义完成标准。

引导用户确定：

```text
正确结果是什么？
错误结果是什么？
什么错误可以接受？
什么错误绝对不能发生？
```

给出选项：

```text
质量优先
速度优先
成本优先
安全优先
平衡
```

如果业务是高风险操作，默认推荐安全优先。

### Stage Gate

至少得到：

- Task Success；
- Critical Failure；
- 1~3 个主要质量指标。

---

## Stage 2 — Need Agent or Not

Agent 必须主动挑战“Agent 假设”。

按照统一复杂度阶梯判断：

```text
Deterministic Code
→ State Machine
→ Deterministic Workflow
→ LLM Workflow
→ Single Agent
→ Agent + Tools / RAG / Memory
→ Multi-Agent
```

必须回答：

> 为什么上一层不足以解决当前问题？

如果 Workflow 已足够，不允许为了技术炫耀升级成 Agent。

### 推荐选项

```text
A. 普通程序 / 规则
B. Workflow + LLM 节点
C. Single Agent
D. Multi-Agent
```

### Stage Gate

记录 Architecture Level 和升级理由。

---

## Stage 3 — Autonomy Boundary

这是 Agent 设计最重要的边界之一。

将决策拆成：

```text
Agent 可以自主决定：
- 是否检索
- 调哪个 Tool
- 调用顺序
- 是否重试
- 是否拆任务

Agent 不可以自主决定：
- 权限策略
- 数据访问 Scope
- 高风险业务审批
- 无限增加预算
- 绕过安全规则
```

让用户选择自治等级：

```text
A0  无自治：固定 Workflow
A1  低自治：有限 Router / Tool Choice
A2  中自治：动态计划与 Tool 调度
A3  高自治：长任务自主执行，但有 Budget/HITL
A4  极高自治：跨系统主动操作
```

默认不要推荐 A4。

### Stage Gate

形成 `Autonomy Contract`。

---

## Stage 4 — Knowledge Boundary

判断是否需要 RAG、Web、数据库或 Memory。

按来源分类：

```text
Model Knowledge
Enterprise Knowledge Base
Operational Database
Web / External Source
User Files
Memory
```

逐项决定：

- 可读吗？
- 谁可读？
- 是否需要 Tenant Filter？
- 是否可信？
- 是否必须 Citation？
- 是否允许写入长期 Memory？

### 推荐决策问题

```text
企业文档是否需要引用来源？
A. 不需要
B. 推荐引用
C. 必须可追溯引用
```

企业场景默认推荐 C。

---

## Stage 5 — Tool and Side-Effect Boundary

列出需要的 Tool，并逐个分类：

```text
Read-only
Write
Destructive
External Communication
Financial / Medical / Security Sensitive
```

每个 Tool 必须确定：

```text
Input Schema
Output Schema
Permission Scope
Timeout
Retry
Idempotency
Side Effect
Audit
HITL
```

引导用户选择写权限模型：

```text
T0 只读
T1 低风险写操作
T2 高风险写操作需要 Approval
T3 高风险自动执行
```

默认生产系统优先 T2，而不是 T3。

### Stage Gate

形成 Tool Capability Matrix。

---

## Stage 6 — State, Session, Memory and Checkpoint

必须先解释四者区别：

- **State**：当前任务运行状态；
- **Session**：一次用户交互上下文；
- **Memory**：跨任务长期信息；
- **Checkpoint**：为了 Resume 保存的执行快照。

引导判断：

```text
任务是否跨分钟/小时？
是否需要断点恢复？
是否需要跨会话记住用户？
哪些数据禁止长期保存？
Memory 是否有 TTL？
```

如果只是短任务，不要强行引入长期 Memory。

---

## Stage 7 — Multi-Agent Boundary

默认从 Single Agent 开始。

只有出现以下明确边界之一才推荐拆 Agent：

```text
不同权限
不同 Context
不同 Tool Set
独立专业职责
可并行的大任务
独立 Reviewer / Critic
独立生命周期
不同模型能力
```

引导问题：

> 如果把两个候选 Agent 合并，它们会在哪个边界上产生真实冲突？

如果回答不出来，通常不应该拆。

可选架构：

```text
A. Single Agent
B. Supervisor + Workers
C. Handoff
D. Pipeline / Chain-of-Experts
E. Debate / Voting
F. Blackboard
G. Swarm
```

每个选择必须解释通信 Contract、State Ownership 与失败传播方式。

---

## Stage 8 — Runtime and Reliability Boundary

判断任务运行形态：

```text
同步短请求
流式短任务
异步长任务
Event-Driven
Scheduled / Proactive
```

长任务必须引导用户考虑：

```text
Task Store
Queue
Worker
Checkpoint
Resume
Cancellation
Retry
DLQ
Event Stream
Artifact Store
```

### Budget Canvas

至少确认：

```text
Max Steps
Max Model Calls
Max Tool Calls
Max Retry
Timeout
Token Budget
Cost Budget
```

---

## Stage 9 — Identity, Permission, Security and HITL

必须回答：

```text
用户是谁？
Agent 代表谁？
Tool 使用谁的权限？
Credential 如何获取？
Tenant 如何隔离？
哪些输入属于不可信数据？
哪些操作需要人批准？
```

高风险场景主动提醒：

- Prompt Injection；
- Indirect Prompt Injection；
- Tool Poisoning；
- Memory Poisoning；
- Excessive Agency；
- Cross-Tenant Data Leak；
- Secret Leakage。

### HITL 决策

```text
Approve
Reject
Edit
Escalate
Timeout
```

HITL 不是只有“确认按钮”，还必须定义超时后怎么办。

---

## Stage 10 — Evaluation Boundary

不要等代码写完才讨论 Eval。

引导用户确定：

```text
最终答案怎么评？
Tool 路径怎么评？
RAG Evidence 怎么评？
安全怎么评？
成本和延迟怎么评？
```

至少建立：

```text
Golden Cases
Failure Cases
Security Cases
Trajectory Rules
Regression Gate
```

---

## Stage 11 — Observability and Operations

确认生产后需要看到什么：

```text
Task ID
Trace ID
Agent Version
Prompt Version
Model Route
Tool Call
Event
Latency
Token
Cost
Error Category
Approval
Artifact
```

如果出现问题却无法回答“这个 Agent 为什么这么做”，可观测性设计不合格。

---

## Stage 12 — Architecture Freeze

在编码前生成最终决策摘要：

```text
Problem Statement
Architecture Level
Agent Responsibilities
Out of Scope
Autonomy Contract
Knowledge Sources
Tool Capability Matrix
State / Memory Model
Multi-Agent Decision
Runtime Model
Permission Model
HITL Rules
Budget
Eval Plan
Observability Plan
Deployment Target
```

让用户确认或允许 Agent 按推荐项继续。

如果用户已经说“后续不用问我，直接做”，则自动采用推荐项并记录。

---

## Stage 13 — Incremental Build

Architecture Freeze 后进入 `agent-greenfield-builder` 或 `agent-existing-project-modifier`。

推荐增量：

```text
M1 Contracts
M2 Happy Path
M3 Tool / RAG
M4 State / Persistence
M5 Runtime / Worker
M6 Failure Handling
M7 HITL / Security
M8 Eval
M9 Observability
M10 Deployment
```

每个 Milestone 必须有可运行验收，不要一次写完整个平台再统一调试。

---

# 6. Boundary Challenge Questions

Agent 在设计过程中应主动使用这些问题挑战方案：

```text
如果模型做错了，最坏会发生什么？
如果 Tool 被调用两次会怎样？
如果任务执行一半 Worker 崩溃会怎样？
如果上下文里出现恶意指令会怎样？
如果用户没有权限但知道对象 ID 会怎样？
如果模型无限循环会怎样？
如果 Token / Cost 超预算会怎样？
如果 RAG 返回错误证据会怎样？
如果 Memory 被污染会怎样？
如果两个 Agent 同时写 Shared State 会怎样？
如果人工审批一直没人处理会怎样？
如果新 Agent Version 发布后质量下降怎么回滚？
```

这些不是高级附加项，而是大型 Agent 项目的基本边界问题。

---

# 7. Option Design Rules

提供选项时：

1. 2~5 个选项即可；
2. 按复杂度从低到高排列；
3. 标明推荐项；
4. 标明“为什么不用更复杂方案”；
5. 说明关键 Trade-off；
6. 允许用户填写自定义选项。

禁止这种无帮助问题：

> 你对 Agent 有什么要求？

应该改成：

> 这个 Agent 对真实系统的操作权限更接近哪种？
> A 只读；B 低风险写；C 高风险需审批；D 高风险自治。推荐 C，因为……

---

# 8. Stop and Escalation Conditions

遇到以下情况不要继续盲目推进：

- 业务目标和成功标准互相冲突；
- 用户要求的自治等级超过当前安全能力；
- 需要高风险操作但没有 Identity / Approval / Rollback；
- Multi-Agent 拆分没有明确边界；
- 长任务没有持久化和恢复设计；
- 生产发布没有 Eval Gate；
- Existing Project 的实际代码与用户描述冲突。

此时应明确指出冲突，给出可选解决方案，再进入下一阶段。

---

# 9. Required Session Artifacts

一次完整 Guided Workshop 最终应得到：

- `Agent Boundary Canvas`
- `Decision Ledger`
- `Architecture Decision Summary`
- `Tool Capability Matrix`
- `Autonomy Contract`
- `State / Memory Model`
- `Runtime Budget`
- `Eval Plan`
- `Implementation Milestones`

这些可以保存在项目文档中，也可以作为后续 Agent 的上下文输入。

---

# 10. Report Back to Master

阶段完成或切换 Skill 时，按 `../agent-engineering-master/SKILL-REGISTRY.md` 的 Return Contract 返回：

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

长期边界与决策由 Master 按 State Write Routing 写入当前项目 `.agent-engineering/boundary-canvas.md` 与 `decision-ledger.md`。

---

# 11. Completion Criteria

Guided Builder 只有在以下条件满足后才算结束：

1. 用户知道系统为什么需要或不需要 Agent；
2. Agent 的职责与 Out-of-Scope 已明确；
3. 自治边界已明确；
4. Tool / Knowledge / Data 权限已明确；
5. State / Memory / Checkpoint 已判断；
6. Multi-Agent 是否需要已有明确理由；
7. Budget / Termination 已定义；
8. HITL / Security 已定义；
9. Eval 和验收标准已定义；
10. 已形成可执行 Milestone，并切换到实际 Builder / Modifier Skill。
