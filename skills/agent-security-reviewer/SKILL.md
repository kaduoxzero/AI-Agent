---
name: agent-security-reviewer
version: 1.1.0
description: Review and harden Agent systems against prompt injection, tool abuse, privilege escalation, cross-tenant leakage, unsafe side effects, secret exposure, untrusted retrieval content, insecure approvals, and weak audit boundaries. Use before production release, when adding tools or RAG, or after any security-sensitive architecture change.
---

# Agent Security Reviewer

## Objective

把 Agent 当成一个 **会读取不可信内容、会调用工具、会代表用户执行动作的软件系统** 来审查，而不是只审 Prompt。

## Threat Model First

先回答：

```text
Who is the user?
What data can the Agent read?
What tools can it call?
What side effects can it cause?
What external content is untrusted?
What secrets exist?
What tenant boundaries exist?
What actions require human approval?
```

## 1. Identity Boundary

必须区分：

- End User Identity；
- Tenant Identity；
- Agent Identity；
- Service Identity；
- Human Approver Identity。

不要让模型自己声明“我是管理员”。

身份应由受信任边界注入。

## 2. Authorization

权限判断使用确定性代码：

```text
Identity
→ Policy
→ Scope
→ Tool Gateway
→ Action
```

不要使用：

```text
Prompt: “如果用户没有权限，请不要调用这个工具。”
```

作为唯一权限机制。

## 3. Tool Least Privilege

每个 Agent 只允许必要 Tool。

每个 Tool 只允许必要 Scope。

高风险 Tool 识别：

- database write / delete；
- payment；
- message / email send；
- file delete；
- shell；
- browser authenticated action；
- account / permission change；
- external system mutation。

## 4. Prompt Injection Boundary

以下内容默认不可信：

- 用户输入；
- Web 页面；
- RAG 文档；
- Email；
- PDF；
- Tool Result；
- 第三方 Agent 消息。

不可信内容只能作为 Data，不得自动成为 System Policy。

## 5. RAG Security

检查：

- tenant filter 在检索前执行；
- document ACL；
- malicious instruction in documents；
- citation traceability；
- index poisoning；
- stale permissions；
- sensitive metadata leakage。

测试至少包含恶意知识库文档。

## 6. Secret Handling

禁止：

- 把 API Key 写入 Prompt；
- 把 Secret 放入 Agent Memory；
- 在 Trace / Log 中打印完整 Token；
- 让模型决定该返回哪个 Secret。

Secret 应只存在于执行层受控环境。

## 7. HITL

高影响动作进入 Human-in-the-Loop。

审批必须包含：

```text
requested action
parameters
risk reason
requesting user
agent identity/version
approver identity
decision
timestamp
```

审批后恢复时要确认批准的是 **同一动作和参数**。

## 8. Side-Effect Safety

具有副作用的操作必须考虑：

- idempotency；
- dry-run；
- transaction；
- rollback；
- confirmation；
- audit。

## 9. Multi-Tenant Isolation

验证：

- API 查询；
- Task Store；
- RAG；
- Memory；
- Artifact；
- Event Stream；
- Cache；
- Logs。

跨租户对象访问优先返回不泄露存在性的错误。

## 10. Sandbox

执行 Shell / Code / Browser 时限制：

- filesystem scope；
- network scope；
- process lifetime；
- CPU / memory；
- timeout；
- credentials；
- writable paths；
- command allow/deny policy。

## 11. Audit

安全相关动作必须可追溯：

```text
trace_id
task_id
actor
agent/version
tool
action
resource
decision
policy
approval
result
```

## 12. Security Regression Dataset

至少包含：

- direct prompt injection；
- indirect injection from RAG；
- tool escalation；
- cross-tenant object access；
- cross-tenant retrieval；
- fake admin claim；
- approval bypass；
- secret exfiltration request；
- duplicate side-effect request；
- malicious Tool output。

## Severity

- **Critical**：可导致跨租户泄露、任意执行、严重不可逆副作用；
- **High**：可越权调用高影响 Tool、绕过审批；
- **Medium**：信息泄露、审计缺失、弱边界；
- **Low**：Defense-in-Depth 改善。

## Fail-Closed Rule

以下情况默认拒绝或进入审批：

- identity 缺失；
- permission 不确定；
- tool scope 不匹配；
- high-risk action 未审批；
- policy engine 失败；
- output schema 无法验证。

## Anti-Patterns

- “模型很聪明，不会被注入”；
- 所有 Agent 共用管理员 Token；
- RAG 先全库召回再让 LLM 过滤权限；
- Tool Permission 只靠 Prompt；
- 审批按钮批准后允许 Agent 换参数；
- 把完整用户数据写入公共 Trace。

## Report Back to Master

审查完成后，按 `../agent-engineering-master/SKILL-REGISTRY.md` 的 Return Contract 返回；Severity 分级结果、Fail-Closed 缺口与 Security Regression Dataset 覆盖情况应写入 Verification Performed 与 New Risks。

---

## Completion Criteria

- Threat Model 已建立；
- Identity / Authorization 不依赖 LLM；
- Tool 最小权限；
- RAG 有 ACL 与注入测试；
- 高风险操作有 HITL；
- Side Effect 有幂等或恢复策略；
- 多租户隔离有自动测试；
- 安全事件可审计；
- Critical / High 问题清零后才允许生产发布。
