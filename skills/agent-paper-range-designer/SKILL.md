---
name: agent-paper-range-designer
version: 1.0.0
description: Design, extend, review, and verify Paper Range narrative cyber-simulation scenarios, typed action contracts, world-state transitions, learning loops, theme packs, and sandbox boundaries. Use when building a fictional cyber range or training simulation where user commands and natural language must mutate only simulated state and never reach real network targets.
---

# Paper Range Designer

## Objective

把“纸上靶场 / 剧情靶场 / Cyber Range 学习游戏”转换成一个 **可验证、可扩展、默认不触达真实网络** 的模拟系统。

本 Skill 的单一职责：设计和审查 Paper Range 的 Scenario / Action / WorldState / Story / Learning / Theme / Sandbox Contract。

## Trigger & Scope

出现以下意图时使用：

- 创建或扩展纸上靶场、剧情靶场、Cyber Range；
- 用户输入 `nmap / curl / ssh` 或自然语言，系统只模拟结果；
- 设计虚构目标机、服务、线索、Evidence、Flag、任务链；
- 设计 WorldState、Story Graph、Branch / Consequence；
- 设计 Hint、Score、复盘、学习报告；
- 设计 Theme Pack Registry 与场景主题选择；
- 审查 Session Reset、容器隔离和场景外目标拒绝；
- 将新场景、新 Action 接入现有 Paper Range Runtime。

不使用本 Skill：

- 对真实目标执行安全测试；
- 与模拟产品无关的通用 Agent 工程；
- 只做普通 CSS 调整且不影响场景、动作、状态契约。

## Simulation Boundary

默认采用 **Simulation-Only / Fail-Closed**：

1. Target 必须来自 Scenario Registry；
2. 用户输入不得直接进入 shell、`subprocess`、raw socket 或真实扫描器；
3. 表面命令必须先变成 Typed Action Intent；
4. Runtime 只修改当前 Session 的虚构 WorldState；
5. 场景外 IP / Host / URL 必须拒绝；
6. 不能因为目标是 RFC1918 地址就默认安全；
7. 如未来需要真实隔离靶容器，必须单独经过 Security Review；
8. 无法确认是否属于模拟世界时 Fail Closed。

正确链路：

```text
User Input
→ Intent Parser
→ Target / Capability Policy
→ Simulation Adapter
→ WorldState Mutation
→ Narrative / Evidence / Learning Event
→ UI
```

禁止：

```text
User Input
→ subprocess.run(user_input)
→ Real Network
```

## Scenario Contract

每个场景至少定义：

```text
Scenario ID
Name / Subtitle
Difficulty
Category
Learning Goal
Target Registry
Initial Narrative
Objectives[]
Hints[]
Services[]
Evidence / Clues[]
Allowed Actions[]
Story Beats[]
Completion Conditions
Flag / Reward
Theme Tags
Reset Semantics
```

场景配置优先数据化，避免每条剧情硬编码到 Runtime 分支。

Target Registry 至少包含：

```text
Target ID
Display Host/IP
Allowed Protocols
Allowed Services
Simulation Adapter
State Owner
```

未登记 Target 一律 Out of Scope。

## Typed Action Contract

自然语言、命令和未来 Agent Action 必须归一化到同一结构：

```text
ActionIntent
- kind
- raw_input
- source: command | natural_language | agent
- target_id
- target_display
- arguments
- required_state
- capability
```

例如：

```text
“我先扫描所有 TCP 端口”
nmap -p- 10.10.10.10
        ↓
ActionIntent(kind=scan_ports)
        ↓
同一个 Simulation Handler
```

Intent Parser 负责解释，不拥有 WorldState mutation 权限。

## WorldState Contract

Session State 至少分层：

```text
Identity
- session_id
- scenario_id
- theme_id

Progress
- current_objective
- completed_objectives
- story_node

Discovery
- discovered_services
- discovered_paths
- clues
- credentials
- evidence

Learning
- score
- action_count
- hint_count
- invalid_action_count

Runtime
- status
- events
- started_at
- completed_at
```

避免多个组件随意覆盖一个无约束的大字典。

## Session & Memory Lifecycle

Paper Range 默认 Ephemeral Session：

```text
container start
→ new SessionStore
→ 本次运行持续复用状态
→ container stop/remove
→ WorldState 消失
```

默认验收：

- 游戏 Session 不写 PostgreSQL；
- 不写 Redis durable memory；
- 不通过宿主机 volume 保存 WorldState；
- 新容器看不到上一容器的战役状态。

未来若需要账号进度/排行榜，必须把 `Player Progress` 和 `Live WorldState` 分离。

## Story Graph

推荐：

```text
StoryNode
- id
- requires
- trigger
- narrative
- effects
- evidence
- unlocks
- next[]
```

关键剧情由 WorldState / Evidence 驱动。模型可生成表达，但不能绕过 Completion Condition。

## Learning Loop

每个场景必须回答：

```text
用户在学什么？
什么行为代表理解？
什么错误值得反馈？
Hint 如何逐步降低难度？
结束后给什么可行动复盘？
```

建议指标：Completion、Action Count、Hint Count、Invalid Action Count、Evidence Coverage、Objective Order、Efficiency Score。

评分奖励正确侦察、证据链、边界意识和任务完成质量，不奖励“攻击强度”。

## Theme Pack Contract

视觉与 Runtime 分离：

```text
ThemePack
- id
- tags
- palette tokens
- typography
- panel treatment
- ambient treatment
- asset references
- motion profile
```

Scenario 只声明 Theme Tags。Theme Selector 决定具体主题。若扩展到 40 套主题，先建立 Registry + Token Contract，不复制 40 份页面逻辑。

## Skill Composition

按需选择最多 2 个 Supporting Skills：

- `agent-security-reviewer`：网络、文件、容器、Tool 权限边界；
- `agent-eval-hardening`：轨迹、Reset、Fail-Closed、回归测试；
- `agent-existing-project-modifier`：修改现有 Paper Range 代码；
- `agent-productionizer`：Docker、镜像、发布、运行环境；
- `agent-multi-agent-designer`：仅在确有多个独立 Agent 角色时使用。

## Verification Gates

Action Gate：

- [ ] 自然语言和命令能映射到同一 Intent；
- [ ] Intent Parser 不直接执行真实命令；
- [ ] 未知 Action Fail Closed；
- [ ] 场景外 Target Fail Closed。

State Gate：

- [ ] 每个 Action 有确定 State Mutation；
- [ ] 重复 Action 不破坏状态；
- [ ] Objective / Story 不能被直接跳过；
- [ ] Completion Condition 可自动测试。

Reset Gate：

- [ ] 同一容器内 Session 可持续；
- [ ] 删除 Session 后状态消失；
- [ ] 后端容器重启后旧 Session 不存在；
- [ ] 默认无持久化 WorldState 的 volume。

Learning Gate：

- [ ] Hint 与评分规则确定；
- [ ] 错误反馈不直接泄露后续全部答案；
- [ ] 完成后能生成复盘；
- [ ] 评分关注学习质量。

UI Gate：

- [ ] 当前 Objective 可见；
- [ ] Clue / Evidence 可见；
- [ ] 可输入自然语言和模拟命令；
- [ ] WorldState 变化有可见反馈；
- [ ] Desktop / Mobile 可完成核心流程。

## Evaluation

最少测试集：

```text
Happy Path
Natural Language Path
Command Path
Wrong Target Path
Unknown Action Path
Hint Path
Wrong Credential Path
Completion Report Path
Session Delete Path
Fresh Container Path
```

Golden Trajectory：

```text
create session
→ scan
→ inspect web
→ discover credential
→ simulated access
→ mission complete
→ report
```

## Deliverables

至少输出：

```text
Scenario Contract
Action Contract
WorldState Contract
Simulation Boundary
Learning Contract
Theme Contract（如涉及 UI）
Changed Files
Verification Evidence
Open Risks
Next Exact Action
```

## Report Back to Master

```text
Skill Used: agent-paper-range-designer
Problem Addressed:
Scenario / Runtime Scope:
Simulation Boundary:
Action Contract Changes:
WorldState Changes:
Learning Changes:
Theme Changes:
Files / Components Affected:
Verification Performed:
Security Boundary Evidence:
New Risks:
Unresolved Items:
Recommended Next Capability:
```
