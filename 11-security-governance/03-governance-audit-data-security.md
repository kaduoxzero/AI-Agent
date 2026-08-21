# Agent Governance、Audit、数据安全与供应链治理

## 1. 为什么大型 Agent 需要治理层

当组织里出现几十个 Agent、MCP Server、Skill、Model 和 Tool 时，仅靠代码仓库无法回答：

- 谁创建的？
- 谁能使用？
- 有什么权限？
- 使用哪个模型？
- 最近 Eval 如何？
- 是否处理敏感数据？
- 是否还能上线？

因此需要 Agent Governance。

## 2. Agent Registry

每个生产 Agent 建议登记：

```yaml
name: finance-research-agent
owner: finance-ai-team
version: 2.4.1
risk_level: high
models: [...]
tools: [...]
mcp_servers: [...]
data_classes: [internal, confidential]
last_eval: 2026-08-01
```

## 3. Tool / MCP / Skill Registry

同样维护：

- Owner；
- Version；
- Permissions；
- Risk Level；
- Allowed Agents；
- Security Review；
- Deprecation Date。

## 4. Audit

Audit 与 Debug Log 不同。

Audit 关注“谁在什么时候做了什么”。

至少记录：

```text
actor
agent
user
resource
action
decision
approval
timestamp
trace_id
result
```

高风险 Tool 的 Audit 应不可轻易篡改。

## 5. Data Classification

给数据分类：

```text
Public
Internal
Confidential
Restricted
```

然后控制：

- 哪个 Model Provider 可接收；
- 哪个 Agent 可读取；
- 是否允许写入 Memory；
- 是否允许 Trace 保存原文；
- 是否允许跨 Region。

## 6. Tenant Isolation

SaaS Agent 系统必须避免：

```text
Tenant A Memory → Tenant B
Tenant A RAG Document → Tenant B
Tenant A Tool Token → Tenant B
```

所有层都带 tenant_id：

```text
State
Memory
Vector Index / Filter
Checkpoint
Artifact
Trace
Cache
```

## 7. Retention

为不同数据定义生命周期：

```text
Conversation: 30 days
Trace metadata: 90 days
Sensitive tool payload: 7 days
Audit: according to compliance
```

不要默认永久保存 Prompt 和 Tool Result。

## 8. Supply Chain Governance

纳入：

- Model SDK；
- MCP Server；
- Skills；
- Prompt Package；
- Container Image；
- Browser Extension；
- Agent Template。

要求：

```text
source verification
version pinning
SBOM where applicable
security review
rollback
```

## 9. Change Management

任何生产变更：

```text
Prompt
Model
Tool
Skill
Workflow
Retriever
Permission
```

都应该：

```text
version → eval → security check → release
```

## 10. Kill Switch

高自治 Agent 必须有运营层紧急控制：

- 禁用 Agent；
- 禁用某个 Tool；
- 撤销 Token；
- 停止所有新 Task；
- 取消运行任务。

## 11. 检查清单

- [ ] 是否有 Agent / Tool / MCP / Skill Registry？
- [ ] 是否记录 Owner 和风险等级？
- [ ] Audit 与普通日志是否分开？
- [ ] 是否有数据分类？
- [ ] Tenant 是否全链路隔离？
- [ ] 是否定义 Retention？
- [ ] 第三方能力是否版本锁定？
- [ ] 是否存在 Kill Switch？
