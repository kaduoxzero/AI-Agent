---
name: agent-project-orchestrator
version: 1.2.0
description: Route Agent engineering work to the correct workflow and decide whether an interactive guided design session is required before coding. Use when a request may involve greenfield Agent development, modification of an existing Agent project, debugging, architecture review, project handover/takeover, RAG, Multi-Agent, evaluation, security, productionization, or performance/cost optimization.
---

# Agent Project Orchestrator

## Objective

把“帮我做一个智能体 / 帮我改这个 Agent / 带我一步步设计 / 这个项目有问题 / 帮我交接或接手这个项目”转换成明确、可执行、可验收的工程任务，并选择正确的专项 Skill。

Orchestrator 负责三件事：

1. 判断当前是 Greenfield、Existing Project、Bug、Architecture、Handover 还是专项工程问题；
2. 判断是否应先进入 **Guided Workshop**；
3. 选择 1 个主 Skill + 必要的辅助 Skill。

它不应该自己取代专项 Skill。

## Guided Workshop Trigger

出现以下任一情况，优先进入 `agent-guided-builder`：

- 需求模糊、不完整或多方案歧义（先经 `agent-grill-me` 澄清，再决定是否需要引导式架构设计）；
- 用户说“带我一步一步做”；
- 用户不知道 Agent 边界怎么考虑；
- 用户只有业务想法，没有架构决策；
- 用户不确定 Workflow / Single Agent / Multi-Agent；
- 用户不确定 RAG / Memory / Tool / HITL 是否需要；
- 新项目会执行真实业务动作；
- 已有项目准备进行大规模能力升级，但 Change Boundary 尚不明确；
- 用户明确希望 Agent 给出选项并帮助做取舍。

交接任务例外：如果用户意图明确是“项目交接 / 接手 / ownership transfer”，优先进入 `agent-enterprise-handover` 做 Scope Freeze 与 Asset Discovery；只有交接范围本身存在关键歧义时，才使用 `agent-grill-me`。不要因为交接内容很多就自动进入 Guided Builder。

如果用户已经给出了完整目标、边界和技术约束，或者明确说“不要再问，直接做”，可以不进入逐项交互；但仍必须内部完成 Boundary Canvas 与 Decision Ledger。

## Non-Negotiable Rules

1. 不要因为用户说“Agent”就默认使用自治 Agent。
2. 不要因为用户说“高级”就默认使用 Multi-Agent。
3. 已有项目在读取代码和配置前，不允许提出大规模重写方案。
4. 不能把“能运行”当成“完成”；必须定义验收条件。
5. 不要为了套 Skill 扩大用户原始目标。
6. 优先使用已有项目的技术栈、约定、目录和依赖。
7. 缺失信息可通过仓库、配置、测试、日志直接推断时，不反复询问用户。
8. 关键架构决策要暴露 Trade-off；普通实现细节不用打断用户。
9. Guided Mode 每轮只推进一个主要决策阶段。
10. 用户已回答的信息必须进入 Decision Ledger，不能后续重复询问。
11. 交接任务不能把“生成文档”当成“完成交接”；必须至少审查资产、运行、验证、风险和 Ownership。
12. 对交接口述信息要区分 VERIFIED / DOCUMENTED / REPORTED / INFERRED / UNKNOWN，不能把推测写成事实。

## Routing Decision

```text
是否明确是项目交接 / 接手 / 移交 / takeover？
├─ 是 → agent-enterprise-handover
└─ 否
   ↓
需求清晰且完整？
├─ 否（模糊 / 不完整 / 多方案歧义）→ agent-grill-me
│        ↓
│        澄清后重新评估
└─ 是
   ↓
用户是否需要“引导式设计”？
├─ 是 → agent-guided-builder
│        ↓
│        决策完成后继续路由
└─ 否
   ↓
是否已有项目？
├─ 否 → agent-greenfield-builder
└─ 是
   ↓
   新增 / 修改 / 迁移 / 重构？
   ├─ 是 → agent-existing-project-modifier
   └─ 否
      ↓
      故障或异常行为？
      ├─ 是 → agent-debugger
      └─ 否
         ↓
         架构问题？
         ├─ 是 → agent-architecture-reviewer
         └─ 按领域路由
```

领域路由：

- 需求澄清、边界探索、高价值决策取舍 → `agent-grill-me`
- 项目交接、项目接手、Ownership Transfer、离职/轮岗移交、交接审计 → `agent-enterprise-handover`
- 知识库、检索、Embedding、Rerank、引用 → `agent-rag-engineer`
- Supervisor、Handoff、Debate、Swarm、多个 Agent → `agent-multi-agent-designer`
- 测试、Benchmark、Regression、稳定性 → `agent-eval-hardening`
- Prompt Injection、Tool 越权、Identity、HITL → `agent-security-reviewer`
- Docker、Queue、Worker、Checkpoint、SRE、上线 → `agent-productionizer`
- Token、延迟、并发、模型成本 → `agent-performance-cost-optimizer`

## Architecture Escalation Rule

只有上一层无法有效解决问题时才升级复杂度。统一复杂度阶梯：

```text
Deterministic Code
→ State Machine
→ Deterministic Workflow
→ LLM Workflow
→ Single Agent
→ Agent + Tools / RAG / Memory
→ Multi-Agent
```

每次升级都需要回答：

- 新复杂度解决了哪个明确问题？
- 为什么上一层做不到？
- 新增了什么 State / Context / Permission？
- 新增了什么延迟和成本？
- 新增了什么故障面？
- 如何测试新增复杂度？

## Boundary First Rule

Agent 项目开始前至少检查统一 **15 类 Agent Boundary Canvas**（权威模板：`../templates/agent-boundary-canvas.md`）：

```text
Goal / User / Input / Output / Autonomy / Knowledge /
Tool & Capability / Data & Permission /
State-Session-Memory-Checkpoint / Multi-Agent /
Time & Budget / Safety & HITL / Failure /
Evaluation / Observability
```

如果边界未知，不代表必须全部询问用户。

处理优先级：

```text
已有信息
→ 仓库可推断
→ 安全默认值
→ Agent 推荐
→ 用户关键决策
```

交接任务额外检查：

```text
Handover Scope / Out of Scope
Current Owner / Target Owner
Assets
Runtime Operability
Permissions
Known Issues / Risks
Evidence Level
Acceptance Gates
```

## Intake Workflow

### 1. 识别任务类型

记录：

- Greenfield / Existing Project / Handover / Takeover
- Feature / Bug / Refactor / Migration / Performance / Security / Production
- Guided / Direct Execution
- 是否需要 RAG
- 是否需要 Tools
- 是否需要 Memory
- 是否可能 Multi-Agent
- 是否涉及高风险 Action
- 是否涉及 Ownership Transfer / Reverse Shadow

### 2. 识别不可变约束

优先从用户和仓库中提取：

- 语言和框架；
- 模型 Provider；
- 数据库 / Queue / Vector DB；
- 部署方式；
- API Contract；
- 已有业务行为；
- 兼容性要求；
- 资源限制；
- 安全要求。

交接任务还需识别：

- 当前交接范围；
- 哪些环境在范围内；
- 当前 Owner 与目标 Owner；
- 是否需要 Production / Release / Rollback 交接；
- 是否存在接手验收要求。

### 3. 建立 Done Definition

至少覆盖：

- 功能结果；
- 代码结果；
- 测试结果；
- Eval 结果；
- 兼容性结果；
- 安全结果；
- 文档 / 配置结果。

交接任务的 Done Definition 必须额外覆盖：

- Asset Ready；
- Runtime Ready；
- Operations Ready；
- Ownership Ready；
- Reverse Shadow / Acceptance Gate。

### 4. 选择 Skill 组合

一个任务通常只加载：

- 1 个主 Skill；
- 1~3 个辅助 Skill 的候选集合；
- 任一时刻实际 Supporting Skill 不超过 Master Registry 规定的上限。

不要一次把所有 Skill 都放入上下文。

`agent-enterprise-handover` 属于聚合型 Primary Skill：它可以顺序调用 Architecture、Existing Project、Evaluation、Security、Production 等专项能力，专项完成后必须回到 Handover 聚合证据并继续 Gate 验收。

## Guided Conversation Contract

如果使用 `agent-guided-builder`，每次用户交互应尽量采用：

```text
当前阶段：
为什么要决定：

A. ...
B. ...
C. ...

推荐：B
原因：
Trade-off：
Boundary Impact：

请选择 A/B/C，或者直接告诉我你的约束。
```

不要一次问十几个散乱问题。

## Standard Internal Summary

```text
Task Type:
Guidance Mode:
Primary Skill:
Supporting Skills:
Current Baseline:
Target State:
Resolved Decisions:
Open Decisions:
Constraints:
Boundary Risks:
Verification Required:
```

交接任务增加：

```text
Handover Mode:
Handover Scope:
Current Owner:
Target Owner:
Evidence Status:
Critical Gaps:
Acceptance Required:
```

## Stop Conditions

出现以下情况必须停止扩大改动：

- 修改开始触及原目标之外的大量模块；
- 基础架构假设与实际代码完全不一致；
- 现有测试大面积失败且与当前改动无关；
- 需要破坏公开 API / 数据格式 / 数据库兼容性；
- 高风险不可逆操作没有恢复方案；
- 用户选择的自治范围超过当前安全边界；
- Multi-Agent 没有可解释的职责 / 权限 / Context 边界。

交接任务出现以下情况时停止“宣布完成”，转为 `INCOMPLETE / BLOCKED`：

- 核心 Repository 无法访问；
- 接手人无法启动项目；
- 关键资产只存在原负责人本地；
- Production Owner / Release / Rollback 不明确；
- 关键权限未移交；
- Reverse Shadow 的关键项无法完成。

## Report Back to Master

路由完成后，按 `../agent-engineering-master/SKILL-REGISTRY.md` 的 Return Contract 返回，至少包含 Primary Skill、Supporting Skills 与 Standard Internal Summary 中的关键信息。

交接任务若路由到 `agent-enterprise-handover`，还必须返回 Handover Mode、Scope、Evidence Summary、Critical Gaps、Acceptance Gates 与 Next Exact Action。

---

## Completion Criteria

Orchestrator 完成的标志：

- 已判断是否需要 Guided Workshop；
- 已明确主执行 Skill；
- 已识别项目现状与目标；
- 已锁定主要约束；
- 已定义或安排定义边界；
- 已定义验收标准；
- 交接任务已识别 Ownership Transfer 与 Acceptance 要求；
- 已进入真正的设计、实现、交接或验证流程。
