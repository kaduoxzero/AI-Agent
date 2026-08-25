# Skills Templates

`skills/templates/` 是 Agent Engineering Skills 的 **共享只读模板库**。

这些文件用于初始化某个业务项目自己的 Agent Engineering 状态，不应该直接保存任何具体项目的数据。

## 正确关系

```text
skills/templates/                  # 共享，只读
        ↓ instantiate / copy
<project>/.agent-engineering/      # 当前项目独占，可更新
```

## 模板用途

模板使用英文 ID（内部协议）；实例化到业务项目时按 `../agent-engineering-master/resources/PROJECT-DOCUMENT-NAMING.md` 使用中文文件名。

| 模板（只读，英文 ID） | 实例化到项目 |
|---|---|
| `project-state.yaml` | `.agent-engineering/项目状态.yaml` |
| `agent-boundary-canvas.md` | `.agent-engineering/边界画布.md` |
| `decision-ledger.md` | `.agent-engineering/决策记录.md` |
| `current-session.md` | `.agent-engineering/当前会话.md` |
| `project-intake.md` | `.agent-engineering/项目调研.md` |
| `architecture-summary.md` | `.agent-engineering/架构设计.md` |
| `change-impact.md` | `.agent-engineering/影响分析.md` |
| `verification-report.md` | `.agent-engineering/验证报告.md` |

内部英文 ID 与中文实例名的对应关系固定；`history/` 目录名保持英文。

## 禁止行为

Agent / Skill 不得：

- 把当前项目的决策直接追加到本目录；
- 修改模板以保存会话状态；
- 用本目录作为多个项目共享的 State Store；
- 因为模板更新而覆盖项目已有 `.agent-engineering/` 状态。

## 项目级状态

每个项目独立维护：

```text
.agent-engineering/
├─ project.yaml
├─ boundary-canvas.md
├─ decision-ledger.md
├─ current-session.md
├─ project-intake.md
├─ architecture.md
├─ change-impact.md
├─ verification-report.md
└─ history/
```

完整规则见：

`../agent-engineering-master/PROJECT-STATE-POLICY.md`

核心原则：

> Template is immutable. Project State is project-scoped. Cross-project state sharing is never implicit.
