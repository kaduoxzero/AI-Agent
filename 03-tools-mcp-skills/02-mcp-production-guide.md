# MCP：从 Tool 协议到生产级 Server

> 本文以 2026-07-28 MCP 规范演进为背景，重点讲工程抽象，而不是只做一个 Demo Server。

## 1. MCP 解决什么问题

MCP（Model Context Protocol）用于标准化 AI 应用与外部能力之间的连接。

可以先建立这个心智模型：

```text
Agent Host
  ↓
MCP Client
  ↓ protocol
MCP Server
  ↓
Tool / Resource / Extension
```

### 专业名词通义

- **Host**：承载 Agent / AI 应用的主程序。
- **Client**：Host 内部与某个 MCP Server 通信的组件。
- **Server**：对外暴露能力的 MCP 服务。
- **Tool**：可执行操作。
- **Resource**：可读取的上下文或资源。

## 2. MCP 与普通 API 的区别

普通 API 解决程序之间的业务调用。

MCP 额外标准化了 Agent 生态关心的：

- 能力发现；
- Tool Schema；
- 上下文交互；
- Agent Host 集成；
- 授权模型；
- 扩展机制。

并不意味着所有内部 API 都应该改造成 MCP。

推荐：

```text
Agent → MCP Adapter → Existing Service API
```

而不是重写所有业务服务。

## 3. 2026-07-28 规范需要知道的变化

截至 2026-07-28，MCP 核心协议转向更 stateless 的设计，并强化：

- Multi Round-Trip Requests；
- Header-based Routing；
- cacheable list results；
- Authorization；
- Extensions；
- Tasks。

这意味着新知识库不要继续把“长连接 session handshake”当成 MCP 永恒核心概念。

> 协议会继续演进，生产代码必须固定兼容版本并做能力协商，而不是假设所有 Server 行为一致。

## 4. MCP Server 怎么设计

### 4.1 Tool 不要映射成数据库表 CRUD

错误：

```text
insert_row
update_row
delete_row
```

更好：

```text
create_followup_plan
update_patient_risk_status
publish_report
```

Tool 应表达业务能力。

### 4.2 Schema 严格

MCP Tool 输入仍然应遵循严格 JSON Schema。

### 4.3 Server 是安全边界

MCP Server 不能信任 Agent 已经做过权限校验。

Server 自己必须处理：

```text
Authentication
Authorization
Tenant Isolation
Input Validation
Audit
Rate Limit
```

## 5. Remote MCP

远程 MCP 需要额外考虑：

- 网络超时；
- DNS / TLS；
- OAuth；
- Scope；
- Server 身份；
- 版本兼容；
- 供应链风险。

第三方 MCP Server 本质上等于给 Agent 安装外部插件，应按第三方依赖治理。

## 6. MCP Authorization

不要把 API Key 明文塞进 Prompt 或 Tool 参数。

建议：

```text
User / Agent Identity
 ↓
OAuth / Credential Broker
 ↓ scoped token
MCP Server
```

授权范围应该最小化。

## 7. MCP Gateway

大型企业可以增加统一 Gateway：

```text
Agents
  ↓
MCP Gateway
├─ Server Registry
├─ Auth
├─ Policy
├─ Audit
├─ Rate Limit
└─ Routing
  ↓
MCP Servers
```

收益：

- 集中治理 Server；
- 统一身份与审计；
- 控制第三方 MCP；
- 统一流量与版本策略。

## 8. MCP 与 A2A

最重要的区别：

```text
MCP：Agent ↔ Tool / Resource
A2A：Agent ↔ Agent
```

实际大型系统可能同时使用：

```text
Agent A --MCP--> Database Tool
Agent A --A2A--> Agent B
Agent B --MCP--> Search Tool
```

## 9. MCP 安全反模式

### 自动信任所有 Server

错误。

### 给 Server 全量用户 Token

违反最小权限。

### MCP Tool 直接开放 Shell root

高危。

### Server Description 决定权限

Description 只帮助模型理解，不是权限机制。

## 10. 生产检查清单

- [ ] MCP Server 是否有明确 Owner？
- [ ] 是否固定兼容协议版本？
- [ ] Tool 是否业务语义化？
- [ ] 是否实现认证和授权？
- [ ] 是否按 Tenant 隔离？
- [ ] 是否有 Audit？
- [ ] 是否定义 Timeout、Rate Limit？
- [ ] 第三方 Server 是否经过安全审查？
- [ ] 高风险 Tool 是否需要 Approval？

## 11. 参考

- MCP 2026-07-28 Specification Release：https://blog.modelcontextprotocol.io/posts/2026-07-28/
- MCP 官方站点：https://modelcontextprotocol.io/
