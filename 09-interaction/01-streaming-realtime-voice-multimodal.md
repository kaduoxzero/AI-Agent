# Streaming、Realtime、Voice 与 Multimodal Agent

## 1. Agent 交互为什么不能只等最终答案

大型 Agent 一次任务可能持续数秒、数分钟甚至更久。如果前端只显示“正在思考”，用户无法判断系统是否卡死。

因此 Agent UI 至少应支持三类流：

```text
Content Stream    → token / text / audio
Progress Stream   → node / task / tool status
Control Stream    → approval / interrupt / error / resume
```

## 2. Streaming

### Token Streaming

模型生成一部分就发送一部分。

优点：首字延迟低。

但 Agent 产品还应该流式展示：

- Tool 开始 / 完成；
- 当前 Worker；
- Progress；
- Citation；
- Artifact；
- Approval Request。

### 传输方式

#### SSE

Server-Sent Events，服务器单向持续推送。

适合多数文本 Agent。

#### WebSocket

双向长连接。

适合：

- Realtime；
- Voice；
- 双向控制；
- 高频事件。

#### WebRTC

低延迟实时音视频场景常用。

## 3. Voice Agent 两种架构

### Pipeline Voice Agent

```text
Audio
 ↓ STT
Text
 ↓ Agent Workflow
Text
 ↓ TTS
Audio
```

优点：

- 可以复用文本 Agent；
- 每一层可独立替换；
- 易调试。

缺点：延迟相对高。

### Speech-to-Speech Realtime Agent

```text
Live Audio ↔ Realtime Model ↔ Tools
```

更低延迟，更自然处理插话，但 Session、Guardrail、音频状态更复杂。

## 4. 专业名词通义

- **STT**：Speech-to-Text，语音转文字；
- **TTS**：Text-to-Speech，文字转语音；
- **VAD**：Voice Activity Detection，检测用户何时开始/停止讲话；
- **Barge-in**：Agent 正在说话时用户插话并打断；
- **Turn Detection**：判断一轮用户输入何时完成；
- **Transport**：承载实时事件的数据通道，例如 WebSocket / WebRTC。

## 5. Realtime Session

Realtime Agent 不是“一次请求一次结果”，而是一段长连接 Session。

典型状态：

```text
connection
conversation history
active agent
voice config
tool executions
guardrail state
pending approvals
interrupt state
```

OpenAI Agents SDK 当前也采用 RealtimeAgent / RealtimeSession 等抽象，并支持工具、Handoff、Guardrail 与自动中断处理。

## 6. Tool Calling in Voice

语音中调用 Tool 时需要给用户反馈：

```text
用户：查一下我的订单。
Agent：我正在查询订单记录……
[Tool executes]
Agent：最新订单已发货。
```

避免 3 秒完全静音。

高风险 Tool 仍然需要审批，Voice 不能绕过安全控制。

## 7. Multimodal Input

Agent 可能同时接收：

```text
Text
Image
Screenshot
Audio
Document
Camera Frame
```

设计 State 时不要把所有模态都转成一段巨型文本。

推荐保存 Artifact Reference：

```json
{
  "artifact_id": "img-123",
  "type": "image",
  "storage_uri": "...",
  "metadata": {}
}
```

模型调用时再选择需要的 Artifact。

## 8. Interrupt

Realtime 中断与 Workflow HITL interrupt 不同：

- Voice Interrupt：停止当前音频响应；
- Workflow Interrupt：暂停业务执行等待外部决定。

二者名称类似但语义不同。

## 9. Realtime 安全

需要考虑：

- 音频转录敏感数据；
- 工具执行审批；
- Voice Spoofing；
- 实时 Guardrail；
- Session Hijack；
- 临时 Token；
- Transport Authentication。

浏览器 Realtime 不应暴露长期服务端 API Secret。

## 10. 体验指标

除了普通 Agent 的 Task Success，还应测：

```text
Time to First Audio
Interruption Latency
Turn Detection Accuracy
Tool Wait Time
Audio Failure Rate
Conversation Recovery Rate
```

## 11. 检查清单

- [ ] 是否区分 Content / Progress / Control Stream？
- [ ] 文本任务是否优先 SSE？
- [ ] Voice 是否设计 VAD / Barge-in？
- [ ] Tool 执行期间是否给用户反馈？
- [ ] Realtime Tool 是否仍然走权限与 Approval？
- [ ] 多模态对象是否 Artifact 化？
- [ ] 浏览器端是否只使用短期凭证？

## 12. 参考

- OpenAI Realtime Agents：https://openai.github.io/openai-agents-js/guides/voice-agents/
