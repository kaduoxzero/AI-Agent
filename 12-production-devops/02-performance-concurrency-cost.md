# Agent 性能工程：并发、缓存、预算、模型路由与成本

## 1. Agent 性能不是只看响应时间

需要同时优化：

```text
Quality
Latency
Cost
Throughput
Reliability
```

很多优化会互相冲突。

## 2. Latency 分解

一次任务耗时：

```text
Queue Wait
+ Model Latency
+ Tool Latency
+ Retrieval
+ Sandbox Startup
+ Serial Dependencies
+ Human Wait（单独统计）
```

必须通过 Trace 找瓶颈，而不是猜。

## 3. 并行

优先识别 DAG 中无依赖任务：

```text
Search A ─┐
Search B ─┼→ Synthesis
Search C ─┘
```

但并行度过高会触发：

- Provider Rate Limit；
- DB Connection Exhaustion；
- Queue Spike；
- Cost Spike。

所以需要 `max_parallelism`。

## 4. Async

Python 网络 I/O 使用 async 可以提高单 Worker 并发能力。

但：

- CPU 密集任务仍需要进程 / 专门 Worker；
- 同步 SDK 会阻塞 event loop；
- Agent Context 需要正确传播。

## 5. Backpressure

**专业名词通义：Backpressure**

下游处理不过来时，上游主动减速或排队，而不是无限创建任务。

实现：

- Queue max length；
- semaphore；
- rate limiter；
- admission control。

## 6. Cache

### Model / Prompt Cache

缓存重复固定前缀或请求（根据厂商能力）。

### Retrieval Cache

相同 Query / index version 缓存检索结果。

### Tool Cache

只适合幂等、允许短期陈旧的 Read Tool。

### Embedding Cache

避免重复计算同一内容 Embedding。

## 7. Cache Key

必须包含影响结果的维度：

```text
model_version
prompt_version
knowledge_version
tenant_id
permission_scope
query
```

否则可能数据串租户。

## 8. Token Optimization

主要手段：

- Context Selection；
- Compaction；
- Tool Result Summarization；
- 不重复注入 Tool Schema；
- Skill 按需加载；
- 小模型 Router；
- Evidence top-k 控制。

## 9. Model Routing

典型：

```text
cheap fast model → classify / route
standard model → normal worker
strong reasoning → planner / difficult retry
```

不要把所有请求直接升级强模型。

## 10. Budget

每个 Task 有预算：

```yaml
max_turns: 30
max_llm_calls: 40
max_tool_calls: 60
max_cost_usd: 2
max_duration: 300s
```

每个 SubAgent 还可以有子预算。

Orchestrator 总预算不能被 Worker 分别无限透支。

## 11. Cost Attribution

成本按：

```text
tenant
user
task
agent
node
model
tool
```

归因。

这样才能找到“哪个 Pattern 太贵”。

## 12. Rate Limit

Provider 可能同时限制：

- requests/min；
- tokens/min；
- concurrent requests。

需要集中 Model Gateway 管理，不要每个 Worker 各自盲目 retry。

## 13. Timeout 层级

```text
Tool Timeout < Node Timeout < Task Timeout
```

避免 Tool 比 Task 总预算还长。

## 14. SLO

为 Agent 服务定义：

```text
Task success >= 95%
P95 first progress < 2s
P95 simple task < 15s
Cancellation effective < 5s
```

长 Research Task 不适合只定义传统接口 500ms SLO。

## 15. 检查清单

- [ ] 是否用 Trace 分解 Latency？
- [ ] 是否设置 max_parallelism？
- [ ] 是否有 Backpressure？
- [ ] Cache 是否 Tenant/Permission 隔离？
- [ ] 是否有 Task Budget？
- [ ] 成本是否按 Node / Agent 归因？
- [ ] Rate Limit 是否集中治理？
