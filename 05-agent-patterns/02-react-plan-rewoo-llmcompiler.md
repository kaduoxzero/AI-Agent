# ReAct、Plan & Solve、ReWOO 与 LLMCompiler

> 这四种模式可以理解为 Agent 在“推理、工具调用、计划和并行执行”上的不同组织方式。

## 1. ReAct

ReAct = Reasoning + Acting。

```text
Task
 ↓
Reason
 ↓
Action / Tool
 ↓
Observation
 ↓
Reason
 ↓
...
 ↓
Answer
```

### 专业名词通义

- **Reasoning**：根据当前任务和 State 判断下一步；
- **Action**：实际执行 Tool 或操作；
- **Observation**：Action 返回给 Agent 的结果。

### 优势

- 动态；
- 遇到新结果可以及时改变策略；
- 很适合搜索、排错、工具任务。

### 缺点

每一次 Observation 后通常需要再次模型推理，导致：

- 串行延迟；
- Token 增长；
- Tool 往返多；
- 长任务容易漂移。

### 简化伪代码

```python
while steps < max_steps:
    decision = model(state)
    if decision.final:
        return decision.answer
    result = execute(decision.tool)
    state.add_observation(result)
```

生产代码必须有 `max_steps`。

## 2. Plan & Solve

核心：先规划，再执行。

```text
Task
 ↓
Planner
 ↓
Plan [S1,S2,S3]
 ↓
Executor
 ↓
Observation
 ↓
Need Replan?
```

适合：

- 长任务；
- 多步骤研究；
- Coding；
- 项目计划；
- 复杂业务流程。

### Replan

执行环境变化或某个步骤失败后，根据新 State 重新规划未完成部分。

不要每执行一步都完全重新生成整个 Plan，否则成本很高。

## 3. ReWOO

ReWOO 的重点不是简单“删除 Observation”，而是把规划推理与工具证据获取尽量解耦。

```text
Task
 ↓
Planner
 ↓
E1 = search(A)
E2 = get_data(B)
E3 = analyze(E1,E2)
 ↓
Workers execute evidence plan
 ↓
Evidence
 ↓
Solver
```

### Evidence

工具或子任务返回、最终解题需要引用的事实。

### Solver

基于所有 Evidence 生成最终结果。

### 为什么更高效

ReAct：

```text
Model → Tool → Model → Tool → Model
```

ReWOO 倾向：

```text
Model Plan → Tools → Model Solve
```

减少模型与 Tool 的来回交互。

## 4. LLMCompiler

LLMCompiler 更进一步，将任务视为具有依赖关系的图，识别哪些 Tool 可以并行。

```text
        ┌→ T1 ─┐
Plan ───┤      ├→ T3 → Join
        └→ T2 ─┘
```

### 专业名词通义：DAG

Directed Acyclic Graph，有向无环图。表示任务依赖，但不允许依赖形成死循环。

例如：

```text
T1: query A ─┐
             ├→ T3: compare A,B
T2: query B ─┘
```

T1/T2 可以并行，T3 必须等待两者。

## 5. 四种模式对比

| 维度 | ReAct | Plan & Solve | ReWOO | LLMCompiler |
|---|---|---|---|---|
| 规划 | 局部动态 | 先整体规划 | 证据计划 | 任务图计划 |
| Tool 往返 | 多 | 中 | 少 | 少 |
| 并行能力 | 弱 | 取决实现 | 可实现 | 强调并行 |
| 动态适应 | 强 | 中/强 | 中 | 中 |
| 实现复杂度 | 低 | 中 | 中 | 高 |
| 适合 | 开放工具任务 | 长任务 | 多查询 | 有依赖并行任务 |

## 6. 如何选

### 用 ReAct

当环境动态、下一步高度依赖刚获得结果。

### 用 Plan & Solve

当任务明显可以分阶段，并希望进度可见。

### 用 ReWOO

当大量信息查询可以提前规划，模型往返成本明显。

### 用 LLMCompiler 思路

当存在大量函数调用，并且依赖图可用于并行优化。

## 7. 生产实现的统一抽象

无论哪种 Pattern，都建议统一 State：

```json
{
  "task": "...",
  "plan": [],
  "completed_steps": [],
  "evidence": [],
  "pending_tools": [],
  "errors": [],
  "budget": {}
}
```

这样 Pattern 变化不会导致系统彻底重构。

## 8. 常见反模式

- 把模型内部私有推理过程强制作为业务日志；
- 没有 Step Budget；
- Plan 生成后完全不允许 Replan；
- 所有 Tool 串行；
- 明明动态强却强行一次性规划所有细节。

## 9. 检查清单

- [ ] 下一步是否高度依赖 Observation？
- [ ] 是否值得先 Plan？
- [ ] 可并行 Tool 是否识别出来？
- [ ] 是否有 Replan 策略？
- [ ] 是否有最大 Step / Cost / Time？
