# Lab 13｜AG-UI Console：Agent Event → Frontend State

> 目标：理解 Agent 前端不是“流式显示 Token”这么简单，而是需要消费 Run、Tool、State、Message 等事件并恢复 UI 状态。

## 1. 学习目标

完成后应能够：

- 理解 AG-UI 的事件驱动模型；
- 处理 Run Lifecycle；
- 展示 Tool Call Start / Args / Result；
- 使用 STATE_SNAPSHOT 建立 UI 状态基线；
- 理解 STATE_DELTA / JSON Patch；
- 区分 Agent Runtime Event 与 UI Event；
- 理解为什么 Refresh / Reconnect 需要 Snapshot，而不只是 Delta。

## 2. 专业名词通义

- **AG-UI**：Agent-User Interaction Protocol，标准化 Agent 与用户界面之间的事件交互。
- **Run Lifecycle**：一次 Agent Run 从开始、步骤执行到完成/失败的生命周期。
- **State Snapshot**：完整状态快照，前端可以直接替换当前状态。
- **State Delta**：局部状态变化，AG-UI 使用 JSON Patch 表示增量。
- **Tool Call Event**：把 Agent 正在调用哪个 Tool、参数和结果透明展示给前端。

## 3. 本实验边界

`server.py` 是一个**AG-UI 事件模型教学服务器**：使用 AG-UI 的标准事件名称和核心字段，通过 SSE 发送给浏览器。

它用于理解协议和 UI 状态机，不声称替代完整 AG-UI SDK / framework integration。

真实 LangGraph 项目可以进一步使用官方 `ag-ui-langgraph` 集成。

## 4. 安装与运行

```bash
cd labs/13-ag-ui-console
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn server:app --reload --port 8013
```

打开：

```text
http://127.0.0.1:8013/
```

## 5. Event Flow

```text
RUN_STARTED
 ↓
STATE_SNAPSHOT
 ↓
TOOL_CALL_START
 ↓
TOOL_CALL_ARGS
 ↓
TOOL_CALL_END
 ↓
TOOL_CALL_RESULT
 ↓
STATE_DELTA
 ↓
TEXT_MESSAGE_START
 ↓
TEXT_MESSAGE_CONTENT...
 ↓
TEXT_MESSAGE_END
 ↓
RUN_FINISHED
```

## 6. 工程延伸

继续加入：

- RUN_ERROR；
- STEP_STARTED / FINISHED；
- Approval Event；
- Artifact Event；
- reconnect 后重新发送 Snapshot；
- threadId / runId 持久化；
- Cancel / Resume；
- LangGraph AG-UI integration。

## 7. 验收标准

- [ ] UI 能显示 Run 状态；
- [ ] UI 能显示 Tool 名称和参数；
- [ ] UI 能显示 Tool Result；
- [ ] UI 能消费 State Snapshot；
- [ ] 能解释 Snapshot 与 Delta 差异；
- [ ] 能解释为什么 SSE 是 Transport，而 AG-UI 是 Event Protocol；
- [ ] 能说明如何升级到官方 AG-UI Framework Integration。
