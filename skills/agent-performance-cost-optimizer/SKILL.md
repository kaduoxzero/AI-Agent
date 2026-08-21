---
name: agent-performance-cost-optimizer
description: Optimize Agent latency, throughput, concurrency, token usage, model calls, tool calls, retrieval cost, and infrastructure cost without silently reducing quality or safety. Use when an Agent is too slow, expensive, rate-limited, over-calling models/tools, or needs capacity planning and performance budgets.
---

# Agent Performance & Cost Optimizer

## Objective

在不破坏正确性、安全和可恢复性的前提下，系统性降低 Agent 的 **Latency、Token、Model Calls、Tool Calls、Cost**，并提高 Throughput。

## Core Rule

先测量，再优化。

禁止：

- 没有 Baseline 就换模型；
- 只看平均延迟；
- 只降 Token 不看质量；
- 为省一次模型调用破坏安全 Gate；
- 把所有步骤并行化。

## 1. Build Baseline

至少记录：

```text
Task Success Rate
Latency P50 / P95 / P99
Queue Wait
Model Latency
Tool Latency
Retrieval Latency
Input Tokens
Output Tokens
Model Calls / Task
Tool Calls / Task
Retry Count
Estimated Cost / Task
Peak Concurrency
```

按 Agent Version / Model Route / Task Type 分组。

## 2. Find Cost Centers

把总耗时拆成：

```text
API wait
+ Queue wait
+ Context build
+ Model planning
+ Retrieval
+ Tool execution
+ Model synthesis
+ Retry
+ Persistence
```

把总成本拆成：

```text
Prompt tokens
+ Completion tokens
+ Repeated context
+ Reflection rounds
+ Multi-Agent duplication
+ Retrieval / rerank
+ External APIs
```

## 3. Remove Unnecessary LLM Calls

优先删除可被确定性逻辑替代的调用：

- 路由规则；
- 权限检查；
- 状态转换；
- 简单字段转换；
- 阈值判断；
- JSON repair 中可程序化处理的部分。

每减少一个模型调用，都要确认没有丢失必要语义判断。

## 4. Context Optimization

检查：

- 重复 System Prompt；
- 重复 Tool Schema；
- 全量历史；
- 无关 Tool Results；
- 低价值 RAG chunks；
- 多 Agent 重复 Context。

使用：

- context selection；
- summarization / compaction；
- bounded memory；
- evidence deduplication；
- lazy capability loading；
- retrieval top-k optimization。

## 5. Model Routing

按任务能力路由：

```text
Simple classification → small/fast model
Structured extraction → structured-output-capable model
Tool planning → tool-capable model
Hard reasoning → reasoning model
Final synthesis → quality-appropriate model
```

必须通过 Eval 证明廉价模型没有破坏质量。

## 6. Parallelization

只并行无依赖步骤。

适合：

- 多来源检索；
- 多个只读 Tool；
- Map 阶段；
- 独立专家分析。

不适合：

- 依赖前一步 State；
- 共享副作用；
- 必须顺序执行的审批 / 写操作。

并行后必须处理 timeout、partial failure 和 cancellation。

## 7. Tool Optimization

检查：

- N+1 API calls；
- 重复 Tool 调用；
- 能否批量接口；
- 缓存；
- timeout；
- connection pooling；
- pagination；
- 重复副作用。

如果多个 Tool 调用本质是一个业务事务，考虑提供更高层 Tool，而不是让模型编排几十次底层调用。

## 8. RAG Optimization

优化顺序：

```text
Filter early
→ Better candidate recall
→ Smaller candidate set
→ Rerank
→ Deduplicate
→ Context budget
```

不要简单把 TopK 从 5 调到 50。

## 9. Multi-Agent Cost Review

检查每个 Agent 是否造成：

- 重复读取同一 Context；
- 重复检索；
- 重复判断；
- Supervisor 频繁 LLM routing；
- Debate 轮数过高；
- Final synthesis 多次重复。

如果 Multi-Agent 的增益不足以覆盖成本，降级为 Single Agent / Workflow。

## 10. Caching

只缓存可安全复用的数据：

- deterministic tool result；
- stable retrieval result；
- embedding；
- rerank result；
- static prompt fragments。

缓存 key 必须考虑：

- tenant；
- permission；
- version；
- freshness；
- model / prompt config。

不要跨租户错误共享缓存。

## 11. Retry Budget

Retry 会放大延迟和成本。

按错误类型决定：

- 429 → backoff / fallback；
- timeout → limited retry；
- validation → bounded repair；
- permission → no retry；
- bad request → no retry；
- safety block → no blind retry。

## 12. Capacity Planning

估算：

```text
Requests per minute
× Avg model calls
× Avg token volume
× Avg tool calls
× P95 task duration
```

据此设置：

- worker concurrency；
- queue capacity；
- provider rate limit；
- DB pool；
- Redis connection；
- autoscaling threshold。

## 13. Performance Gate

优化后必须比较 Baseline：

```text
Quality delta
Task success delta
P95 latency delta
Avg token delta
Avg cost delta
Safety delta
```

任何明显质量 / 安全回退都不能仅因成本下降而接受。

## Completion Criteria

- 有性能 Baseline；
- 找到主要 Cost Center；
- 优化有可归因的数据；
- P95 而非只有平均值被改善或受控；
- Token / Cost 有预算；
- Retry 不会无限放大；
- 并发有上限；
- 缓存不破坏权限隔离；
- Quality / Safety Regression 通过。
