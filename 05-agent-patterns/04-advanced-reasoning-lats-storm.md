# Self-Discover、LATS、STORM 与高级推理 / Research Pattern

## 1. 这些模式为什么放在一起

它们都不属于最基础的 Tool Loop，而是在复杂问题上引入“推理结构搜索、候选路径搜索或系统化研究”。成本明显更高，不应该默认使用。

## 2. Self-Discover

Self-Discover 的核心是：让模型根据任务选择并组合适合的 Reasoning Modules。

```text
Task
 ↓
Candidate Reasoning Modules
 ↓
Select
 ↓
Adapt
 ↓
Compose Structure
 ↓
Solve
```

### Reasoning Module

可复用的思考方法，例如：

- 问题分解；
- 因果分析；
- 反事实；
- 批判性检查；
- 约束排序。

它不是业务 Tool。

## 3. LATS

LATS = Language Agent Tree Search。

不是只走一条路径：

```text
              State
          /     |      \
       A        B       C
      / \      / \     / \
```

Agent 对多个候选 Action 进行：

```text
Generate
→ Execute / Simulate
→ Evaluate
→ Reflect
→ Expand promising branches
```

### MCTS

Monte Carlo Tree Search，蒙特卡洛树搜索。可以粗略理解为在多条候选路径间动态分配探索资源，更多尝试高价值分支。

### LATS 适用

- 高难度代码修复；
- 复杂决策；
- 有验证器的数学 / 逻辑；
- Web Navigation；
- 高价值但低频任务。

### 缺点

分支数 × 深度会快速放大模型调用和 Tool 调用。

必须限制：

```text
max_depth
max_branches
max_rollouts
max_cost
```

## 4. STORM

STORM 更适合 Research 与长文知识生成。

一个典型高层流程：

```text
Topic
 ↓
Discover Perspectives
 ↓
Generate Questions
 ↓
Retrieve Evidence
 ↓
Organize Knowledge
 ↓
Construct Outline
 ↓
Write Sections
 ↓
Review / Citation
```

### Perspective

针对同一主题从不同角色 / 角度生成研究问题。

例如 AI 医疗：

```text
临床
患者
医院运营
监管
技术
安全
```

## 5. Deep Research 与普通 Search Agent

普通 Search Agent：

```text
Search → summarize
```

Deep Research：

```text
Plan
→ Decompose
→ Multi-source Retrieval
→ Parallel Research
→ Evidence Store
→ Cross-check
→ Synthesis
→ Citation
```

STORM 可以作为其中一种知识组织 Pattern，而不是 Deep Research 唯一实现。

## 6. Candidate Search 的统一抽象

高级推理系统通常包含：

```text
Generator
Evaluator
Search Policy
State Store
Budget
Termination
```

不同 Pattern 只是搜索空间不同。

## 7. 什么时候不要用

以下任务通常不需要：

- FAQ；
- 普通 RAG；
- 简单工具调用；
- 固定流程；
- 延迟敏感客服。

## 8. 生产落地建议

高级 Pattern 必须先有基准版本。

例如：

```text
Baseline ReAct accuracy: 72%, cost: $0.05
LATS accuracy: 80%, cost: $0.80
```

如果业务不值得 16 倍成本，就不应采用。

## 9. 检查清单

- [ ] 是否有普通 Agent baseline？
- [ ] 高级搜索是否显著提升质量？
- [ ] 是否限制分支 / 深度 / 预算？
- [ ] 是否存在可靠 Evaluator？
- [ ] Research 是否保留 Evidence / Citation？
