# Agent Memory Engineering：从会话历史到长期记忆

## 1. Memory 解决什么问题

模型本身不会因为一次 API 调用自动永久记住用户或任务。

Memory 用于保存以后仍然有价值的信息。

## 2. Memory 分类

### Working Memory

当前任务临时工作信息。

### Short-Term Memory

当前 Session 内需要保留的信息。

### Long-Term Memory

跨 Session 仍需保存的信息。

### Episodic Memory

过去发生过什么，例如：

> 上一次部署失败，因为数据库 Migration 未执行。

### Semantic Memory

稳定知识和事实。

### Procedural Memory

“如何做某件事”的经验或操作流程，常与 Skill 重叠。

## 3. Memory ≠ Conversation History

直接无限保存聊天历史会导致：

- Token 增长；
- 隐私风险；
- 错误信息长期污染；
- 检索噪声。

Memory 应经过选择和治理。

## 4. Memory Write Policy

Agent 不应该把每句话都存为长期记忆。

写入前判断：

```text
Is it stable?
Is it useful later?
Is it allowed to store?
Does it conflict with existing memory?
What is the TTL?
```

## 5. Memory Schema

例如：

```json
{
  "memory_id": "...",
  "subject": "user:123",
  "type": "preference",
  "content": "prefers concise technical answers",
  "source": "conversation:456",
  "confidence": 0.95,
  "created_at": "...",
  "expires_at": null
}
```

## 6. Memory Retrieval

不要把全部 Memory 注入 Context。

```text
Current Task
 ↓
Memory Query
 ↓
Relevant Memory
 ↓
Context Builder
```

可以结合：

- metadata filter；
- semantic search；
- recency；
- confidence。

## 7. Consolidation

多个相似 Memory 可以合并：

```text
Memory A
Memory B
Memory C
 ↓ consolidate
Stable Memory
```

避免碎片无限增长。

## 8. Forgetting / TTL

长期 Memory 需要遗忘机制：

- TTL；
- 用户删除；
- 过期检测；
- 置信度衰减；
- 业务状态更新。

## 9. Conflict Resolution

例如：

```text
旧 Memory：用户使用 Python 3.10
新 Memory：用户已升级 Python 3.13
```

不能两条同时当真。

需要：

- 时间；
- 来源优先级；
- 显式覆盖；
- 冲突状态。

## 10. Memory Poisoning

外部恶意内容或错误模型输出如果进入长期 Memory，会跨 Session 持续影响 Agent。

防护：

```text
Untrusted Input
 ↓
Validation / Policy
 ↓
Memory Candidate
 ↓
Write Decision
 ↓
Memory Store
```

高价值长期 Memory 可以要求用户或业务系统确认。

## 11. Memory Store 设计

可能组合：

```text
PostgreSQL → structured memory
Vector DB → semantic retrieval
Redis → short-term / session cache
Object Store → large artifacts
```

不要为了 Memory 强行使用单一 Vector DB。

## 12. Multi-Agent Memory

区分：

```text
Global Memory
Team Memory
Agent-local Memory
User Memory
Task Memory
```

不是所有 Agent 都应该读全部 Memory。

## 13. 检查清单

- [ ] 什么信息允许进入长期 Memory？
- [ ] 是否有 Memory Schema？
- [ ] 是否有 TTL / 删除？
- [ ] 是否处理冲突？
- [ ] 是否记录来源？
- [ ] Memory 是否按权限隔离？
- [ ] 是否防止 Prompt Injection 写入长期 Memory？
- [ ] 是否定期评估 Memory 命中质量？
