# Agent Framework / SDK 选型与框架无关设计

## 1. 全能工程师不能只会一个框架

框架 API 会变化，但核心抽象长期稳定：

```text
Model
Agent
Runner / Runtime
Tool
State / Session
Workflow
Handoff
Guardrail
Memory
Trace
```

学习目标应该是看到新 SDK 后能快速映射这些概念。

## 2. 三类工具

### 高层 Agent SDK

特点：快速创建 Agent，自带循环、Tool、Handoff、Guardrail 等。

适合：

- 单 Agent；
- 轻量 Multi-Agent；
- 快速产品开发。

### Workflow / Graph Runtime

特点：显式 State 和 Control Flow。

适合：

- 复杂业务 Workflow；
- 长任务；
- HITL；
- Multi-Agent；
- 可恢复执行。

### Harness

特点：为长、多步骤任务提供“工作环境”。

常见能力：

- Plan / Todo；
- Context Compaction；
- Filesystem；
- Skills；
- Tool Approval；
- Memory；
- Observability。

## 3. LangGraph

定位：低层 orchestration runtime。

强项：

```text
StateGraph
Durable Execution
Persistence
HITL
Streaming
SubGraph
Complex Control Flow
```

适合需要“自己控制图”的开发团队。

## 4. OpenAI Agents SDK

当前核心抽象包含：

- Agents；
- Tools；
- Handoffs / Agents as Tools；
- Guardrails；
- Sessions；
- Tracing；
- Sandbox Agents；
- Realtime / Voice。

它的特点是抽象较少，用语言本身完成很多编排。

如果需要显式复杂 Graph，可以自己组合或使用其他 Runtime。

## 5. Microsoft Agent Framework

当前官方将能力明确分为：

```text
Agents
Harness
Workflows
```

并提供 session、context providers、middleware、MCP client 等基础构件。

这个分层很值得作为工程心智模型，即使项目不使用 Microsoft SDK。

## 6. 其他框架应该如何学

对于 ADK、CrewAI 等，不建议“把每个 API 都背一遍”。

评估：

```text
Model Provider Support
Tool / MCP
Workflow Control
Multi-Agent
Persistence
HITL
Memory
Tracing
Deployment
Community / Stability
Vendor Lock-in
```

## 7. 什么时候自己写 Runtime

简单 Agent Loop 可以自己写：

```python
for step in range(max_steps):
    response = model(...)
    if final(response):
        return response
    result = tool_executor(response.tool_call)
    state.update(result)
```

但一旦需要：

```text
Checkpoint
Resume
Parallel
HITL
Distributed Worker
Trace
Retry semantics
```

自己维护 Runtime 成本迅速上升。

## 8. Framework Adapter

业务层应避免直接依赖具体框架对象。

例如定义：

```text
AgentService
WorkflowService
ModelGateway
ToolRegistry
MemoryRepository
TraceContext
```

框架实现放 infrastructure 层。

这样未来可以：

```text
LangGraph → another runtime
Provider A → Provider B
```

而不重写业务核心。

## 9. 选型决策

### 简单 Tool Agent

优先高层 Agent SDK。

### 强控制复杂流程

LangGraph / Graph Workflow。

### Coding / Workspace Agent

优先考虑带 Harness / Sandbox 的体系，或自己构建 Harness。

### 企业跨技术栈

关注 MCP / A2A、身份、观测和部署，而不是只看本地 Demo 体验。

## 10. 参考

- LangGraph：https://docs.langchain.com/oss/python/langgraph/overview
- OpenAI Agents SDK：https://openai.github.io/openai-agents-python/
- Microsoft Agent Framework：https://learn.microsoft.com/en-us/agent-framework/overview/
