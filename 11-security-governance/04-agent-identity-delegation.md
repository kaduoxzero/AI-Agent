# Agent Identity、Delegation 与 Authorization

> 目标：解决生产级 Agent 最容易被忽视的问题——Agent 到底“代表谁”访问资源，它自己的身份是什么，它能否把权限继续委派给其他 Agent 或 Tool。

## 1. 为什么普通 API Key 模型不够

Demo 常见写法：

```text
Agent
  ↓
ADMIN_API_KEY
  ↓
所有系统
```

这在生产环境中风险极高，因为：

- 无法区分是哪个 Agent 执行；
- 无法知道它是否代表某个用户；
- 无法做最小权限；
- 无法在 Agent 被攻陷后缩小爆炸半径；
- Multi-Agent 委派时权限边界不清楚；
- 审计日志只能看到“某应用调用了 API”。

## 2. 专业名词通义

- **Identity（身份）**：系统中“谁正在发起操作”的可验证主体。
- **Authorization（授权）**：这个身份允许做什么。
- **Delegation（委派）**：一个主体把受限能力交给另一个主体代为执行。
- **On-Behalf-Of（OBO，代表用户）**：Agent 以自己的执行身份工作，但代表已认证用户访问被授权资源。
- **Workload Identity（工作负载身份）**：服务、Pod、Job 等非人工作负载使用的身份。
- **Agent Identity（智能体身份）**：专门代表一个 Agent 实例或逻辑 Agent 的非人身份。
- **Scope（权限范围）**：Token 被允许访问的资源或动作范围。

## 3. 应区分哪些身份

大型系统至少要区分：

```text
Human User Identity
Application Identity
Workload Identity
Agent Identity
Tool / Service Identity
Resource Identity
```

不要把它们全部压缩成一个 `user_id`。

## 4. Agent 代表用户时的信任链

```text
User
 ↓ Authenticate
Frontend / API
 ↓
Agent Runtime
 ↓ Agent Identity + delegated user context
Tool Gateway
 ↓ scoped token
Business API
```

审计时应该能够回答：

```text
谁提出了任务？
哪个 Agent 执行？
哪个 Agent Version？
代表哪个用户？
调用了哪个 Tool？
使用了什么 Scope？
最终修改了哪个 Resource？
```

## 5. Autonomous Agent 与 Interactive Agent

### Interactive Agent

由用户当前会话触发。

```text
User → Agent → Resource
```

授权可以与当前用户上下文绑定。

### Autonomous Agent

例如定时任务、监控 Agent：

```text
Scheduler → Agent → Resource
```

此时没有在线用户，必须使用明确的 Agent / Workload Identity，并限制其长期权限。

## 6. Delegation Chain

Multi-Agent 最危险的设计之一：

```text
Agent A 有权限
 ↓
把自己的完整 Token 给 Agent B
 ↓
Agent B 再给 Agent C
```

正确思路是：

```text
Agent A
 ↓ request constrained delegation
Identity / Credential Broker
 ↓ short-lived scoped token
Agent B
```

委派应收窄，而不是放大权限。

建议规则：

```text
child_scopes ⊆ parent_scopes
child_duration <= parent_duration
child_resource_scope <= parent_resource_scope
```

## 7. Token 设计原则

推荐：

- Short-lived；
- Audience 限定；
- Scope 最小化；
- 不写入 Prompt；
- 不写入长期 Memory；
- Tool 执行时临时获取；
- Secret Broker / Credential Broker 集中管理。

禁止：

```text
把 Bearer Token 塞进 Agent Context
把管理员密钥放进 System Prompt
把 Cloud Secret 返回给模型
```

## 8. Tool Gateway

对于高权限企业系统，建议：

```text
Agent
 ↓ logical tool call
Tool Gateway
 ├─ authenticate agent
 ├─ resolve user delegation
 ├─ evaluate policy
 ├─ acquire downstream credential
 ├─ execute
 └─ audit
```

这样模型不直接持有数据库密码、OAuth Refresh Token 等真实凭据。

## 9. 权限模型

### RBAC

按照角色授权：

```text
research-agent → read-public-data
billing-agent → read-invoice
```

### ABAC

根据属性：

```text
if agent.department == resource.department
and action == "read"
and risk < threshold
```

### Policy-Based Authorization

对于 Agent 更推荐把这些信息一起评估：

```text
User
Agent
Tool
Action
Resource
Tenant
Risk
Time
Environment
```

## 10. Agent Identity 生命周期

```text
Provision
 ↓
Assign owner / sponsor
 ↓
Grant policy
 ↓
Run / Monitor
 ↓
Rotate / Review
 ↓
Disable / Revoke
 ↓
Delete
```

无人负责的 Agent Identity 应视为安全问题。

## 11. 与 MCP / A2A 的关系

协议解决“怎么通信”，Identity 解决“你是谁、能做什么”。

```text
MCP ≠ Authentication System
A2A ≠ Authorization System
```

跨 Agent / Tool 通信时仍需要：

- identity；
- credential；
- policy；
- audit。

## 12. 企业落地示例

采购 Agent 想执行 `create_purchase_order`：

```text
1. User 提交请求
2. Agent Runtime 识别 agent_id
3. Policy 检查 user + agent + amount
4. amount > 10000 → HITL
5. Approval 通过
6. Credential Broker 下发 60 秒 scoped token
7. Tool Gateway 调采购 API
8. Audit 保存 actor=user, agent, approval_id, resource
```

## 13. 检查清单

- [ ] 每个生产 Agent 是否有独立 Identity？
- [ ] 是否能区分 Agent 自主行为与代表用户的行为？
- [ ] 委派是否只会缩小权限？
- [ ] Agent 是否永远看不到长期 Secret？
- [ ] Token 是否 short-lived + audience-bound？
- [ ] Tool Gateway 是否统一做 Policy 与 Audit？
- [ ] Agent Identity 是否有 Owner、生命周期和吊销机制？

## 14. 参考方向

- Microsoft Entra Agent ID：企业级 Agent 身份、治理与 OAuth 模型；
- OAuth 2.x / Token Exchange / OBO；
- Workload Identity Federation；
- Zero Trust 与最小权限。