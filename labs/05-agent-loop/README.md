# Lab 05｜Agent Loop：Action、Observation、Budget 与终止条件

> 目标：不依赖任何 Agent 框架，亲手实现一个最小但工程上正确的 Agent Runtime，理解框架背后的循环到底做了什么。

## 1. 学习目标

完成后应能够：

- 实现 Model → Action → Tool → Observation 循环；
- 将 Model Decision 与 Tool Execution 分离；
- 使用 State 保存 Observation；
- 使用 Runtime Budget 强制限制最大 Turn / Tool Call；
- 输出统一 Runtime Event；
- 处理 Final / Tool / Invalid Action 三类结果；
- 理解 ReAct 为什么必须有确定性停止条件。

## 2. 专业名词通义

- **Turn**：一次模型决策轮次。
- **Action**：模型决定执行的下一步动作。
- **Observation**：Tool 或环境返回给 Agent 的结果。
- **Budget**：Runtime 允许消耗的最大轮数、Tool Calls、Token、时间或金额。
- **Trajectory**：从任务开始到最终结果所经过的 Action / Observation 路径。

## 3. 为什么不用真实模型

本实验使用 `DeterministicModel`，目的是让 Agent Loop 完全可测试、可观察。

后续替换真实模型时，只需要保持：

```python
model.decide(state) -> Decision
```

Runtime、Tool、Budget、Event 不需要改变。

## 4. 运行

```bash
cd labs/05-agent-loop
python app.py
```

## 5. 核心链路

```text
State
 ↓
Model.decide()
 ↓
Decision
 ├─ tool → validate → execute → Observation → State
 └─ final → terminate
```

Runtime 同时维护：

```text
turn_count
model_call_count
tool_call_count
events
observations
```

## 6. 实验任务

1. 正常查询供应商风险；
2. 把 `max_tool_calls` 改为 0，观察 Budget 强制停止；
3. 修改模型使其重复调用同一 Tool，观察 `max_turns` 如何防止死循环；
4. 增加新的 Tool，而不修改 Runtime 核心循环。

## 7. 验收标准

- [ ] Runtime 和 Model 解耦；
- [ ] Tool Registry 和 Model 解耦；
- [ ] 有 max_turns；
- [ ] 有 max_tool_calls；
- [ ] 每个 Turn 都产生日志事件；
- [ ] Agent 无法自行绕过 Budget；
- [ ] 能画出完整 Trajectory。
