# Lab 16｜Event-Driven Agent：Dedup、Retry、DLQ 与 Replay

> 目标：摆脱“Agent = 聊天框”的限制，构建由 Webhook / Cron / Alert / Message 等事件触发的 Agent 任务系统。

## 1. 学习目标

完成后应能够：

- 将外部 Event 转换成标准 Task；
- 使用 Event ID 去重；
- 使用 Idempotency 避免重复副作用；
- 对失败任务执行有限 Retry；
- 超过次数后进入 DLQ；
- 修复问题后 Replay；
- 理解 Event-Driven Agent 与同步 Chat Agent 的架构差异。

## 2. 专业名词通义

- **Event-Driven Agent**：由系统事件而非用户聊天直接触发的 Agent。
- **Deduplication**：识别重复 Event，避免创建重复任务。
- **DLQ（Dead Letter Queue）**：多次失败后存放无法正常处理任务的队列。
- **Replay**：把历史 Event / Task 重新送入处理链路。
- **At-least-once Delivery**：消息可能被投递多次，因此消费端必须考虑幂等。

## 3. 运行

```bash
cd labs/16-event-driven-agent
python app.py
```

## 4. 流程

```text
Webhook / Cron / Alert
 ↓
Event Gateway
 ↓ dedup
Task Queue
 ↓
Agent Worker
 ├─ success → DONE
 └─ failure → Retry
                ↓ max attempts
               DLQ
                ↓ repair
              Replay
```

## 5. 实验行为

程序会模拟：

1. 正常 Event；
2. 同一个 Event 重复投递；
3. 一个持续失败的 Event；
4. 失败进入 DLQ；
5. 修复故障后 Replay 成功。

## 6. 生产化延伸

真实项目可替换为：

```text
Kafka
RabbitMQ
SQS
Redis Streams
NATS
Pulsar
```

并加入：

- visibility timeout；
- partition / ordering；
- backpressure；
- distributed dedup store；
- event schema registry；
- poison message handling；
- audit / trace propagation。

## 7. 验收标准

- [ ] 重复 Event 不创建重复任务；
- [ ] Retry 有上限；
- [ ] 超过上限进入 DLQ；
- [ ] DLQ 可以 Replay；
- [ ] Handler 设计为幂等；
- [ ] Event 带 trace_id / event_id；
- [ ] 能解释为什么 MQ 的“至少一次投递”要求业务幂等。
