# Shared Schemas：Agent 系统数据契约

> 大型 Agent 系统应该优先共享“Schema”，而不是共享“聊天记录”。本目录用于沉淀跨 Agent、Runtime、前端、Eval 和存储层都能复用的稳定数据契约。

## 1. 为什么需要 schemas/

如果每个模块都自行定义：

```text
Task
Plan
Evidence
Artifact
Event
Approval
ToolResult
```

很快会出现字段含义冲突、Trace 无法关联、Checkpoint 无法升级、Multi-Agent 输出难以复用的问题。

## 2. 推荐 Schema

```text
schemas/
├─ task.schema.json
├─ plan.schema.json
├─ evidence.schema.json
├─ artifact.schema.json
├─ runtime-event.schema.json
├─ tool-call.schema.json
├─ approval.schema.json
├─ agent-definition.schema.json
└─ eval-result.schema.json
```

## 3. Task Contract

建议字段：

```text
task_id
tenant_id
user_id
agent_id
agent_version
status
priority
budget
created_at
updated_at
trace_id
```

状态至少：

```text
CREATED
QUEUED
RUNNING
WAITING_APPROVAL
CANCELLING
CANCELLED
FAILED
COMPLETED
```

## 4. Plan Contract

```json
{
  "plan_id": "p1",
  "version": 1,
  "nodes": [
    {
      "id": "n1",
      "type": "research",
      "depends_on": [],
      "status": "pending"
    }
  ]
}
```

Plan 应支持 DAG、节点级 Retry 和 Artifact Reference。

## 5. Evidence Contract

必须能够回答：

```text
哪个 Claim？
来自哪里？
何时获取？
属于哪个 Tenant？
原始资源是什么？
```

不要只保留一段模型总结文本。

## 6. Runtime Event Contract

统一 Event Envelope：

```json
{
  "event_id": "evt_123",
  "event_type": "TOOL_COMPLETED",
  "task_id": "task_1",
  "trace_id": "trace_1",
  "timestamp": "...",
  "sequence": 42,
  "payload": {}
}
```

所有 UI、Trace、Replay、Eval 都可以基于统一 Envelope。

## 7. Approval Contract

至少：

```text
approval_id
task_id
action
resource
requested_by_agent
requested_for_user
risk_level
reason
evidence_refs
status
reviewer
expires_at
```

Approval 不应该只是一个 `bool approved`。

## 8. Agent Definition Contract

```text
agent_id
version
owner
model_policy
prompt_version
tools
skills
runtime_policy
security_policy
memory_policy
```

这是 Control Plane 的核心资产。

## 9. Schema Versioning

每个长期持久化 Schema 都要版本化。

推荐：

```text
schema_name
schema_version
```

规则：

- 新增可选字段优先兼容；
- Breaking Change 必须升级 Major；
- Checkpoint 恢复要提供 Migration；
- Consumer 明确支持版本范围；
- CI 验证兼容性。

## 10. 目录未来应加入的真实文件

当对应 Lab 开始实现时，把 Pydantic / Zod / JSON Schema 的正式定义提交到本目录，而不是复制在多篇文档中。

## 11. 验收标准

- [ ] Task / Event / Artifact 有唯一 ID；
- [ ] 所有持久化结构有 Schema Version；
- [ ] Tenant ID 不依赖 Context 隐式传递；
- [ ] Evidence 可追溯；
- [ ] Approval 有完整审计字段；
- [ ] Runtime Event 可以排序 / Replay；
- [ ] Agent Definition 可版本化部署。