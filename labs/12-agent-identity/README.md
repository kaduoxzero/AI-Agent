# Lab 12｜Agent Identity：Delegation、Scoped Credential 与最小权限

> 目标：让 Agent 访问 Tool / Resource 时拥有可审计、可过期、范围受限的身份，而不是所有 Agent 共用一个管理员 API Key。

## 1. 学习目标

完成后应能够：

- 区分 User Identity、Agent Identity、Tool Identity；
- 建模 Delegation：用户允许 Agent 代表自己做哪些事；
- 由 Credential Broker 颁发短期 Scoped Credential；
- 确保 Agent 不能获得用户未委派的 Scope；
- 确保 Credential 过期后不能继续使用；
- 记录 `who → delegated to whom → called what` 的审计链。

## 2. 专业名词通义

- **Delegation**：用户或上游主体把有限权限委派给 Agent，而不是把完整身份交出去。
- **Scoped Credential**：只包含特定权限范围的凭据。
- **Short-lived Credential**：有效时间很短的 Token / Credential，降低泄漏后的影响范围。
- **Credential Broker**：根据 Identity、Policy、Delegation 动态签发访问凭据的服务。
- **On-Behalf-Of（OBO）**：Agent 代表用户调用下游资源的身份链模式。

## 3. 运行

```bash
cd labs/12-agent-identity
python app.py
```

## 4. 实验模型

```text
User Identity
  scopes: supplier:read, supplier:write
        ↓ delegates only read
Agent Identity
  requested: supplier:read
        ↓
Credential Broker
        ↓
short-lived token
  scopes: supplier:read
        ↓
Tool Gateway
```

Agent 请求 `supplier:delete` 时必须失败，即使模型强烈要求。

## 5. 工程原则

Credential 不应进入模型 Context：

```text
Model
 ↓ Tool Intent
Runtime / Tool Gateway
 ↓
Credential Broker
 ↓
Short-lived Credential
 ↓
Resource
```

模型只需要知道“能不能调用”，不需要看到长期 Secret。

## 6. 生产化延伸

真实环境可映射到：

- OAuth 2.x Scope；
- Token Exchange；
- OBO；
- Workload Identity；
- SPIFFE / SPIRE；
- Cloud IAM；
- Secret Manager / Vault。

本实验用纯 Python 对象模拟授权语义，重点是建立正确边界。

## 7. 验收标准

- [ ] Agent Credential 有过期时间；
- [ ] Scope 是委派范围的子集；
- [ ] Agent 不能自行扩大 Scope；
- [ ] Tenant 不匹配时拒绝；
- [ ] Credential 不进入模型输入；
- [ ] 有完整 Audit Trail；
- [ ] 能解释为什么共享管理员 Key 会造成 Excessive Agency。
