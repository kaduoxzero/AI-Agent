# AG-UI 与 Agent 前后端协议

> 目标：补齐 Agent 系统第三条关键通信链路——Agent 与用户界面之间如何用统一事件模型交互。

## 1. 三类协议要分清

```text
Agent ↔ Tool / Data
       MCP

Agent ↔ Agent
       A2A

Agent ↔ User / Frontend
       AG-UI
```

MCP 解决能力接入，A2A 解决 Agent 间协作，AG-UI 解决 Agent Runtime 与前端之间的实时交互。

## 2. 专业名词通义

- **AG-UI（Agent-User Interaction Protocol）**：面向 Agent 与用户前端之间的开放、轻量、事件驱动协议。
- **Event（事件）**：Runtime 对外发布的结构化事实，例如 RunStarted、ToolCallStarted、StateDelta。
- **State Snapshot（状态快照）**：某一时刻完整状态。
- **State Delta（状态增量）**：只发送相对于上一次状态发生变化的部分。
- **UI Intent**：Agent 希望前端展示或触发的交互意图，而不是直接操纵 DOM。

## 3. 为什么普通 SSE 文本流不够

很多项目只发送：

```text
data: token1
data: token2
```

但真正的 Agent UI 还需要知道：

```text
任务开始了吗？
正在调用哪个 Tool？
Tool 参数是什么？
是否等待人工审批？
State 哪一部分变化了？
是否产生 Artifact？
任务是失败还是取消？
```

所以应该从“Token Stream”升级为“Agent Event Stream”。

## 4. 推荐事件模型

```text
RunStarted
TurnStarted
TextMessageStart
TextMessageDelta
ToolCallStart
ToolCallArgs
ToolCallResult
StateSnapshot
StateDelta
ApprovalRequested
ArtifactCreated
RunCompleted
RunFailed
```

AG-UI 当前采用的就是 streaming event-based architecture，并定义了生命周期、文本、Tool Call、State 等标准事件类别。

## 5. 后端事件到前端状态

```text
Agent Runtime
 ↓ emit event
Event Stream
 ↓
Frontend Reducer
 ↓
UI State
 ↓
Chat / Timeline / Tool Panel / Approval / Artifact
```

前端不应该通过解析模型自然语言判断：

> “模型说‘我正在搜索’，所以大概正在调用 Tool。”

而应消费明确事件：

```json
{
  "type": "TOOL_CALL_START",
  "tool_call_id": "tc_123",
  "tool_name": "search_web"
}
```

## 6. 与 Runtime Event Model 对齐

本知识库 Runtime 章节已经要求统一事件模型。最佳实践是内部事件与外部协议事件分层：

```text
Domain / Runtime Event
       ↓ adapter
AG-UI Event
       ↓
Frontend
```

不要让 Runtime 核心直接依赖某一个 UI SDK。

## 7. State Snapshot 与 Delta

长任务中每次发送完整 State 成本很高。

推荐：

```text
首次连接 → STATE_SNAPSHOT
后续变化 → STATE_DELTA
断线重连 → 新 Snapshot + 后续 Delta
```

前端本地通过 Reducer 合并。

## 8. Tool UI

Tool Call 应可视化为：

```text
search_web
状态：running
参数：{"query": "..."}
耗时：1.2s
结果：3 sources
```

高风险 Tool：

```text
ApprovalRequested
 ↓
Frontend Approval Card
 ↓ approve / reject
Backend resumes task
```

## 9. Artifact

聊天文本不是所有 Agent 的最终输出。

Agent 可能产生：

```text
Report
Code Patch
CSV
Chart
Plan
Risk Assessment
Generated File
```

建议 UI 区分：

```text
Conversation Stream
Task Timeline
Artifact Workspace
```

## 10. Transport

AG-UI 是事件语义，不等于固定 Transport。

常见：

- SSE：服务器持续推送，简单可靠；
- WebSocket：双向低延迟交互；
- WebRTC：Realtime Voice / Audio 场景；
- HTTP：控制命令、审批、取消等。

## 11. 断线恢复

生产前端必须支持：

```text
network disconnected
 ↓
remember last_event_id
 ↓ reconnect
 ↓
server replay or snapshot
 ↓
continue rendering
```

否则长任务一刷新页面就丢失进度。

## 12. 前端状态机

建议至少：

```text
IDLE
RUNNING
WAITING_APPROVAL
CANCELLING
CANCELLED
FAILED
COMPLETED
```

UI 状态来源于后端 Task State，而不是模型文本。

## 13. 安全

前端事件中不要泄露：

- System Prompt；
- Secret；
- 内部 Chain-of-Thought；
- 原始 Credential；
- 不允许用户看到的 Tool Result。

Trace 数据和用户可见事件需要分层。

## 14. MCP + A2A + AG-UI 总图

```text
                       User
                         ↑↓
                       AG-UI
                         ↑↓
                     Agent Runtime
                    /             \
                 MCP               A2A
                  ↓                 ↓
         Tool / DB / Service     Other Agent
```

三个协议解决不同边界，不应互相替代。

## 15. 实训

为毕业项目增加一个 Agent Console：

1. `/tasks/{id}/events` 返回结构化事件流；
2. 前端显示 Tool Timeline；
3. 支持 State Snapshot / Delta；
4. 支持 Approval Card；
5. 支持 Cancel；
6. 支持 Artifact 面板；
7. 刷新页面后可恢复任务状态。

## 16. 检查清单

- [ ] 前端是否消费结构化 Event，而不是解析自然语言？
- [ ] 是否区分 Message、Tool、State、Artifact？
- [ ] 是否支持 WAITING_APPROVAL？
- [ ] 是否支持断线恢复？
- [ ] UI Event 是否与内部 Trace 分层？
- [ ] 是否避免暴露 Secret / 内部推理？