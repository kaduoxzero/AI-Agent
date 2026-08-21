# AI Agent 全能工程师知识库

> 面向有一定 AI 与软件开发基础的开发人员，目标不是“会调用一个 Agent 框架”，而是能够从 0 到 1 设计、实现、评估、部署并维护真实的大型 Agent / Multi-Agent 系统。

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
- 防御 Prompt Injection、Tool Poisoning、Memory Poisoning、Excessive Agency 等 Agent 安全风险；
- 设计长任务后端、Queue、Checkpoint、并发、缓存、模型路由、成本控制与 CI/CD；
- 独立完成 Coding Agent、Research Agent、Data Agent、企业知识库 Agent 与生产级 Multi-Agent 项目。

## 知识库结构

```text
AI Agent 全能工程师知识库
├── 00-roadmap/              # 学习路线、能力地图、架构选型
├── 01-models/               # LLM、Reasoning、模型路由与多模态
├── 02-context-state/        # Prompt、Context Engineering、State、Session
├── 03-tools-mcp-skills/     # Tool Calling、MCP、Skills
├── 04-rag-memory/           # RAG、Agentic RAG、Memory、数据工程
├── 05-agent-patterns/       # Agent Workflow 与经典设计模式
├── 06-multi-agent/          # Multi-Agent 与 A2A
├── 07-frameworks/           # LangGraph 与主流 Agent SDK
├── 08-runtime-harness/      # Runtime、Harness、Sandbox、Browser/Computer Use
├── 09-interaction/          # Streaming、Realtime、Voice、多模态与 Agent UX
├── 10-evaluation-observability/ # Eval、Testing、Tracing、Observability
├── 11-security-governance/  # 安全、权限、HITL、治理与审计
├── 12-production-devops/    # Backend、长任务、性能、成本、部署、CI/CD
└── 13-projects/             # 专项 Agent 与大型综合项目
```

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
Eval / Testing / Observability
  ↓
Security / Governance
  ↓
Production / DevOps
  ↓
综合项目
```

## 阅读约定

每篇文档尽量保持统一结构：

1. **概念与定位**：解决什么问题；
2. **专业名词通义**：只解释开发人员容易混淆的名词；
3. **核心原理**：内部机制与数据流；
4. **架构 / 流程**：用图或伪代码描述；
5. **核心实现**：代码、Schema 或接口设计；
6. **工程落地**：生产项目中的设计方法；
7. **优势与限制**：避免“只讲优点”；
8. **适用与不适用场景**；
9. **常见反模式**；
10. **检查清单**：用于真实项目设计评审。

## 一条最重要的工程原则

> **能用确定性代码解决的问题，不要交给 LLM；能用 Workflow 解决的问题，不要强行做自治 Agent；能用一个 Agent 解决的问题，不要为了“高级”拆成多个 Agent。**

Agent 工程的目标不是最大化“智能体数量”或“推理轮数”，而是在 **质量、可控性、延迟、成本、安全与可维护性** 之间取得合理平衡。
