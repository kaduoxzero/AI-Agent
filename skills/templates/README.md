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

- `project-state.yaml` → 初始化 `.agent-engineering/project.yaml`
- `agent-boundary-canvas.md` → 初始化 `.agent-engineering/boundary-canvas.md`
- `decision-ledger.md` → 初始化 `.agent-engineering/decision-ledger.md`
- `guided-session-state.md` → 初始化 `.agent-engineering/current-session.md`
- `project-intake.md` → 初始化 `.agent-engineering/project-intake.md`
- `change-impact.md` → 初始化 `.agent-engineering/change-impact.md`
- `verification-report.md` → 初始化 `.agent-engineering/verification-report.md`

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
