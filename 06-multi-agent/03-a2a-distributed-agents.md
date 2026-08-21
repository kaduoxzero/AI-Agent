# A2A 与分布式 Agent：Agent-to-Agent 互操作

> 截至 2026 年，A2A 已发布 1.0.0 稳定规范，目标是让不同框架、语言、厂商构建的独立 Agent 可以发现能力并协作。

## 1. 为什么需要 A2A

进程内 Multi-Agent 可以直接共享函数和 State。

但企业级系统经常是：

```text
Department A Agent (Python / LangGraph)
Department B Agent (Java / custom)
Partner Agent (external)
```

它们不能共享内部内存或代码。

A2A 用于定义跨系统 Agent 的公共通信模型。

## 2. MCP 与 A2A

```text
MCP：Agent ↔ Tool / Resource
A2A：Agent ↔ Agent
```

两者互补。

```text
Client Agent
  ├─ MCP → DB Tool
  └─ A2A → Research Agent
               └─ MCP → Search Tool
```

## 3. A2A 的核心能力

A2A 1.0 关注：

- Agent Discovery；
- 能力描述；
- 任务协作；
- Message / Artifact；
- Streaming；
- 异步长任务；
- 多协议绑定；
- 安全互操作。

## 4. Agent Card

Agent Card 相当于远程 Agent 的能力说明书。

可描述：

- 名称；
- endpoint；
- 协议版本；
- 支持的 skills；
- authentication；
- input / output modality。

标准发现位置可使用：

```text
/.well-known/agent-card.json
```

### 专业名词通义：Agent Discovery

客户端无需预先写死所有远程 Agent 内部实现，而是通过标准能力描述了解“这个 Agent 能做什么、怎么调用”。

## 5. Task

A2A 将协作抽象为 Task，而不只是一问一答。

适合长任务：

```text
submitted
→ working
→ input-required
→ completed / failed
```

具体状态以协议定义为准，工程上要建立“远程任务有生命周期”的意识。

## 6. Message 与 Artifact

### Message

Agent 间交换的交互消息。

### Artifact

任务产生的稳定产物，例如：

- 报告；
- 文件；
- 结构化结果。

这比只返回一段聊天文本更适合跨系统协作。

## 7. Opaque Agent

A2A 的重要设计目标之一是：

> 一个 Agent 可以与另一个 Agent 协作，而不需要访问对方内部 Memory、Tools 或私有实现。

这对跨部门和跨公司很重要。

## 8. Distributed Agent Architecture

```text
              Agent Registry
                   ↑
Client Agent ── discovery
     │
     ├─ A2A → Research Service
     ├─ A2A → Finance Service
     └─ A2A → Partner Service
```

需要额外考虑：

- Network Timeout；
- Identity；
- Authorization；
- Version Negotiation；
- Retry；
- Task Idempotency；
- Distributed Trace。

## 9. Agent Identity

远程 Agent 不能只凭“我是某某 Agent”自我声明权限。

需要：

```text
Service Identity
User Delegation
OAuth / Token
Tenant Context
Policy Enforcement
```

## 10. A2A 与内部 Handoff 的区别

内部 Handoff：同一个 Runtime 内转移控制。

A2A：跨网络、跨系统协作，需要处理协议、身份、任务生命周期和失败恢复。

## 11. 什么时候使用 A2A

适合：

- 跨团队 Agent 平台；
- 不同技术栈；
- 第三方 Agent；
- Agent Marketplace；
- 独立部署 Agent Service。

不适合：

同一进程内两个简单 Node。直接函数调用更简单。

## 12. 检查清单

- [ ] 是否真的跨独立 Agent 系统？
- [ ] 是否需要 Agent Discovery？
- [ ] 是否定义身份与授权？
- [ ] 是否支持长 Task 状态？
- [ ] 是否有 Distributed Trace ID？
- [ ] 是否处理 Version Negotiation？
- [ ] 是否有网络失败 / Retry / Idempotency？

## 13. 参考

- A2A 1.0 Specification：https://a2a-protocol.org/latest/specification/
- A2A 1.0 Announcement：https://a2a-protocol.org/latest/announcing-1.0/
