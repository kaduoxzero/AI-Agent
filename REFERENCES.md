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

## Protocol

- Model Context Protocol: https://modelcontextprotocol.io/
- MCP 2026-07-28 Release: https://blog.modelcontextprotocol.io/posts/2026-07-28/
- A2A Protocol: https://a2a-protocol.org/latest/
- A2A 1.0 Specification: https://a2a-protocol.org/latest/specification/

## Security

- OWASP Top 10 for Agentic Applications 2026: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
- OWASP Agentic Security Initiative: https://genai.owasp.org/initiatives/agentic-security-initiative/
- OWASP Memory & Context Poisoning: https://genai.owasp.org/2026/05/13/memory-is-a-feature-it-is-also-an-attack-surface/

## Observability

- OpenTelemetry: https://opentelemetry.io/
- LangSmith: https://www.langchain.com/langsmith

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

学习一个新框架时，不要先背 API。先回答：

```text
它的 Agent 是什么？
Runtime 在哪？
State 如何保存？
Tool 如何执行？
HITL 怎么暂停恢复？
Memory 怎么分层？
Trace 怎么导出？
生产部署怎么做？
```

能回答这些问题，框架迁移会非常快。
