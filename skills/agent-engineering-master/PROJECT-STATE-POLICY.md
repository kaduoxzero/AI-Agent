# Agent Engineering Master — 项目状态策略

本文件定义 `agent-engineering-master` 的项目状态隔离与归档规则。它属于**强制执行策略**，不是可选建议。

## 1. 核心原则

```text
skills/templates/             = 共享只读模板
<project>/.agent-engineering/ = 当前项目独占状态
```

任何 Skill 都不得把项目运行状态、用户决策、架构选择、验证结果直接写入 `skills/templates/`。

项目级实例文档的**文件名与正文默认均为简体中文**。完整语言、文件映射和历史时间命名规则以：

```text
resources/PROJECT-DOCUMENT-NAMING.md
```

为权威来源（SSoT）。

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

模板文件名是内部英文 ID；实例化到用户业务项目后必须使用中文项目文件名。

允许：读取、复制、用作初始化依据。

禁止：写入项目数据、追加项目决策、修改模板保存当前会话、把模板目录作为跨项目共享 State Store。

## 3. 当前项目状态目录

Master 在每个业务项目根目录使用：

```text
.agent-engineering/
├─ 项目状态.yaml
├─ 边界画布.md
├─ 决策记录.md
├─ 当前会话.md
├─ 项目调研.md
├─ 架构设计.md
├─ 影响分析.md
├─ 验证报告.md
└─ history/
```

所有 Markdown 项目实例文档的标题、章节、表头、说明和结论默认使用简体中文；技术标识符、代码、Schema Key 和标准技术名词可以保留英文。

## 4. 项目根目录识别

Master 每次进入任务时必须先确定 **Project Root**。

优先级：

1. 用户明确指定的项目目录；
2. 当前 Git 仓库根目录；
3. 当前工作目录中包含主要依赖/构建文件的根目录；
4. 如果仍无法判断且多个候选目录代表不同项目，才询问用户。

不得把 Skills 安装目录误判为业务项目根目录。

## 5. 初始化流程

每次任务开始执行：

```text
Resolve Project Root
        ↓
检查 <project>/.agent-engineering/项目状态.yaml
        ↓
存在？
├─ 是 → 读取当前项目状态
└─ 否 → 初始化项目状态目录
          ↓
       从 skills/templates/ 复制结构
          ↓
       按中文项目文件名实例化
          ↓
       写入新的 项目状态.yaml
```

初始化是 **Copy / Instantiate**，不是移动或修改模板原件。

如果 `.agent-engineering/` 已存在但缺少部分文件，只创建缺失文件，不覆盖现有状态。

## 6. 项目身份与时区规则

`项目状态.yaml` 建议结构：

```yaml
schema_version: 1
project_id: <stable-project-id>
project_name: <human-readable-name>
project_root: <project-root>
project_timezone: <IANA-or-stable-timezone>
created_at: <ISO-8601-timestamp>
updated_at: <ISO-8601-timestamp>
current_phase: discovery
current_task: null
```

规则：

- `project_id` 在项目生命周期中保持稳定；
- 项目移动后可更新 `project_root`，不要无理由生成新的 `project_id`；
- `project_timezone` 首次初始化后应保持稳定；
- 历史归档时间必须使用 `project_timezone`；
- 禁止同一项目的归档文件混用 UTC、本地时间和其他时区。

## 7. Session 与长期状态分离

```text
当前会话.md = 当前任务的短期工作状态
边界画布.md = 长期有效的系统边界
决策记录.md = 长期重要决策
history/     = 已完成任务和阶段性记录归档
```

当前任务结束时：

1. 将仍长期有效的边界同步到 `边界画布.md`；
2. 将重要决定同步到 `决策记录.md`；
3. 将验证结论写入 `验证报告.md`；
4. 将任务摘要归档到 `history/`；
5. 重置或更新 `当前会话.md`，不要无限追加。

## 8. 历史归档命名与排序

任务级历史记录必须使用：

```text
.agent-engineering/history/<YYYYMMDD-HHmmss>-<task-id>-<中文主题>.md
```

没有 `task-id` 时：

```text
.agent-engineering/history/<YYYYMMDD-HHmmss>-<中文主题>.md
```

示例：

```text
20260831-153312-task-042-需求澄清.md
20260831-161005-task-043-架构冻结.md
20260901-091500-task-044-功能验证.md
```

强制要求：

- 年、月、日、时、分、秒全部固定宽度并补零；
- 时间戳必须放在文件名最前面；
- 使用项目固定 `project_timezone`；
- 文件名普通字符串升序必须等于真实时间从旧到新；
- 同一秒冲突时在时间戳后添加 `-01`、`-02` 等序号；
- 主题使用中文；
- 禁止 `<task-id-or-date>-<topic>` 这类首排序键不稳定的混合规则。

更完整规则见 `resources/PROJECT-DOCUMENT-NAMING.md`。

## 9. 多项目隔离

两个项目同时运行时必须形成：

```text
Project A/.agent-engineering/
Project B/.agent-engineering/
```

Master 不得：

- 把 A 的决策记录复用到 B；
- 根据另一个项目的当前会话推断当前项目状态；
- 使用全局共享的可写状态文件保存多个项目；
- 因项目名称相似就合并状态。

只有用户明确要求跨项目比较、迁移或复用设计时，才允许读取另一个项目的状态；即使如此，也不得自动合并两者。

## 10. 并发任务规则

同一项目可同时存在多个任务。

长期状态仍属于项目级：

- `边界画布.md`
- `决策记录.md`

任务级记录进入 `history/`，并遵循第 8 节的固定时间前缀规则。

多个 Agent 同时写同一个项目状态时：

- 避免无条件覆盖；
- 先读取最新版本再更新；
- 对架构决策冲突进行显式合并；
- 不允许静默覆盖另一个任务刚写入的 Decision；
- 同秒归档使用递增序号避免文件名冲突。

## 11. 已有项目安全规则

如果项目已经存在 `.agent-engineering/`：

- 不重新初始化；
- 不覆盖用户已有状态；
- 先读取 `项目状态.yaml` 和长期状态；
- 只创建缺失文件；
- 模板升级不能直接覆盖项目实例；
- 若发现旧版英文实例文件，应迁移到中文文件名，不要并行维护两套状态；
- 已有历史文件不强制批量重命名，除非用户要求；新归档必须执行新规范。

模板版本变化与项目状态迁移必须分开处理。

## 12. 状态写入契约

专项 Skill 返回 Master 后，Master 根据结果写入当前项目：

```text
Boundary changed
→ 边界画布.md

Architecture decision
→ 决策记录.md

Current task progress
→ 当前会话.md

Existing-project blast radius
→ 影响分析.md

Verification / Eval / Security result
→ 验证报告.md

Completed task summary
→ history/<YYYYMMDD-HHmmss>-<task-id>-<中文主题>.md
```

专项 Skill 不应自行选择全局共享状态位置。

## 13. Fail-Safe 规则

以下情况禁止写状态，直到定位清楚：

- Project Root 不明确且存在多个项目候选；
- 当前 `.agent-engineering/项目状态.yaml` 的 `project_id` 与明显不同的项目不匹配；
- 状态目录位于 Skills 安装目录而非业务项目；
- 目标位置是另一个项目的 `.agent-engineering/`；
- 历史归档无法确定项目时区。

## 14. Git 策略

`.agent-engineering/` 是否提交 Git 由项目决定。

推荐：

- `边界画布.md`、`决策记录.md`、`架构设计.md`、`验证报告.md`：适合团队项目提交；
- 包含敏感信息、临时会话、环境数据的内容：必须脱敏或加入 `.gitignore`。

禁止在状态文件中写 API Key、密码、Token、私钥等 Secret。

## 15. 不可违反的最终规则

```text
Template is immutable.
Project State is project-scoped.
Session State is task-scoped.
Decisions are durable.
History timestamp is fixed-width and timezone-stable.
Project-facing documents are Chinese by default.
Cross-project state sharing is opt-in, never implicit.
```
