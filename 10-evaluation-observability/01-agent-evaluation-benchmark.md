# Agent Evaluation 与 Benchmark：从最终答案到执行轨迹

## 1. 为什么 Agent Eval 比 LLM Eval 更难

普通生成任务常只评价 Output。

Agent 还需要评价：

```text
Input
 ↓
Planning
 ↓
Tool Selection
 ↓
Tool Arguments
 ↓
Trajectory
 ↓
Final Output
```

最终答案碰巧正确，不代表执行过程合理。

## 2. 四层 Eval

### 2.1 Component Eval

单个组件：

- Router accuracy；
- Retrieval recall；
- Tool argument correctness；
- Guardrail precision / recall。

### 2.2 Task Eval

整个任务是否完成。

### 2.3 Trajectory Eval

Agent 走的路径是否合理。

例如：

```text
Expected:
search → fetch → answer

Actual:
search → search → wrong_tool → retry → answer
```

虽然答案正确，但路径成本和风险更高。

### 2.4 System Eval

生产指标：

- P50 / P95 latency；
- cost / task；
- failure rate；
- human intervention rate；
- retry rate。

## 3. Golden Dataset

建立代表真实业务的测试集：

```json
{
  "input": "...",
  "expected": {...},
  "required_tools": ["search"],
  "forbidden_tools": ["delete"],
  "rubric": {...}
}
```

不要只用十个“漂亮案例”。

应覆盖：

- 正常；
- 边界；
- 歧义；
- Tool Failure；
- 数据缺失；
- 权限不足；
- Prompt Injection；
- 长 Context。

## 4. 指标

### Quality

- Task Success Rate；
- Accuracy；
- Completeness；
- Faithfulness；
- Citation Correctness。

### Agent Behavior

- Tool Success Rate；
- Tool Selection Accuracy；
- Invalid Tool Call Rate；
- Mean Steps；
- Unnecessary Steps；
- Handoff Accuracy。

### System

- Latency；
- Token；
- Cost；
- Retry；
- Timeout；
- Stability。

## 5. LLM-as-a-Judge

适用于难以用规则评价的开放文本。

必须使用 Rubric，例如：

```text
Correctness: 0-4
Evidence: 0-4
Completeness: 0-4
Safety: pass/fail
```

不要只问 Judge：

> 这个答案好吗？

## 6. Deterministic Eval

能确定性测试的尽量不用 Judge：

- JSON Schema；
- 单元测试；
- SQL 结果；
- 文件是否生成；
- 必须 Tool 是否调用；
- 禁止 Tool 是否调用。

## 7. Baseline

任何复杂 Pattern 上线前先有 baseline：

```text
Single Agent
vs
Reflection
vs
Multi-Agent
```

比较：

```text
Quality + Cost + Latency
```

如果 Multi-Agent 质量只提升 1%，成本提高 4 倍，通常不值得。

## 8. Online Eval

线上可以采集：

- user feedback；
- task abandon；
- human override；
- correction；
- escalation；
- sampled judge。

但线上数据涉及隐私和偏差，需要治理。

## 9. Regression Gate

每次修改：

```text
Prompt
Model
Tool
Skill
Retriever
Workflow
```

都应触发相关 Eval。

```text
Change
 ↓
Eval Suite
 ↓
Threshold Pass?
├─ YES → deploy
└─ NO → block
```

## 10. 检查清单

- [ ] 是否同时评 Output 和 Trajectory？
- [ ] 是否有 Golden Dataset？
- [ ] 是否覆盖 Tool Failure / Security Cases？
- [ ] 能确定性评估的是否使用确定性方法？
- [ ] Judge 是否有 Rubric？
- [ ] 是否比较 Quality / Latency / Cost？
- [ ] 部署是否有 Regression Gate？
