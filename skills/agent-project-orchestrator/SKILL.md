---
name: agent-project-orchestrator
description: Route Agent engineering work to the correct workflow. Use when a request may involve greenfield Agent development, modification of an existing Agent project, debugging, architecture review, RAG, Multi-Agent, evaluation, security, productionization, or performance/cost optimization and the correct execution path must be chosen before coding.
---

# Agent Project Orchestrator

## Objective

把模糊的“帮我做一个智能体 / 帮我改这个 Agent / 这个项目有问题”转换成明确、可执行、可验收的工程任务，并选择正确的专项 Skill。

这个 Skill 负责 **判断与编排**，不应该取代专项 Skill 的详细执行流程。

## When To Use

出现以下任一情况时使用：

- 用户要求从 0 到 1 构建 Agent，但需求还没有落成工程边界；
- 用户给出一个已有 Agent 项目，要求新增、重构、迁移或修复；
- 用户只描述结果，没有说明是 RAG、Workflow、Single Agent 还是 Multi-Agent；
- 同一个任务同时涉及架构、代码、RAG、Eval、安全、生产部署等多个领域；
- 当前 Agent 不确定下一步应该读代码、查日志、画架构、写测试还是直接实现。

## Non-Negotiable Rules

1. 不要因为用户说“Agent”就默认使用自治 Agent。
2. 不要因为用户说“高级”就默认使用 Multi-Agent。
3. 已有项目在读取代码和配置前，不允许提出大规模重写方案。
4. 不能把“能运行”当成“完成”；必须定义验收条件。
5. 不要为了套 Skill 而扩大用户原始目标。
6. 优先使用已有项目的技术栈、约定、目录和依赖。
7. 缺失信息可通过仓库、配置、测试、日志直接推断时，不反复询问用户。
8. 只有真正阻塞实现且无法从项目中推断的信息才需要询问。

## Routing Decision

按以下顺序判断：

```text
是否已有项目？
├─ 否 → agent-greenfield-builder
└─ 是
   ↓
   是“新增 / 修改 / 迁移 / 重构”吗？
   ├─ 是 → agent-existing-project-modifier
   └─ 否
      ↓
      是故障或异常行为吗？
      ├─ 是 → agent-debugger
      └─ 否
         ↓
         是架构问题吗？
         ├─ 是 → agent-architecture-reviewer
         └─ 继续按领域路由
```

领域路由：

- 知识库、检索、Embedding、Rerank、引用 → `agent-rag-engineer`
- Supervisor、Handoff、Debate、Swarm、多个 Agent → `agent-multi-agent-designer`
- 测试、Benchmark、Regression、稳定性 → `agent-eval-hardening`
- Prompt Injection、Tool 越权、Identity、HITL → `agent-security-reviewer`
- Docker、Queue、Worker、Checkpoint、SRE、上线 → `agent-productionizer`
- Token、延迟、并发、模型成本 → `agent-performance-cost-optimizer`

## Architecture Escalation Rule

只有满足上一层无法有效解决问题时，才升级复杂度：

```text
普通函数 / Rule
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
- 新增了什么状态、权限、延迟、成本和故障面？

## Intake Workflow

### 1. 识别任务类型

记录：

- Greenfield / Existing Project
- Feature / Bug / Refactor / Migration / Performance / Security / Production
- 是否需要 RAG
- 是否需要 Tools
- 是否需要 Memory
- 是否需要 Multi-Agent
- 是否需要 Human Approval

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

### 3. 定义 Done

任务开始前至少建立以下完成标准：

- 功能结果；
- 代码结果；
- 测试结果；
- Eval 结果；
- 兼容性结果；
- 安全结果；
- 文档 / 配置结果。

### 4. 选择 Skill 组合

一个任务最多指定：

- 1 个主 Skill；
- 1~3 个辅助 Skill。

不要一次把所有 Skill 都加载进上下文。

## Standard Output Contract

Orchestrator 应生成内部执行摘要：

```text
Task Type:
Primary Skill:
Supporting Skills:
Current Baseline:
Target State:
Constraints:
Risk Areas:
Verification Required:
```

然后直接进入专项 Skill 执行。

## Stop Conditions

出现以下情况必须暂停继续扩大改动：

- 修改开始触及原目标之外的大量模块；
- 发现基础架构假设与实际代码完全不一致；
- 现有测试大面积失败且与当前改动无关；
- 需要破坏公开 API / 数据格式 / 数据库兼容性；
- 涉及高风险不可逆操作而没有恢复方案。

此时应缩小改动、建立 Migration / Compatibility Plan，而不是继续强推。

## Completion Criteria

Orchestrator 完成的标志不是写出方案，而是：

- 已明确主执行 Skill；
- 已识别项目现状与目标；
- 已锁定主要约束；
- 已定义验收标准；
- 已进入实际实现或验证流程。
