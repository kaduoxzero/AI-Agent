# Agent Engineering Master — Project State Policy

本文件定义 `agent-engineering-master` 的项目状态隔离规则。它属于 **强制执行策略**，不是可选建议。

## 1. 核心原则

```text
skills/templates/           = 共享只读模板
<project>/.agent-engineering/ = 当前项目独占状态
```

任何 Skill 都不得把项目运行状态、用户决策、架构选择、验证结果直接写入 `skills/templates/`。

## 2. 模板目录必须只读

`skills/templates/` 只负责提供结构模板，例如：

- `agent-boundary-canvas.md`
- `decision-ledger.md`
- `current-session.md`
- `project-intake.md`
- `architecture-summary.md`
- `change-impact.md`
- `verification-report.md`
- `project-state.yaml`

模板文件名（英文 ID）与项目状态实例文件（中文）通过 `resources/PROJECT-DOCUMENT-NAMING.md` 映射；唯一的例外是 `agent-boundary-canvas.md` → `边界画布.md`、`architecture-summary.md` → `架构设计.md`、`project-state.yaml` → `项目状态.yaml`。

允许：

- 读取；
- 复制；
- 用作初始化依据。

禁止：

- 写入项目数据；
- 追加项目决策；
- 修改模板来保存当前会话；
- 用模板目录作为跨项目共享 State Store。

## 3. 当前项目状态目录

Master 在每个业务项目根目录使用：

```text
.agent-engineering/
├─ 项目状态.yaml            (project.yaml)
├─ 边界画布.md              (boundary-canvas.md)
├─ 决策记录.md              (decision-ledger.md)
├─ 当前会话.md              (current-session.md)
├─ 项目调研.md              (project-intake.md)
├─ 架构设计.md              (architecture.md)
├─ 影响分析.md              (change-impact.md)
├─ 验证报告.md              (verification-report.md)
└─ history/
```

## 3.1 命名约定

Skill 内部协议、模板与注册表使用英文 ID；实例化到业务项目的状态文件使用中文文件名。

完整映射的权威来源：

```text
resources/PROJECT-DOCUMENT-NAMING.md
```

本策略后续章节提到的英文名均指对应的中文实例文件。`history/` 目录名保持英文。

其中：

- `project.yaml`：项目身份与状态版本；
- `boundary-canvas.md`：长期有效的系统边界；
- `decision-ledger.md`：长期架构决策记录；
- `current-session.md`：当前任务 / 当前引导阶段的短期状态；
- `project-intake.md`：项目现状与约束；
- `architecture.md`：当前确认架构摘要；
- `change-impact.md`：当前重大修改的 Blast Radius；
- `verification-report.md`：最近一次验证结果；
- `history/`：已完成任务和阶段性记录归档。

## 4. Project Root Resolution

Master 每次进入任务时必须先确定 **Project Root**。

优先级：

1. 用户明确指定的项目目录；
2. 当前 Git 仓库根目录；
3. 当前工作目录中包含主要依赖 / 构建文件的根目录；
4. 如果仍无法判断且多个候选目录代表不同项目，才询问用户。

不得把 Skills 安装目录误判为业务项目根目录。

## 5. Bootstrap 流程

每次任务开始执行：

```text
Resolve Project Root
        ↓
检查 <project>/.agent-engineering/project.yaml
        ↓
存在？
├─ 是 → 读取当前项目状态
└─ 否 → 初始化项目状态目录
          ↓
       从 skills/templates/ 复制结构
          ↓
       写入新的 project.yaml
```

初始化是 **Copy / Instantiate**，不是移动或修改模板原件。

## 6. project.yaml 身份规则

建议结构：

```yaml
schema_version: 1
project_id: <stable-project-id>
project_name: <human-readable-name>
project_root: <project-root>
created_at: <timestamp>
updated_at: <timestamp>
current_phase: discovery
current_task: null
```

`project_id` 应在项目生命周期中保持稳定。

项目目录移动后，可以更新 `project_root`，但不要无理由生成新的 `project_id`。

## 7. Session 与长期状态分离

不要把所有历史都无限追加到一个文件。

```text
current-session.md
    = 当前任务的短期工作状态

boundary-canvas.md
    = 长期边界

decision-ledger.md
    = 长期重要决策

history/
    = 已完成任务的归档记录
```

当当前任务结束时：

1. 把仍然长期有效的边界同步到 `boundary-canvas.md`；
2. 把重要决定同步到 `decision-ledger.md`；
3. 把验证结论写入 `verification-report.md`；
4. 将任务摘要归档到 `history/`；
5. 重置或更新 `current-session.md`，不要让其无限膨胀。

## 8. 多项目隔离

两个项目同时运行时必须形成：

```text
Project A/.agent-engineering/
Project B/.agent-engineering/
```

Master 不得：

- 把 A 的 Decision Ledger 复用到 B；
- 根据另一个项目的 Session State 推断当前项目状态；
- 使用全局共享的可写状态文件保存多个项目；
- 因为项目名称相似就合并状态。

只有用户明确要求跨项目比较、迁移或复用设计时，才允许读取另一个项目的状态；即使如此，也不得自动合并两者。

## 9. 并发任务规则

同一个项目可能同时存在多个任务。

长期状态仍然属于项目级：

- `boundary-canvas.md`
- `decision-ledger.md`

但任务级记录应进入：

```text
.agent-engineering/history/<task-id-or-date>-<topic>.md
```

如果多个 Agent 同时写同一个项目状态：

- 避免无条件覆盖；
- 先读取最新版本再更新；
- 对架构决策冲突进行显式合并；
- 不允许静默覆盖另一个任务刚写入的 Decision。

## 10. Existing Project Safety

如果项目已经存在 `.agent-engineering/`：

- 不重新初始化；
- 不覆盖用户已有状态；
- 先读取 `project.yaml` 和长期状态；
- 只创建缺失文件；
- 模板升级不能直接覆盖项目实例。

模板版本变化与项目状态迁移必须分开处理。

## 11. State Write Contract

专项 Skill 返回 Master 后，Master 根据结果写入当前项目：

```text
Boundary changed
→ 边界画布.md (boundary-canvas.md)

Architecture decision
→ 决策记录.md (decision-ledger.md)

Current task progress
→ 当前会话.md (current-session.md)

Existing-project blast radius
→ 影响分析.md (change-impact.md)

Verification / Eval / Security result
→ 验证报告.md (verification-report.md)

Completed task summary
→ history/
```

专项 Skill 不应自行选择全局共享状态位置。

## 12. Fail-Safe Rules

以下情况禁止写状态，直到定位清楚：

- Project Root 不明确且存在多个项目候选；
- 当前 `.agent-engineering/project.yaml` 的 `project_id` 与明显不同的项目不匹配；
- 状态目录位于 Skills 安装目录而非业务项目；
- 目标位置是另一个项目的 `.agent-engineering/`。

## 13. Git 策略

`.agent-engineering/` 是否提交 Git 由项目决定。

推荐：

- `boundary-canvas.md`、`decision-ledger.md`、`architecture.md`、`verification-report.md`：适合团队项目提交；
- 包含敏感信息、临时会话、环境数据的内容：必须脱敏或加入 `.gitignore`。

禁止在状态文件中写 API Key、密码、Token、私钥等 Secret。

## 14. 不可违反的最终规则

```text
Template is immutable.
Project State is project-scoped.
Session State is task-scoped.
Decisions are durable.
Cross-project state sharing is opt-in, never implicit.
```
