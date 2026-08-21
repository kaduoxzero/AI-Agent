# Agent 全能工程师能力地图与学习路线

> 目标：建立完整的 Agent Engineering 心智模型，而不是只会某个框架的 API。

## 1. Agent 全能工程师是什么

Agent 全能工程师需要同时具备 **AI 能力理解 + 软件架构 + 数据工程 + 后端工程 + 安全 + 测试评估 + DevOps**。

一个生产级 Agent 系统通常不是单一 LLM，而是：

```text
Model
  + Prompt / Context
  + State / Session
  + Tools
  + RAG / Memory
  + Agent Loop
  + Workflow / Multi-Agent
  + Runtime / Harness
  + Security / HITL
  + Evaluation / Observability
  + Backend / Queue / Storage
  + Deployment / CI/CD
```

### 专业名词通义

- **Agent Engineering**：围绕 Agent 的设计、开发、评估、部署和维护形成的工程体系。
- **Runtime**：Agent 真正执行时依赖的运行环境，包括循环、状态、工具、任务、取消、恢复等能力。
- **Harness**：包裹模型的“工程外壳”，为长任务提供规划、Todo、上下文压缩、文件访问、权限审批、可观测性等能力。
- **Orchestration**：把 Agent、函数、Tool 和业务节点按一定控制流组合起来。

## 2. 能力分层

### L1：LLM 应用开发

能完成：

- 模型 API 调用；
- System Prompt；
- Structured Output；
- Streaming；
- 基本错误处理。

但此时还不能称为 Agent 工程师。

### L2：Single Agent

能完成：

```text
User
 ↓
Agent
 ↓
Model decides Action
 ↓
Tool
 ↓
Observation
 ↓
Agent
```

需要掌握：

- Tool Calling；
- Agent Loop；
- State；
- Session；
- RAG；
- 基础 Memory。

### L3：Workflow / Agentic Workflow

能够处理：

- Routing；
- Parallel；
- Retry；
- Reflection；
- Planner / Executor；
- Human Approval；
- Checkpoint。

这一级开始真正进入大型 Agent 项目。

### L4：Multi-Agent

能够回答：

- 为什么要拆 Agent？
- Agent 的职责边界是什么？
- 谁负责调度？
- State 是否共享？
- Context 如何隔离？
- Agent 之间如何通信？
- 如何防止循环委派？

### L5：Production Agent

必须掌握：

```text
Evaluation
Tracing
Security
Permissions
Sandbox
Queue
Checkpoint
Concurrency
Caching
Cost Control
CI/CD
```

### L6：Agent 全能工程师

除了搭 Agent，还要能够：

- 自己设计 Agent Runtime；
- 判断什么时候不该用 Agent；
- 设计 MCP / A2A 接入；
- 构建 Coding / Research / Data / Browser / Voice Agent；
- 设计多租户、权限与审计；
- 对大型系统进行性能和成本优化；
- 建立 Evals 驱动的迭代流程。

## 3. 推荐学习路线

### 阶段一：模型与接口

学习：

1. LLM 与 Reasoning Model；
2. Token / Context Window；
3. Sampling；
4. Structured Output；
5. Tool Calling；
6. Streaming。

完成物：一个可靠的模型调用层，而不是散落在业务代码中的 SDK 调用。

### 阶段二：Single Agent

学习：

1. Agent Loop；
2. Tool；
3. State；
4. Session；
5. Context Engineering；
6. RAG / Memory。

完成物：一个能自主选择工具、执行并校验结果的 Agent。

### 阶段三：Workflow

学习：

```text
Prompt Chaining
Routing
Parallelization
MapReduce
ReAct
Plan & Solve
Reflection
Evaluator-Optimizer
```

完成物：一个可控、可追踪、有明确终止条件的复杂工作流。

### 阶段四：Multi-Agent

学习：

```text
Supervisor
Orchestrator-Workers
Handoff
Chain-of-Experts
Debate
Voting
Blackboard
Swarm
```

完成物：一个职责明确、上下文受控的 Multi-Agent 系统。

### 阶段五：Runtime 与 Production

学习：

```text
Checkpoint
Persistence
Resume
Task Queue
Sandbox
HITL
Trace
Eval
Security
Deployment
```

完成物：一个能够连续运行、故障恢复和安全上线的 Agent Service。

## 4. 学习时必须避免的误区

### 误区一：Agent 就是 Prompt + while 循环

原型可以如此，但生产系统还需要状态、权限、停止条件、Trace、恢复、成本和评估。

### 误区二：Agent 越多越高级

Agent 数量增加会同步增加：

- Token；
- Latency；
- 状态同步难度；
- 错误传播；
- 调试复杂度。

只有职责真正独立时才应该拆 Agent。

### 误区三：所有事情都交给 LLM

这些通常应由确定性系统控制：

```text
Authentication
Authorization
金额校验
数据约束
幂等
风险硬阈值
事务
```

### 误区四：只会框架，不理解抽象

必须做到看到不同 SDK 时，能够识别：

```text
Agent
Runner
State
Tool
Handoff
Workflow
Checkpoint
Memory
Guardrail
Trace
```

只是不同框架中的不同命名。

## 5. 毕业标准

学完整套知识库后，至少能够独立完成以下设计题：

> 构建一个企业级 Research + RAG + Data Multi-Agent 平台。用户提交长任务后，Planner 拆解任务，Research Worker 并行搜索，Data Worker 查询数据库，RAG Worker 查询内部文档，Evaluator 校验结果；高风险 Tool 需要人工审批；任务可以暂停恢复；全链路有 Trace；部署为可水平扩展的异步 Worker 集群。

如果能够说明其中的 State、Context、Tool、Queue、Checkpoint、权限、Eval、成本、安全与故障处理，并实现主要代码，就达到了本知识库的目标。
