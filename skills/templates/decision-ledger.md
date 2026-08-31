# Agent 设计决策记录

> 用于记录设计和构建过程中所有关键决策，避免 Agent 在后续实现时遗忘、漂移或重新解释用户选择。项目实例文件：`.agent-engineering/决策记录.md`。

## 会话元数据

- 项目：
- 模式：新项目 / 已有项目
- 用户目标：
- 主 Skill：
- 开始时间：
- 最后更新时间：

## 决策状态

机器协议值可以保留英文，面向人的含义如下：

- `Proposed`：已提出，尚未确认
- `Accepted`：用户确认或明确授权 Agent 采用推荐项
- `Rejected`：明确不采用
- `Deferred`：当前不实现，但需要记录
- `Superseded`：已被后续决策替代

## 决策表

| ID | 主题 | 状态 | 最终决策 | 原因 | 权衡 | 验证方式 |
|---|---|---|---|---|---|---|
| D-001 | | | | | | |

---

## 决策详情模板

### D-XXX — <主题>

**状态：** Proposed / Accepted / Rejected / Deferred / Superseded

**待解决问题**

需要解决什么工程决策？

**已考虑方案**

- A.
- B.
- C.

**推荐方案**

- 方案：
- 原因：

**最终决策**


**决策原因**


**权衡**

- 复杂度：
- 延迟：
- 成本：
- 可靠性：
- 安全性：
- 可维护性：

**新增边界**

- State：
- Context：
- Tool：
- 权限：
- 数据：
- Runtime：

**受影响组件**


**验证方式**


**回滚 / 重新评估触发条件**

在什么条件下需要重新评估这个决策？

---

## 推荐必须记录的决策

至少应记录以下主题中的关键项：

- D-001 业务目标 / Out-of-Scope
- D-002 架构层级：Workflow / Single Agent / Multi-Agent
- D-003 自主性等级
- D-004 知识源 / RAG
- D-005 Tool 与外部副作用模型
- D-006 State / Memory / Checkpoint
- D-007 Multi-Agent 拆分决策
- D-008 Identity / Permission
- D-009 HITL 策略
- D-010 Runtime / Queue / Worker
- D-011 预算 / 终止条件
- D-012 Eval / Release Gate
- D-013 可观测性
- D-014 Deployment

## 架构冻结摘要

```text
目标：
不在范围内：
架构：
自主性：
知识：
Tools：
State / Memory：
Multi-Agent：
Identity / Permission：
HITL：
Runtime：
预算：
Eval：
可观测性：
Deployment：
```

只有这里与 `边界画布.md` 一致后，才进入大规模实现。
