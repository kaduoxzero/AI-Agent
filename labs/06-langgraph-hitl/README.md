# Lab 06｜LangGraph Checkpoint + Human-in-the-Loop

> 目标：把“Agent 需要人工确认”从一个 if/else 变成真正可暂停、持久化并恢复的工作流。

## 1. 学习目标

完成后应能够：

- 使用 LangGraph StateGraph 定义有状态流程；
- 使用 Checkpointer 保存 Thread 状态；
- 使用 `interrupt()` 暂停工作流；
- 使用 `Command(resume=...)` 恢复原任务；
- 理解 `thread_id` 为什么是恢复语义的一部分；
- 把高风险 Action 放入 HITL，而不是让模型自行执行。

## 2. 专业名词通义

- **Checkpoint**：Graph 执行过程中的持久状态快照。
- **Thread**：一条可持续恢复的 Graph 执行上下文，通过 `thread_id` 标识。
- **Interrupt**：在 Node 内主动暂停执行，并向外部返回需要人工处理的数据。
- **Resume**：使用相同 Thread 从暂停点继续执行。

## 3. 场景

系统准备把供应商状态改为 `blocked`：

```text
Analyze
 ↓
Propose Action
 ↓
Approval Node
 ↓ interrupt
Human approves?
 ├─ yes → Execute
 └─ no  → Rejected
```

## 4. 安装与运行

```bash
cd labs/06-langgraph-hitl
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python graph.py
```

实验使用内存 Checkpointer，方便本地理解。生产环境必须替换为持久化实现，否则进程重启后无法恢复。

## 5. 关键观察点

第一次 `invoke()` 不会得到最终结果，而会得到 Interrupt 信息。

第二次：

```python
graph.invoke(
    Command(resume={"approved": True, "reviewer": "alice"}),
    config,
)
```

必须使用与第一次相同的 `thread_id`。

## 6. 生产化设计

真实系统通常是：

```text
Agent Worker
 ↓ interrupt
Checkpoint Store
 ↓
Task status = WAITING_APPROVAL
 ↓
UI / Approval API
 ↓
resume command
 ↓
Worker continues
```

不要让 HTTP 请求一直挂着等待人工审批。

## 7. 验收标准

- [ ] 第一次运行在审批 Node 暂停；
- [ ] 同一 thread_id 可以 resume；
- [ ] approve 后执行 Action；
- [ ] reject 后不会执行 Action；
- [ ] 能解释为什么生产 Checkpointer 必须耐久化；
- [ ] 能说明 Approval UI 与 Graph Runtime 之间如何通过 Task API 解耦。
