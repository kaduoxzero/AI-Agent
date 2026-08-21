# Agent 权限、Identity、Guardrails 与 Human-in-the-Loop

## 1. Prompt 不是权限系统

错误设计：

```text
System Prompt:
“没有权限时不要调用管理员工具。”
```

如果 Tool API 没有真正验证权限，这不是安全控制。

## 2. Identity 分层

至少考虑：

```text
Human User Identity
Agent / Service Identity
Delegated Identity
Tool / Resource Identity
```

### User Delegation

Agent 代表用户执行任务时，权限不应自动超过用户本人。

## 3. Least Privilege

为 Agent 提供完成当前任务所需的最小权限。

例如 Research Agent：

```text
web.read
kb.read
```

不应该拥有：

```text
customer.delete
payment.execute
```

## 4. RBAC / ABAC

### RBAC

Role-Based Access Control，按角色授权。

### ABAC

Attribute-Based Access Control，根据用户、资源、环境等属性判断。

Agent 系统复杂场景通常 ABAC 更灵活：

```text
user.department == document.department
AND action == read
AND risk < high
```

## 5. Guardrail

Guardrail 是输入、输出或 Tool 层的检查机制。

```text
Input Guardrail
 ↓
Agent
 ↓
Tool Input Guardrail
 ↓
Tool
 ↓
Tool Output Guardrail
 ↓
Agent
 ↓
Output Guardrail
```

不要只在最终回答加一个 Safety Agent。

## 6. Deterministic Guardrail

优先使用：

- Schema Validation；
- Permission；
- regex / data detector；
- allowlist；
- rule engine；
- transaction limits。

LLM Guardrail 作为语义补充。

## 7. Human-in-the-Loop

HITL 适合：

- 删除；
- 转账；
- 发布；
- 医疗 / 法律高风险建议；
- 权限修改；
- 外发敏感信息；
- 高风险 Shell。

流程：

```text
Agent proposes Action
 ↓
Policy evaluates
 ↓
Approval Request
 ↓
Human approves/rejects/edits
 ↓
Execute
```

## 8. Approval Scope

一次审批只能覆盖明确 Action。

错误：

> 允许这个 Agent 以后做所有事情。

更安全：

```text
Approve tool=create_report
args hash=...
expires=5min
```

## 9. Don't-Ask-Again 风险

某些 Harness 提供“不再询问”工具审批体验。

生产使用时必须限定：

- Tool；
- Scope；
- Workspace；
- Session；
- 有效期。

否则便利功能会变成永久提权。

## 10. Policy Engine

大型平台建议独立：

```text
Agent Runtime
 ↓ action proposal
Policy Engine
├─ identity
├─ tool risk
├─ tenant policy
├─ data classification
└─ context
 ↓
allow / deny / require_approval
```

模型不直接控制 Policy Engine。

## 11. Secret Management

Agent 不应该在 Context 中看到不需要的 Secret。

推荐：

```text
Tool call
 ↓
Credential Broker
 ↓
Scoped short-lived token
 ↓
External API
```

模型只看到 Tool Result。

## 12. 检查清单

- [ ] Tool API 是否重新验证权限？
- [ ] 是否区分 User / Agent / Service Identity？
- [ ] 是否最小权限？
- [ ] Guardrail 是否覆盖 Tool 层？
- [ ] 高风险 Action 是否 HITL？
- [ ] Approval 是否限定 Scope 和时间？
- [ ] Secret 是否不进入模型 Context？
