# Agent 架构选型：从函数、Workflow 到 Multi-Agent

## 1. 最重要的原则

> 如果普通函数能完成，不用 LLM；如果固定 Workflow 能完成，不要强行自治 Agent；如果 Single Agent 能完成，不要强行 Multi-Agent。

Agent 架构设计不是比谁“AI 味更浓”，而是选择最低复杂度、可满足业务目标的方案。

## 2. 五级复杂度模型

### Level 0：普通程序

```text
Input → Code → Output
```

适用于：

- 权限校验；
- 金额计算；
- 数据转换；
- 硬规则；
- CRUD；
- 事务逻辑。

### Level 1：单次 LLM

```text
Input → Prompt → Model → Output
```

适用于：摘要、分类、改写、信息抽取。

### Level 2：Workflow

```text
Input → Step A → Step B → Branch → Step C
```

流程主要由代码决定。

适用于：

- 报告生成；
- 审核流水线；
- 固定 RAG；
- 内容加工。

### Level 3：Single Agent

模型动态决定下一步：

```text
Task
 ↓
Reason / Decide
 ↓
Tool
 ↓
Observation
 ↓
Next Action
```

适用于：

- 搜索研究；
- Coding；
- 多工具任务；
- 动态排障。

### Level 4：Multi-Agent

```text
                    ┌→ Research Agent
User → Orchestrator ┼→ Data Agent
                    └→ Reviewer Agent
```

适用于真正存在独立职责、工具和上下文的复杂任务。

## 3. Workflow 与 Agent 的本质区别

| 维度 | Workflow | Agent |
|---|---|---|
| 下一步谁决定 | 程序 | 模型 + 状态 |
| 控制性 | 高 | 相对低 |
| 行为可预测性 | 高 | 较低 |
| 适合任务 | 固定流程 | 开放任务 |
| 测试难度 | 较低 | 较高 |
| 成本 | 较低 | 通常较高 |

### 专业名词通义

- **Deterministic（确定性）**：相同输入通常沿固定逻辑得到可预测输出。
- **Agentic（智能体式）**：允许模型参与决定控制流或 Action。
- **Autonomy（自主性）**：Agent 在无需人工指定每一步的情况下完成任务的程度。

## 4. 什么时候应该拆 Multi-Agent

满足多个条件时再拆：

### 4.1 不同目标

例如：

```text
Research Agent：搜集证据
Risk Agent：风险判断
Reviewer Agent：审查结论
```

### 4.2 不同工具权限

例如：

- 查询 Agent 只有 Read Tool；
- Action Agent 才允许 Write；
- Approval Agent 不接触业务数据，只做审查。

### 4.3 不同上下文

Coding Agent 不需要看到全部财务文档；Risk Agent 也不应该收到完整源代码。

### 4.4 可以独立执行

好的 Worker Task 应该是：

```text
输入明确
范围明确
完成标准明确
输出 Schema 明确
```

## 5. 不应该拆 Agent 的情况

以下通常只是函数或 Tool：

- JSON Parser Agent；
- Date Format Agent；
- SQL Execute Agent；
- Email Send Agent。

如果某个组件不需要自主判断，只是执行确定操作，就更适合作为 Tool。

## 6. Pattern 快速选择

| 需求 | Pattern |
|---|---|
| 固定步骤 | Prompt Chaining |
| 根据类型分流 | Routing |
| 独立任务同时执行 | Parallelization |
| 大量同构任务 | MapReduce |
| 边查边判断 | ReAct |
| 长任务先规划 | Plan & Solve |
| 多工具减少模型往返 | ReWOO |
| 有依赖的工具并行 | LLMCompiler |
| 生成后检查 | Reflection |
| 独立评估者反复优化 | Evaluator-Optimizer |
| 从失败经验中改进 | Reflexion |
| 复杂多路径搜索 | LATS |
| 深度研究 / 长文 | STORM |
| 一个经理动态拆任务 | Orchestrator-Workers |
| 专家依次处理 | Chain-of-Experts |
| 不同观点比较 | Debate |
| 多模型决策 | Voting / Ensemble |
| Agent 自由转交 | Handoff |

## 7. 生产架构决策树

```text
问题能否由普通程序可靠解决？
├─ YES → 普通代码
└─ NO
   ↓
单次模型是否足够？
├─ YES → LLM Call
└─ NO
   ↓
执行路径是否可提前确定？
├─ YES → Workflow
└─ NO
   ↓
是否需要动态 Tool / Planning？
├─ YES → Single Agent
└─ NO → 重新评估是否真的需要 Agent

Single Agent 是否存在明显职责冲突或 Context 膨胀？
├─ NO → 保持 Single Agent
└─ YES → Multi-Agent
```

## 8. 架构评审指标

选择方案时至少比较：

```text
Quality
Latency
Token Cost
Tool Calls
Failure Rate
Controllability
Security
Observability
Maintainability
```

不要只比较“回答质量”。

## 9. 落地检查清单

- [ ] 哪些逻辑可以由普通代码完成？
- [ ] 哪些步骤真的需要模型决策？
- [ ] Agent 是否拥有明确终止条件？
- [ ] Tool 是否遵循最小权限？
- [ ] 是否可以将并行任务并行执行？
- [ ] 是否需要持久化 State？
- [ ] 是否需要人工审批？
- [ ] 是否定义 Token / Step / Time Budget？
- [ ] 是否有 Eval Dataset？
- [ ] 是否能够通过 Trace 解释一次完整运行？
