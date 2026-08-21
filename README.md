# AI Agent 全能工程师知识库

> 面向有一定 AI 与软件开发基础的开发人员。目标不是“会调用一个 Agent 框架”，而是能够从 0 到 1 设计、实现、评估、部署并维护真实的大型 Agent / Multi-Agent 系统。

## 学完应具备的能力

完成本知识库后，应能够独立完成：

- 根据业务复杂度选择 LLM、Workflow、Single Agent 或 Multi-Agent；
- 设计 Prompt、Context、State、Session、Memory 与 Structured Output；
- 设计 Tool Calling、Function Calling、MCP Server、Skills 与工具权限；
- 构建企业级 RAG、Agentic RAG、长期 Memory 与知识更新链路；
- 理解并实现 ReAct、Plan & Solve、ReWOO、LLMCompiler、Reflection、Reflexion、LATS、STORM 等模式；
- 使用 LangGraph 等框架实现有状态、可恢复、可中断的复杂工作流；
- 设计 Supervisor、Handoff、Debate、Voting、Swarm、Shared State 等 Multi-Agent 架构；
- 理解 MCP 与 A2A 的职责边界，实现 Agent-to-Tool 与 Agent-to-Agent 互操作；
- 构建 Agent Runtime / Harness、Sandbox、Shell、Filesystem、Browser / Computer Use 能力；
- 实现 Streaming、Realtime、Voice、多模态与 Human-in-the-Loop 交互；
- 建立 Evaluation、Benchmark、Regression、Tracing、Logging 与 Observability；
- 防御 Prompt Injection、Tool Misuse、Memory Poisoning、Identity Abuse 等 Agent 安全风险；
- 设计长任务后端、Queue、Checkpoint、并发、缓存、模型路由、成本控制与 CI/CD；
- 独立完成 Coding Agent、Research Agent、Data Agent、企业知识库 Agent 与生产级 Multi-Agent 项目。

## 推荐学习顺序

```text
模型能力
  ↓
Prompt / Context / State
  ↓
Tool / MCP / Skills
  ↓
RAG / Memory
  ↓
Agent Loop / Workflow Pattern
  ↓
Multi-Agent
  ↓
LangGraph / Agent SDK
  ↓
Runtime / Harness / Sandbox
  ↓
交互 / Realtime / Multimodal
  ↓
Eval / Testing / Observability
  ↓
Security / Governance
  ↓
Production / DevOps
  ↓
综合项目
```

## 完整学习目录

### 00｜能力地图与架构选型

1. [Agent 全能工程师能力地图与学习路线](00-roadmap/01-agent-engineer-roadmap.md)
2. [Agent 架构选型：从函数、Workflow 到 Multi-Agent](00-roadmap/02-architecture-selection.md)

### 01｜模型与推理基础

1. [LLM、Reasoning Model 与 Agent 所需模型能力](01-models/01-model-and-reasoning-foundations.md)
2. [模型路由、Fallback、多模态与成本优化](01-models/02-model-routing-and-multimodal.md)

### 02｜Prompt、Context、State 与 Session

1. [Agent Prompt Engineering 与 Structured Output](02-context-state/01-prompt-structured-output.md)
2. [Context Engineering、State、Session 与 Compaction](02-context-state/02-context-state-session-compaction.md)

### 03｜Tool、MCP、Skills 与能力扩展

1. [Tool Calling 与 Function Calling 工程实践](03-tools-mcp-skills/01-tool-calling-engineering.md)
2. [MCP：从 Tool 协议到生产级 Server](03-tools-mcp-skills/02-mcp-production-guide.md)
3. [Agent Skills、Capability Registry 与渐进式能力加载](03-tools-mcp-skills/03-agent-skills-and-capability-registry.md)

### 04｜RAG、Knowledge 与 Memory

1. [企业级 RAG：从文档接入到可评估知识系统](04-rag-memory/01-enterprise-rag-engineering.md)
2. [Agentic RAG 与高级检索架构](04-rag-memory/02-agentic-rag-advanced-retrieval.md)
3. [Agent Memory Engineering：从会话历史到长期记忆](04-rag-memory/03-agent-memory-engineering.md)

### 05｜Agent Workflow 与设计模式

1. [Workflow Pattern：Prompt Chaining、Routing、Parallelization、MapReduce 与 Orchestrator-Workers](05-agent-patterns/01-workflow-patterns.md)
2. [ReAct、Plan & Solve、ReWOO 与 LLMCompiler](05-agent-patterns/02-react-plan-rewoo-llmcompiler.md)
3. [Reflection、Evaluator-Optimizer 与 Reflexion](05-agent-patterns/03-reflection-reflexion-evaluator.md)
4. [Self-Discover、LATS、STORM 与高级推理 / Research Pattern](05-agent-patterns/04-advanced-reasoning-lats-storm.md)

### 06｜Multi-Agent 与分布式智能体

1. [Multi-Agent 架构设计与职责拆分](06-multi-agent/01-multi-agent-architecture-design.md)
2. [Multi-Agent 协作模式：Supervisor、Handoff、Debate、Voting、Blackboard 与 Swarm](06-multi-agent/02-collaboration-patterns.md)
3. [A2A 与分布式 Agent：Agent-to-Agent 互操作](06-multi-agent/03-a2a-distributed-agents.md)

### 07｜Agent Framework 与 LangGraph

1. [LangGraph 核心：State、Node、Edge 与 Graph Runtime](07-frameworks/01-langgraph-core.md)
2. [LangGraph 高级工程：Persistence、Checkpoint、HITL、Streaming 与 Memory](07-frameworks/02-langgraph-persistence-hitl-streaming.md)
3. [Agent Framework / SDK 选型与框架无关设计](07-frameworks/03-agent-framework-selection.md)

### 08｜Agent Runtime、Harness 与执行环境

1. [Agent Runtime、Runner 与 Harness](08-runtime-harness/01-agent-runtime-and-harness.md)
2. [Sandbox、Shell、Filesystem 与 Code Execution](08-runtime-harness/02-sandbox-shell-filesystem.md)
3. [Browser Agent、Computer Use 与环境交互](08-runtime-harness/03-browser-computer-use.md)

### 09｜Agent 交互、Realtime 与多模态

1. [Streaming、Realtime、Voice 与 Multimodal Agent](09-interaction/01-streaming-realtime-voice-multimodal.md)
2. [Agent UX、任务进度、Artifact 与 Human Interaction](09-interaction/02-agent-ux-and-human-interaction.md)

### 10｜Evaluation、Testing 与 Observability

1. [Agent Evaluation 与 Benchmark：从最终答案到执行轨迹](10-evaluation-observability/01-agent-evaluation-benchmark.md)
2. [Agent Testing、Regression 与 Red Team](10-evaluation-observability/02-agent-testing-regression-redteam.md)
3. [Agent Observability：Tracing、Logging、Metrics 与事件模型](10-evaluation-observability/03-tracing-logging-observability.md)

### 11｜Security、权限与 Governance

1. [Agent 安全威胁：从 Prompt Injection 到 Rogue Agent](11-security-governance/01-agent-security-threats.md)
2. [Agent 权限、Identity、Guardrails 与 Human-in-the-Loop](11-security-governance/02-permission-identity-hitl.md)
3. [Agent Governance、Audit、数据安全与供应链治理](11-security-governance/03-governance-audit-data-security.md)

### 12｜Production Engineering 与 Agent DevOps

1. [Agent Backend：长任务、Queue、Checkpoint 与任务状态机](12-production-devops/01-agent-backend-long-running-tasks.md)
2. [Agent 性能工程：并发、缓存、预算、模型路由与成本](12-production-devops/02-performance-concurrency-cost.md)
3. [Agent Deployment、CI/CD 与 Agent DevOps](12-production-devops/03-deployment-cicd-agent-devops.md)

### 13｜专项 Agent 与大型项目

1. [专项 Agent 架构：Coding、Research、Data 与 Browser Agent](13-projects/01-specialized-agent-architectures.md)
2. [企业知识库 Agent：从 RAG Demo 到生产平台](13-projects/02-enterprise-knowledge-agent.md)
3. [毕业项目：生产级 Research + RAG + Data Multi-Agent 平台](13-projects/03-production-multi-agent-capstone.md)

### 辅助资料

- [Agent Engineering 专业名词速查](GLOSSARY.md)
- [官方资料与继续学习索引](REFERENCES.md)

## 阅读方式

每篇文档尽量采用统一结构：

1. **概念与定位**：解决什么问题；
2. **专业名词通义**：解释开发人员容易混淆的术语；
3. **核心原理**：内部机制与数据流；
4. **架构 / 流程**：使用图、Schema 或伪代码描述；
5. **核心实现**：接口、状态和代码层设计；
6. **工程落地**：生产项目中的实现方式；
7. **优势与限制**：明确成本和边界；
8. **适用与不适用场景**；
9. **常见反模式**；
10. **检查清单**：用于真实项目设计评审。

## 学习建议

不要按照“把所有框架 API 背完”学习。每学一个技术，都尝试回答：

```text
它解决什么工程问题？
状态保存在哪里？
谁控制下一步？
Tool 的权限怎么约束？
失败如何恢复？
如何测试？
如何 Eval？
如何 Trace？
如何控制 Token / Cost？
如何部署到多 Worker？
```

如果这些问题都能回答，换 Agent 框架时迁移成本会很低。

## 一条最重要的工程原则

> **能用确定性代码解决的问题，不要交给 LLM；能用 Workflow 解决的问题，不要强行做自治 Agent；能用一个 Agent 解决的问题，不要为了“高级”拆成多个 Agent。**

Agent 工程的目标不是最大化 Agent 数量或推理轮数，而是在 **质量、可控性、延迟、成本、安全、可观测性与可维护性** 之间取得合理平衡。
