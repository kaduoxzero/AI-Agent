# Workflow Pattern：Prompt Chaining、Routing、Parallelization、MapReduce 与 Orchestrator-Workers

## 1. 为什么先学 Workflow Pattern

很多所谓“Agent 系统”本质上首先是一个 Workflow。理解控制流后，再决定哪些节点需要 Agent 自主决策，系统会更可控。

## 2. Prompt Chaining

```text
Input
 ↓
Step A
 ↓
Step B
 ↓
Step C
 ↓
Output
```

### 适用

- 大纲 → 正文 → 审核；
- 需求 → 设计 → 代码；
- 抽取 → 归一化 → 入库。

### 优点

- 可预测；
- 易测试；
- 容易定位错误。

### 缺点

流程写死，对开放任务适应性较差。

## 3. Routing

```text
                 ┌→ Research
Input → Router ──┼→ Data
                 └→ Direct Answer
```

Router 可以由：

- 规则；
- 小模型；
- Structured Output；
- Embedding 分类器。

### 专业名词通义：Routing

根据当前输入或 State 决定下一条执行路径。

### 工程建议

Router 输出必须结构化，例如：

```json
{
  "route": "data",
  "confidence": 0.94
}
```

低置信度可以进入 fallback route。

## 4. Parallelization

无依赖任务应该并行：

```text
Task
├─ A ─┐
├─ B ─┼→ Join
└─ C ─┘
```

适合：

- 多角度分析；
- 多搜索源；
- 多数据查询；
- 多个独立章节。

### Serial vs Parallel vs Concurrency

- **Serial**：一个完成后下一个开始；
- **Parallel**：多个任务真实同时执行；
- **Concurrency**：系统能够交错处理多个任务，网络 I/O 场景常通过 async 实现。

## 5. MapReduce

核心：

> 拆开做，再合起来。

```text
Documents
 ↓ fan-out
Mapper A
Mapper B
Mapper C
 ↓ fan-in
Reducer
 ↓
Result
```

### 专业名词通义

- **Mapper**：对每个分片执行相同类型任务；
- **Reducer**：汇总 Mapper 结果；
- **Fan-out**：一个输入动态分发成多个任务；
- **Fan-in**：多个结果重新聚合。

### 适用

- 1000 篇文档总结；
- 多日志分析；
- 大型 Repo 分区审查；
- 大量患者 / 设备批处理。

### Reduce 的风险

Reducer Context 可能再次爆炸。

可以使用分层 Reduce：

```text
1000 results
 ↓
20 group summaries
 ↓
5 regional summaries
 ↓
Final summary
```

## 6. Orchestrator-Workers

```text
Task
 ↓
Orchestrator
├─ Worker 1
├─ Worker 2
└─ Worker 3
 ↓
Synthesis
```

与固定 Parallelization 不同，Worker 数量和任务在运行时由 Orchestrator 动态决定。

### Orchestrator 负责

- 理解目标；
- Task Decomposition；
- 选择 Worker；
- 分配输入；
- 检查子结果；
- 决定是否继续；
- 汇总。

### Worker 负责

一个清晰、边界明确、可以独立完成的任务。

好的 Worker Task：

```json
{
  "task_id": "sub-3",
  "goal": "分析最近30天供应链新闻",
  "constraints": ["必须引用来源"],
  "output_schema": "EvidenceReport"
}
```

## 7. 五种模式对比

| Pattern | 控制流 | 动态程度 | 并行 | 典型场景 |
|---|---|---:|---:|---|
| Chaining | 固定 | 低 | 否 | 固定流水线 |
| Routing | 条件 | 中 | 可选 | 意图分流 |
| Parallel | 固定/动态 | 中 | 是 | 独立任务 |
| MapReduce | 数据驱动 | 中 | 是 | 大批量同构任务 |
| Orchestrator-Workers | Agent 驱动 | 高 | 常见 | 动态复杂任务 |

## 8. 生产约束

所有循环 / 动态派发必须定义：

```text
max_tasks
max_parallelism
max_iterations
max_cost
max_time
```

否则 Worker 数量可能失控。

## 9. 检查清单

- [ ] 可以并行的任务是否仍在串行？
- [ ] Router 是否有低置信度处理？
- [ ] MapReduce 是否考虑 Reduce Context？
- [ ] Worker Task 是否独立且边界明确？
- [ ] Orchestrator 是否有限制最大派发数量？
