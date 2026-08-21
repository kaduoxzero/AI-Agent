# 官方资料与继续学习索引

> Agent 生态变化快。知识库正文讲稳定工程思想；涉及协议和 SDK 具体 API 时，应以官方最新文档为准。

## Agent / Workflow / Runtime

- LangGraph Overview: https://docs.langchain.com/oss/python/langgraph/overview
- LangGraph Persistence: https://docs.langchain.com/oss/python/langgraph/persistence
- LangGraph Interrupts: https://docs.langchain.com/oss/python/langgraph/interrupts
- LangGraph Streaming: https://docs.langchain.com/oss/python/langgraph/streaming
- OpenAI Agents SDK: https://openai.github.io/openai-agents-python/
- OpenAI Agents SDK Tracing: https://openai.github.io/openai-agents-python/tracing/
- OpenAI Sandbox Agents: https://openai.github.io/openai-agents-python/sandbox/guide/
- Microsoft Agent Framework Overview: https://learn.microsoft.com/en-us/agent-framework/overview/
- Microsoft Agent Harness: https://learn.microsoft.com/en-us/agent-framework/get-started/harness

## Agent Protocol / Interoperability

### Agent ↔ Tool / Data

- Model Context Protocol: https://modelcontextprotocol.io/
- MCP 2026-07-28 Release: https://blog.modelcontextprotocol.io/posts/2026-07-28/

### Agent ↔ Agent

- A2A Protocol: https://a2a-protocol.org/latest/
- A2A Specification: https://a2a-protocol.org/latest/specification/

### Agent ↔ User / Frontend

- AG-UI Repository: https://github.com/ag-ui-protocol/ag-ui
- AG-UI Overview: https://github.com/ag-ui-protocol/ag-ui/blob/main/docs/introduction.mdx
- AG-UI Events: https://github.com/ag-ui-protocol/ag-ui/blob/main/docs/concepts/events.mdx

## Agent Identity / Authentication / Authorization

- Microsoft Entra Agent ID: https://learn.microsoft.com/en-us/entra/agent-id/
- Microsoft Entra Agent Identities: https://learn.microsoft.com/en-us/entra/agent-id/agent-identities
- Microsoft Entra Agent Authorization: https://learn.microsoft.com/en-us/entra/agent-id/authorization-agent-id
- IETF Internet-Draft — AI Agent Authentication and Authorization: https://datatracker.ietf.org/doc/draft-klrc-aiagent-auth/

> 注意：IETF Internet-Draft 属于持续演进中的工作文档，不应当作已经完成标准化的正式 RFC。学习重点是理解 Workload Identity、OAuth、Delegation、Token Exchange 和最小权限等设计思想。

## Security

- OWASP Top 10 for Agentic Applications 2026: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
- OWASP Agentic Security Initiative: https://genai.owasp.org/initiatives/agentic-security-initiative/
- OWASP Memory & Context Poisoning: https://genai.owasp.org/2026/05/13/memory-is-a-feature-it-is-also-an-attack-surface/

## Observability / Reliability

- OpenTelemetry: https://opentelemetry.io/
- LangSmith: https://www.langchain.com/langsmith
- Google SRE Books: https://sre.google/books/

## Identity / Authorization 基础标准

进一步学习 Agent Identity 前，建议理解：

- OAuth 2.0 / OAuth 2.1 演进；
- JWT；
- OAuth Token Exchange；
- Workload Identity Federation；
- Zero Trust；
- RBAC / ABAC；
- Short-lived Credentials。

## Data / Backend / Platform 基础

Agent 全能工程师还应熟悉：

- PostgreSQL；
- Redis；
- Message Queue；
- Object Storage；
- Docker / Kubernetes；
- API Gateway；
- Secret Manager；
- CI/CD；
- OpenTelemetry；
- SLI / SLO / Error Budget。

## 经典 Agent Pattern 论文方向

- ReAct: Synergizing Reasoning and Acting in Language Models
- Plan-and-Solve Prompting
- ReWOO: Decoupling Reasoning from Observations for Efficient Augmented Language Models
- An LLM Compiler for Parallel Function Calling
- Reflexion: Language Agents with Verbal Reinforcement Learning
- Self-Discover: Large Language Models Self-Compose Reasoning Structures
- Language Agent Tree Search (LATS)
- STORM: Synthesis of Topic Outlines through Retrieval and Multi-perspective Question Asking

## 阅读建议

学习一个新框架 / 协议时，不要先背 API。先回答：

```text
它解决哪个系统边界的问题？
它的 Agent / Runtime 是什么？
State 如何保存？
Tool 如何执行？
Identity 如何验证？
权限在哪里判断？
HITL 怎么暂停恢复？
Memory 怎么分层？
Trace 怎么导出？
如何测试故障？
生产部署怎么做？
```

能回答这些问题，框架迁移会非常快。