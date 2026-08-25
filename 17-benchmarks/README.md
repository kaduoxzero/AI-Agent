# Agent Benchmark Framework

## 目标

建立统一 Agent 能力评估体系，而不是只评价最终文本。

## Benchmark Categories

|能力|指标|
|-|-|
|Planning|任务拆解正确率|
|Tool Use|工具调用成功率|
|RAG|检索准确率与引用质量|
|Memory|记忆召回质量|
|Coding|代码正确率|
|Safety|风险防护能力|
|Cost|Token 成本|
|Latency|响应时间|

## Evaluation Layers

```text
Output Evaluation
        ↓
Trajectory Evaluation
        ↓
Tool Evaluation
        ↓
System Evaluation
```

## Score Card

每个 Agent 应拥有：

- Capability Score
- Reliability Score
- Safety Score
- Cost Score
- Production Readiness Score
