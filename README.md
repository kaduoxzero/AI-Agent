# AI Agent 全能工程师知识库

> 面向有一定 AI 与软件开发基础的开发人员。目标不是“会调用一个 Agent 框架”，而是能够从 0 到 1 **设计、实现、评估、部署、治理并维护真实的大型 Agent / Multi-Agent 平台**。

## 当前仓库已经包含什么

这不是只有 Markdown 的知识库。当前仓库已经形成四层学习体系：

```text
Layer 1｜Knowledge
核心概念、原理、Pattern、Framework
        ↓
Layer 2｜Practice
18 个可运行 Hands-on Labs
        ↓
Layer 3｜Engineering
Golden Evals + Schemas + ADR + Reference Architecture + CI
        ↓
Layer 4｜Production
Reference Platform Starter + Security + SRE + Platform Engineering
```

当前工程化资产包括：

- **15 个知识领域**：从模型、Context、Tool、RAG、Pattern、Multi-Agent 到 Runtime、Security、SRE、Platform；
- **18 个实际 Lab**：每个 Lab 都有代码和工程验收目标；
- **Golden Dataset / Security Red Team Dataset**：用于 Output、Trajectory、Tool、安全回归；
- **GitHub Actions**：自动执行 Lab 和 Reference Starter 测试，并对 Skills 体系做结构校验；
- **Reference Agent Platform Starter**：FastAPI Task API、Typed Contract、Dockerfile、PostgreSQL、Redis、API Test；
- **Reference Architecture**：统一生产级 Agent 平台架构蓝图；
- **Schemas / ADR / Glossary / References**：数据契约、架构决策、术语与官方资料；
- **Agent Engineering Runtime v2 与 Skills 体系**：可注册、可校验、可版本管理的 Skill 工程系统（见下节）。

> 注意：GitHub Actions Workflow 已经写入仓库，但是否通过应以仓库 Actions 页面中的实际 Check Run 为准；不要把“存在 CI 配置”与“当前 CI 已绿”混为一谈。

最终目标是完成从：

```text
知道 → 会写 → 会设计 → 会测试 → 会排障 → 会上线 → 会治理
```

的完整能力闭环。

## 学完应具备的能力

完成本知识库后，应能够独立：

- 根据业务复杂度选择 LLM、Workflow、Single Agent 或 Multi-Agent；
- 设计 Prompt、Context、State、Session、Memory、Artifact 与 Structured Output；
- 设计 Tool Calling、Function Calling、MCP Server、Skills 与工具权限；
- 构建企业级 RAG、Agentic RAG、长期 Memory 与知识更新链路；
- 实现 ReAct、Plan & Solve、ReWOO、LLMCompiler、Reflection、Reflexion、LATS、STORM 等模式；
- 使用 LangGraph 等框架实现有状态、可恢复、可中断的复杂工作流；
- 设计 Supervisor、Handoff、Debate、Voting、Swarm、Shared State 等 Multi-Agent 架构；
- 理解 MCP、A2A、AG-UI 三类边界，实现 Tool、Agent、Frontend 的标准化互操作；
- 构建 Agent Runtime / Harness、Sandbox、Shell、Filesystem、Browser / Computer Use 能力；
- 设计 Agent Identity、Delegation、Tool Gateway、最小权限与 HITL；
- 建立 Model Gateway、模型路由、Fallback、Quota 与成本治理；
- 实现 Event-Driven / Proactive Agent、Queue、DLQ、Replay 和 Scheduler；
- 建立 Evaluation、Scenario Simulation、Regression、Tracing、Logging 与 Observability；
- 建立 SLI / SLO、Circuit Breaker、Degraded Mode、Runbook 与 Agent SRE；
- 建设 Agent Registry、Release、Canary、Rollback 和 Control Plane；
- 独立完成生产级 Coding、Research、Data、Browser、RAG 与 Multi-Agent 项目。

## 推荐学习顺序

```text
模型能力 / Model Gateway
  ↓
Prompt / Context / State / Artifact
  ↓
Tool / MCP / Skills
  ↓
RAG / Memory
  ↓
Agent Loop / Workflow Pattern
  ↓
Multi-Agent / A2A
  ↓
LangGraph / Agent SDK
  ↓
Runtime / Harness / Sandbox
  ↓
AG-UI / Realtime / Multimodal
  ↓
Eval / Simulation / Observability
  ↓
Identity / Security / Governance
  ↓
Backend / Event Driven / SRE / DevOps
  ↓
Agent Platform Engineering
  ↓
18 Labs
  ↓
Reference Agent Platform
  ↓
生产级毕业项目
```

# Agent Engineering 工程体系（Runtime v2）

仓库不只是知识库，还包含一套可治理的 Agent 工程系统：

| 目录 | 职责 | 权威入口 |
|---|---|---|
| `skills/` | 13 个可注册 Skill（SKILL.md 执行协议 + skill.yaml 机器清单 + 模板） | [skills/README.md](skills/README.md) |
| `runtime/` | Runtime v2 治理层：registry / router / loader / validator / policy / state 规范 | [runtime/README.md](runtime/README.md) |
| `schemas/` | Agent / Task / Evidence 等共享数据契约 | [schemas/README.md](schemas/README.md) |
| `architecture/` | Core-Domain 分层与 Skill 设计规范 | [architecture/CORE-DOMAIN-SEPARATION.md](architecture/CORE-DOMAIN-SEPARATION.md) |
| `docs/` | v2 架构说明与 Skill 开发标准 | [docs/AI-AGENT-V2-ARCHITECTURE.md](docs/AI-AGENT-V2-ARCHITECTURE.md) |
| `evaluation/` | 评估框架：benchmark schema、metrics、路由与安全用例 | [evaluation/README.md](evaluation/README.md) |
| `evals/` | 可执行数据集：Golden Dataset 与 Red Team 数据（jsonl） | [evals/golden/agent_baseline.jsonl](evals/golden/agent_baseline.jsonl) |
| `governance/` | Tool 风险分级与确认策略 | [governance/tool-governance.yaml](governance/tool-governance.yaml) |
| `memory/` | Memory L0-L4 分层、生命周期与记录 Schema | [memory/README.md](memory/README.md) |
| `15-skill-engineering/` | Skill Router / Validator 工程设计视角 | [15-skill-engineering/README.md](15-skill-engineering/README.md) |
| `16-agent-operating-system/` | Agent OS：把 Agent 当受管软件实体治理 | [16-agent-operating-system/README.md](16-agent-operating-system/README.md) |
| `17-benchmarks/` | Agent 能力基准框架（Planning/Tool/RAG/Safety/Cost 等） | [17-benchmarks/README.md](17-benchmarks/README.md) |
| `18-case-studies/` | Coding / Knowledge / Healthcare 场景案例骨架 | [18-case-studies/README.md](18-case-studies/README.md) |

机器事实源与护栏：

```text
runtime/skill-registry.yaml      Skill 注册表（status / category，SSoT）
scripts/validate_skills.py       结构校验执行器（manifest 一致性、引用完整性等）
.github/workflows/skills.yml     CI 强制校验
```

核心约定：Skill 内部协议使用英文 ID；实例化到业务项目的状态文档使用中文文件名（映射见 `skills/agent-engineering-master/resources/PROJECT-DOCUMENT-NAMING.md`）；模板只读，项目状态隔离在 `<project>/.agent-engineering/`。

# 完整学习目录

## 00｜能力地图与架构选型

1. [Agent 全能工程师能力地图与学习路线](00-roadmap/01-agent-engineer-roadmap.md)
2. [Agent 架构选型：从函数、Workflow 到 Multi-Agent](00-roadmap/02-architecture-selection.md)

## 01｜模型与推理基础

1. [LLM、Reasoning Model 与 Agent 所需模型能力](01-models/01-model-and-reasoning-foundations.md)
2. [模型路由、Fallback、多模态与成本优化](01-models/02-model-routing-and-multimodal.md)
3. [Model Gateway、Serving 与 Inference Infrastructure](01-models/03-model-gateway-serving.md)

## 02｜Prompt、Context、State 与 Artifact

1. [Agent Prompt Engineering 与 Structured Output](02-context-state/01-prompt-structured-output.md)
2. [Context Engineering、State、Session 与 Compaction](02-context-state/02-context-state-session-compaction.md)
3. [Agent Artifact、Evidence 与数据契约工程](02-context-state/03-artifact-evidence-contracts.md)

## 03｜Tool、MCP、Skills 与能力扩展

1. [Tool Calling 与 Function Calling 工程实践](03-tools-mcp-skills/01-tool-calling-engineering.md)
2. [MCP：从 Tool 协议到生产级 Server](03-tools-mcp-skills/02-mcp-production-guide.md)
3. [Agent Skills、Capability Registry 与渐进式能力加载](03-tools-mcp-skills/03-agent-skills-and-capability-registry.md)

## 04｜RAG、Knowledge 与 Memory

1. [企业级 RAG：从文档接入到可评估知识系统](04-rag-memory/01-enterprise-rag-engineering.md)
2. [Agentic RAG 与高级检索架构](04-rag-memory/02-agentic-rag-advanced-retrieval.md)
3. [Agent Memory Engineering：从会话历史到长期记忆](04-rag-memory/03-agent-memory-engineering.md)

## 05｜Agent Workflow 与设计模式

1. [Workflow Pattern：Prompt Chaining、Routing、Parallelization、MapReduce 与 Orchestrator-Workers](05-agent-patterns/01-workflow-patterns.md)
2. [ReAct、Plan & Solve、ReWOO 与 LLMCompiler](05-agent-patterns/02-react-plan-rewoo-llmcompiler.md)
3. [Reflection、Evaluator-Optimizer 与 Reflexion](05-agent-patterns/03-reflection-reflexion-evaluator.md)
4. [Self-Discover、LATS、STORM 与高级推理 / Research Pattern](05-agent-patterns/04-advanced-reasoning-lats-storm.md)

## 06｜Multi-Agent 与分布式智能体

1. [Multi-Agent 架构设计与职责拆分](06-multi-agent/01-multi-agent-architecture-design.md)
2. [Multi-Agent 协作模式：Supervisor、Handoff、Debate、Voting、Blackboard 与 Swarm](06-multi-agent/02-collaboration-patterns.md)
3. [A2A 与分布式 Agent：Agent-to-Agent 互操作](06-multi-agent/03-a2a-distributed-agents.md)

## 07｜Agent Framework 与 LangGraph

1. [LangGraph 核心：State、Node、Edge 与 Graph Runtime](07-frameworks/01-langgraph-core.md)
2. [LangGraph 高级工程：Persistence、Checkpoint、HITL、Streaming 与 Memory](07-frameworks/02-langgraph-persistence-hitl-streaming.md)
3. [Agent Framework / SDK 选型与框架无关设计](07-frameworks/03-agent-framework-selection.md)

## 08｜Agent Runtime、Harness 与执行环境

1. [Agent Runtime、Runner 与 Harness](08-runtime-harness/01-agent-runtime-and-harness.md)
2. [Sandbox、Shell、Filesystem 与 Code Execution](08-runtime-harness/02-sandbox-shell-filesystem.md)
3. [Browser Agent、Computer Use 与环境交互](08-runtime-harness/03-browser-computer-use.md)

## 09｜Agent 交互、Realtime 与多模态

1. [Streaming、Realtime、Voice 与 Multimodal Agent](09-interaction/01-streaming-realtime-voice-multimodal.md)
2. [Agent UX、任务进度、Artifact 与 Human Interaction](09-interaction/02-agent-ux-and-human-interaction.md)
3. [AG-UI 与 Agent 前后端协议](09-interaction/03-ag-ui-agent-frontend-protocol.md)

## 10｜Evaluation、Testing 与 Observability

1. [Agent Evaluation 与 Benchmark：从最终答案到执行轨迹](10-evaluation-observability/01-agent-evaluation-benchmark.md)
2. [Agent Testing、Regression 与 Red Team](10-evaluation-observability/02-agent-testing-regression-redteam.md)
3. [Agent Observability：Tracing、Logging、Metrics 与事件模型](10-evaluation-observability/03-tracing-logging-observability.md)
4. [Agent Simulation、Scenario Test 与 Environment Eval](10-evaluation-observability/04-simulation-environment-eval.md)

## 11｜Security、Identity 与 Governance

1. [Agent 安全威胁：从 Prompt Injection 到 Rogue Agent](11-security-governance/01-agent-security-threats.md)
2. [Agent 权限、Identity、Guardrails 与 Human-in-the-Loop](11-security-governance/02-permission-identity-hitl.md)
3. [Agent Governance、Audit、数据安全与供应链治理](11-security-governance/03-governance-audit-data-security.md)
4. [Agent Identity、Delegation 与 Authorization](11-security-governance/04-agent-identity-delegation.md)

## 12｜Production Engineering、Event 与 SRE

1. [Agent Backend：长任务、Queue、Checkpoint 与任务状态机](12-production-devops/01-agent-backend-long-running-tasks.md)
2. [Agent 性能工程：并发、缓存、预算、模型路由与成本](12-production-devops/02-performance-concurrency-cost.md)
3. [Agent Deployment、CI/CD 与 Agent DevOps](12-production-devops/03-deployment-cicd-agent-devops.md)
4. [Event-Driven 与 Proactive Agent](12-production-devops/04-event-driven-proactive-agents.md)
5. [Agent SRE：Reliability Engineering 与故障治理](12-production-devops/05-agent-sre-reliability.md)

## 13｜专项 Agent 与大型项目

1. [专项 Agent 架构：Coding、Research、Data 与 Browser Agent](13-projects/01-specialized-agent-architectures.md)
2. [企业知识库 Agent：从 RAG Demo 到生产平台](13-projects/02-enterprise-knowledge-agent.md)
3. [毕业项目：生产级 Research + RAG + Data Multi-Agent 平台](13-projects/03-production-multi-agent-capstone.md)

## 14｜Agent Platform Engineering

1. [Agent Platform：Control Plane 与 Data Plane](14-platform-engineering/01-control-plane-data-plane.md)
2. [Agent Registry、Versioning 与 Release Governance](14-platform-engineering/02-registry-version-release-governance.md)

# 工程实训与规范

- [Hands-on Labs：18 个已实现 Agent 工程实训](labs/README.md)
- [Agent Engineering Skills：可注册可校验的技能体系](skills/README.md)
- [Agent Runtime v2：运行时治理层](runtime/README.md)
- [Skill 开发标准与结构校验](docs/SKILL-DEVELOPMENT-STANDARD.md)
- [Reference Agent Platform Starter：可启动工程脚手架](reference-architecture/starter/README.md)
- [Production Reference Architecture：生产架构蓝图](reference-architecture/README.md)
- [Golden Evals](evals/)
- [Evaluation Framework](evaluation/README.md)
- [Examples：最小可运行示例规划](examples/README.md)
- [Shared Schemas：Task / Event / Artifact / Evidence 数据契约](schemas/README.md)
- [ADR：Architecture Decision Records](adrs/README.md)
- [Agent Engineering 专业名词速查](GLOSSARY.md)
- [官方资料与继续学习索引](REFERENCES.md)

# 18 个实训覆盖的工程链

```text
01 Structured Output
 ↓
02 Tool Runtime
 ↓
03 MCP Server
 ↓
04 Enterprise RAG
 ↓
05 Agent Loop
 ↓
06 LangGraph HITL
 ↓
07 Agent Eval
 ↓
08 Model Gateway
 ↓
09 Agentic RAG
 ↓
10 Memory Engineering
 ↓
11 Multi-Agent + Typed Artifact
 ↓
12 Agent Identity / Delegation
 ↓
13 AG-UI Event Console
 ↓
14 Sandbox Coding Agent
 ↓
15 Security Red Team
 ↓
16 Event-Driven Agent
 ↓
17 Agent SRE
 ↓
18 Agent Platform / Canary / Rollback
```

完成后再进入 `reference-architecture/starter/`，把这些能力逐步装配到同一个 Agent Platform 中。

# 每篇知识文档的统一标准

1. **概念与定位**：解决什么问题；
2. **专业名词通义**：解释容易混淆的术语；
3. **核心原理**：内部机制与数据流；
4. **架构 / 流程**：图、Schema 或伪代码；
5. **核心实现**：接口、状态、数据契约和代码层设计；
6. **工程落地**：生产项目中的实现方式；
7. **优势与限制**：明确成本和边界；
8. **故障与安全**：失败时发生什么；
9. **适用与不适用场景**；
10. **常见反模式**；
11. **Lab / 实训建议**；
12. **检查清单 / 验收标准**。

# 学习时始终问这 12 个问题

```text
1. 它解决什么工程问题？
2. 谁控制下一步？
3. State 保存在哪里？
4. Context 如何构建与压缩？
5. 模块之间传递什么 Artifact / Schema？
6. Tool / Agent 的权限在哪里判断？
7. 失败如何 Retry / Fallback / Resume？
8. 如何测试 Output 和 Trajectory？
9. 如何 Trace？
10. 如何限制 Token / Step / Cost？
11. 如何部署、扩缩容和降级？
12. 出事故如何止损、回滚和复盘？
```

如果这些问题都能回答，换 Agent 框架或模型时迁移成本会很低。

## 一条最重要的工程原则

> **能用确定性代码解决的问题，不要交给 LLM；能用 Workflow 解决的问题，不要强行做自治 Agent；能用一个 Agent 解决的问题，不要为了“高级”拆成多个 Agent。**

Agent 工程的目标不是最大化 Agent 数量或推理轮数，而是在 **质量、可控性、延迟、成本、安全、可靠性、可观测性与可维护性** 之间取得合理平衡。
