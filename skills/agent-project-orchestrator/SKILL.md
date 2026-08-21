---
name: agent-project-orchestrator
description: Route Agent engineering work to the correct workflow and decide whether an interactive guided design session is required before coding. Use when a request may involve greenfield Agent development, modification of an existing Agent project, debugging, architecture review, RAG, Multi-Agent, evaluation, security, productionization, or performance/cost optimization.
---

# Agent Project Orchestrator

## Objective

把“帮我做一个智能体 / 帮我改这个 Agent / 带我一步步设计 / 这个项目有问题”转换成明确、可执行、可验收的工程任务，并选择正确的专项 Skill。

Orchestrator 负责三件事：

1. 判断当前是 Greenfield、Existing Project、Bug、Architecture 还是专项工程问题；
2. 判断是否应先进入 **Guided Workshop**；
3. 选择 1 个主 Skill + 必要的辅助 Skill。

它不应该自己取代专项 Skill。

## Guided Workshop Trigger

出现以下任一情况，优先进入 `agent-guided-builder`：

- 用户说“带我一步一步做”；
- 用户不知道 Agent 边界怎么考虑；
- 用户只有业务想法，没有架构决策；
- 用户不确定 Workflow / Single Agent / Multi-Agent；
- 用户不确定 RAG / Memory / Tool / HITL 是否需要；
- 新项目会执行真实业务动作；
- 已有项目准备进行大规模能力升级，但 Change Boundary 尚不明确；
- 用户明确希望 Agent 给出选项并帮助做取舍。

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

## Routing Decision

```text
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

- 知识库、检索、Embedding、Rerank、引用 → `agent-rag-engineer`
- Supervisor、Handoff、Debate、Swarm、多个 Agent → `agent-multi-agent-designer`
- 测试、Benchmark、Regression、稳定性 → `agent-eval-hardening`
- Prompt Injection、Tool 越权、Identity、HITL → `agent-security-reviewer`
- Docker、Queue、Worker、Checkpoint、SRE、上线 → `agent-productionizer`
- Token、延迟、并发、模型成本 → `agent-performance-cost-optimizer`

## Architecture Escalation Rule

只有上一层无法有效解决问题时才升级复杂度：

```text
Function / Rule
  ↓
State Machine
  ↓
Deterministic Workflow
  ↓
LLM Workflow
  ↓
Single Agent
  ↓
Agent + RAG / Tools / Memory
  ↓
Multi-Agent
```

每次升级都需要回答：

- 新复杂度解决了哪个明确问题？
- 为什么上一层做不到？
- 新增了什么 State / Context / Permission？
- 新增了什么延迟和成本？
- 新增了什么故障面？
- 如何测试新增复杂度？

## Boundary First Rule

Agent 项目开始前至少检查：

```text
Goal Boundary
Autonomy Boundary
Knowledge Boundary
Tool / Side-Effect Boundary
Permission Boundary
State / Memory Boundary
Multi-Agent Boundary
Time / Cost Boundary
Safety / HITL Boundary
Failure / Recovery Boundary
Eval Boundary
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

## Intake Workflow

### 1. 识别任务类型

记录：

- Greenfield / Existing Project
- Feature / Bug / Refactor / Migration / Performance / Security / Production
- Guided / Direct Execution
- 是否需要 RAG
- 是否需要 Tools
- 是否需要 Memory
- 是否可能 Multi-Agent
- 是否涉及高风险 Action

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

### 3. 建立 Done Definition

至少覆盖：

- 功能结果；
- 代码结果；
- 测试结果；
- Eval 结果；
- 兼容性结果；
- 安全结果；
- 文档 / 配置结果。

### 4. 选择 Skill 组合

一个任务通常只加载：

- 1 个主 Skill；
- 1~3 个辅助 Skill。

不要一次把所有 Skill 都放入上下文。

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

## Stop Conditions

出现以下情况必须停止扩大改动：

- 修改开始触及原目标之外的大量模块；
- 基础架构假设与实际代码完全不一致；
- 现有测试大面积失败且与当前改动无关；
- 需要破坏公开 API / 数据格式 / 数据库兼容性；
- 高风险不可逆操作没有恢复方案；
- 用户选择的自治范围超过当前安全边界；
- Multi-Agent 没有可解释的职责 / 权限 / Context 边界。

## Completion Criteria

Orchestrator 完成的标志：

- 已判断是否需要 Guided Workshop；
- 已明确主执行 Skill；
- 已识别项目现状与目标；
- 已锁定主要约束；
- 已定义或安排定义边界；
- 已定义验收标准；
- 已进入真正的设计、实现或验证流程。
