# Agent 架构设计摘要

> 记录当前已确认的架构摘要，在 Architecture Freeze 或重大架构决策后更新。项目实例文件：`.agent-engineering/架构设计.md`。

## 架构层级

- 层级：Deterministic Code / State Machine / Deterministic Workflow / LLM Workflow / Single Agent / Agent + Tools-RAG-Memory / Multi-Agent
- 升级原因（为什么上一层不足）：

## 核心组件

| 组件 | 职责 | 关键契约 | 备注 |
|---|---|---|---|
| | | | |

## 数据流与控制流

```text
触发
  ↓
...
  ↓
最终 Artifact
```

- 谁决定下一步：
- 哪些步骤必须确定性执行：

## 关键决策

| 决策 ID | 主题 | 一句话摘要 |
|---|---|---|
| D-001 | | |

详细记录见 `决策记录.md`。

## 边界快照

- 自主性：
- 知识：
- Tool / 外部副作用：
- 权限：
- State / Memory：
- Multi-Agent：
- 预算：
- HITL：
- 安全：

完整边界见 `边界画布.md`。

## Runtime 与 Deployment

- Runtime 模型：
- 持久化：
- Deployment 目标：
- Rollback 策略：

## 已知约束

- 
