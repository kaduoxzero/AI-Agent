# Reflection、Evaluator-Optimizer 与 Reflexion

## 1. 为什么需要反馈环

LLM 第一次生成的结果不一定达到要求。高质量任务经常需要：

```text
Generate
 ↓
Evaluate
 ↓
Feedback
 ↓
Revise
```

但不同模式的关键区别是“谁评、评什么、反馈是否进入长期经验”。

## 2. Basic Reflection

```text
Generator
 ↓
Draft
 ↓
Reflection
 ↓
Revision
```

可以由同一个模型 / Agent 完成。

适合：

- 文本润色；
- 简单代码自检；
- 报告完整性检查。

### 风险

同一个模型可能看不出自己原来的错误，即“自我确认偏差”。

## 3. Evaluator-Optimizer

将生成者和评估者职责分离：

```text
Generator
 ↓
Candidate
 ↓
Evaluator
 ↓ score + feedback
Pass?
├─ YES → Output
└─ NO → Generator revise
```

Evaluator 可以是：

- LLM Judge；
- 单元测试；
- 编译器；
- 规则引擎；
- 人工；
- 多种 Eval 组合。

### 关键工程思想

> 能用确定性 Evaluator，就不要只用另一个 LLM。

例如代码：

```text
LLM Review
+
Compile
+
Unit Test
+
Static Analysis
```

比“另一个 Agent 看一遍”可靠。

## 4. Threshold 与 Iteration

```text
score >= threshold → finish
iteration >= max_iterations → stop / escalate
```

必须同时存在质量阈值和最大循环次数。

否则：

```text
Writer ↔ Reviewer ↔ Writer ↔ Reviewer ...
```

可能无限循环。

## 5. Reflexion

Reflexion 的重点是把外部反馈转化为语言形式的经验，并用于后续尝试。

```text
Attempt
 ↓
Environment Feedback
 ↓
Reflection
 ↓
Episodic Memory
 ↓
Next Attempt
```

### 不是传统参数训练

Reflexion 通常不会在每次失败后更新模型权重，而是把反思存成可再次使用的 Memory。

### 示例

第一次代码 Agent：

```text
失败：修改 API 后忘记更新测试 fixture。
```

Reflection：

```text
对于影响 API Schema 的修改，执行前先搜索所有 fixture / mock，并在完成后运行契约测试。
```

下一次类似任务加载这条经验。

## 6. Feedback 的质量

垃圾 Feedback 会让 Generator 越改越差。

Evaluator 应使用 Rubric：

```json
{
  "correctness": 0.8,
  "completeness": 0.6,
  "evidence": 0.9,
  "issues": ["遗漏边界场景"],
  "pass": false
}
```

## 7. Multi-Evaluator

高风险任务可以并行：

```text
Candidate
├─ Safety Eval
├─ Factual Eval
├─ Format Eval
└─ Domain Eval
 ↓
Decision
```

并非每个 Evaluator 都要是 Agent。

## 8. 退出策略

推荐：

```text
PASS
OR max_iterations reached
OR budget exhausted
OR no improvement for N rounds
```

“连续无提升”是很实用的停止条件。

## 9. 三种模式对比

| 模式 | Evaluator | Memory | 适用 |
|---|---|---|---|
| Reflection | 常由自己 | 无/短期 | 简单自检 |
| Evaluator-Optimizer | 独立 Evaluator | 可选 | 高质量迭代 |
| Reflexion | 外部反馈 + 反思 | 强调 Episodic Memory | 多次尝试学习 |

## 10. 检查清单

- [ ] Evaluator 是否有明确 Rubric？
- [ ] 能否使用确定性测试？
- [ ] 是否有 Threshold？
- [ ] 是否有最大迭代？
- [ ] 是否检测无改进循环？
- [ ] Reflexion Memory 是否可追溯和可删除？
