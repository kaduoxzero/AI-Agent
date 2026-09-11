---
name: agent-paper-range-designer
version: 1.0.0
description: Design, extend, review, and verify Paper Range narrative cyber-simulation scenarios, typed action contracts, world-state transitions, learning loops, theme packs, and sandbox boundaries. Use when building a fictional cyber range or training simulation where user commands and natural language must mutate only simulated state and never reach real network targets.
---

# Paper Range Designer

## Objective

把“做一个网络安全靶场 / 剧情推演 / 命令式学习游戏”转换成一个 **可验证、可扩展、默认不触达真实网络** 的模拟系统。

本 Skill 的单一职责是：

> 设计和审查 Paper Range 类叙事式模拟产品的 Scenario / Action / WorldState / Story / Learning / Theme / Sandbox Contract。

它不负责通用 Web 前端实现、通用生产部署或真实安全测试；这些工作按需交给 Existing Project Modifier、Security Reviewer、Eval Hardening、Productionizer 等专项 Skill。

## 1. Trigger & Scope

出现以下意图时使用：

- 纸上靶场、剧情靶场、Cyber Range、CTF-like 学习场景；
- “用户输入 nmap/curl/ssh 或自然语言，系统模拟结果”；
- 设计虚构目标机、服务、证据、线索、Flag、任务链；
- 设计 WorldState、Story Graph、Branch / Consequence；
- 设计 Hint、Score、复盘、学习报告；
- 设计多套前端 Theme Pack 与场景到主题的选择规则；
- 审查是否可能误触真实网络、宿主机或持久化外部状态；
- 将新的 Paper Range 场景或动作接入现有 Runtime。

不使用本 Skill 的情况：

- 对真实目标执行安全测试；
- 通用漏洞利用研究；
- 与 Paper Range 无关的普通 Agent 项目；
- 只做 CSS 调整且不影响场景/动作/状态契约。

## 2. Non-Negotiable Simulation Boundary

Paper Range 默认采用 **Simulation-Only / Fail-Closed** 边界：

1. 场景目标必须来自 Scenario Registry；
2. 用户输入不能直接传入 `subprocess`、shell、raw socket 或真实扫描器；
3. `nmap / curl / ssh / browser / file` 等表面命令必须先解析成 Typed Action Intent；
4. Runtime 只修改当前 Session 的虚构 WorldState；
5. 输入场景之外的 IP / Host / URL 必须拒绝；
6. 不允许因为“看起来像内网地址”就默认安全；
7. 容器内如需真实工具，只能作用于明确创建的隔离靶容器，并必须单独经过 Security Review；
8. 默认不向宿主机、互联网、公司网络或用户真实资产发包；
9. 所有 Flag、凭据、日志、服务 Banner 必须是训练数据；
10. 无法确认目标是否属于模拟世界时，Fail Closed。

推荐边界：

```text
User Input
   ↓
Intent Parser
   ↓
Target / Capability Policy
   ↓
Simulation Adapter
   ↓
WorldState Mutation
   ↓
Narrative / Evidence / Learning Event
   ↓
UI
```

禁止：

```text
User Input
   ↓
subprocess.run(user_input)
   ↓
Real Network
```

## 3. Scenario Contract

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

场景配置应优先数据化，避免把每条剧情硬编码进 Runtime 分支。

### Target Registry

目标必须显式登记：

```text
Target ID:
Display Host/IP:
Allowed Protocols:
Allowed Services:
Simulation Adapter:
State Owner:
```

任何未登记目标都视为 Out of Scope。

## 4. Typed Action Contract

自然语言和命令必须归一化到同一动作模型。

推荐：

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

示例：

```text
“我先扫描所有 TCP 端口”
nmap -p- 10.10.10.10
        ↓
ActionIntent(kind=scan_ports)
        ↓
同一个 Simulation Handler
```

Intent Parser 只负责解释，不拥有 WorldState mutation 权限。

## 5. WorldState Contract

Session State 至少拆分：

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

不要使用一个无约束的大字典让不同组件任意覆盖。

## 6. Session & Memory Lifecycle

Paper Range 默认采用 Ephemeral Session：

```text
container start
  ↓
new SessionStore
  ↓
本次运行持续复用状态
  ↓
container stop/remove
  ↓
状态消失
```

默认验收：

- 无数据库持久化游戏 Session；
- 无 Redis durable memory；
- 无宿主机 volume 保存 WorldState；
- 新容器无法看到上一容器的战役状态。

如果产品未来需要账号进度、排行榜或课程历史，必须把 **Player Progress** 与 **Live WorldState** 分离，不能直接把整个游戏 Session 永久化。

## 7. Story Graph

剧情不应只是一串固定文案。推荐模型：

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

规则：

- 关键剧情推进由 WorldState / Evidence 驱动，不由模型随意宣告；
- 模型可以生成叙事表达，但不能绕过 Completion Condition；
- Branch 必须有可测试的 Trigger；
- Consequence 必须修改明确字段或解锁明确节点。

## 8. Learning Loop

每个场景至少回答：

```text
用户在学什么？
什么行为代表理解？
什么错误值得反馈？
Hint 如何逐步降低难度？
如何在结束后给出可行动的复盘？
```

推荐指标：

- Completion；
- Action Count；
- Hint Count；
- Invalid Action Count；
- Evidence Coverage；
- Objective Order；
- Optional Efficiency Score。

评分不应奖励“更激进的攻击动作”，而应奖励正确的侦察、证据链、边界意识和任务完成质量。

## 9. Theme Pack Contract

视觉主题与游戏逻辑分离。

```text
ThemePack
- id
- tags
- palette tokens
- typography
- panel treatment
- ambient treatment
- icon / asset references
- motion profile
```

场景只声明：

```text
theme_tags: [underground, inferno, industrial]
```

Theme Selector 决定具体主题。不要在 Scenario Runtime 中硬编码 CSS。

如果存在 40 套主题，应先做 Registry + Token Contract，再扩主题数量，而不是复制 40 份页面逻辑。

## 10. Skill Composition

本 Skill 可以请求最多 2 个 Supporting Skills：

- `agent-security-reviewer`：审查网络、文件、容器、Tool 权限边界；
- `agent-eval-hardening`：建立场景回归、轨迹、Reset、Fail-Closed 测试；
- `agent-existing-project-modifier`：已有 Paper Range 工程代码修改；
- `agent-productionizer`：Docker、发布、SRE、镜像与运行环境；
- `agent-multi-agent-designer`：只有场景确实需要多个独立 Agent 角色时使用。

不要一次加载全部 Skill。

## 11. Verification Gates

至少验证：

### Action Gate

- [ ] 自然语言和命令能映射到同一 Intent；
- [ ] Intent Parser 不直接执行真实命令；
- [ ] 未知 Action Fail Closed；
- [ ] 场景外 Target Fail Closed。

### State Gate

- [ ] 每个 Action 有确定的 State Mutation；
- [ ] 重复 Action 不破坏状态；
- [ ] Objective / Story 不能被直接跳过；
- [ ] Completion 条件可自动测试。

### Reset Gate

- [ ] 同一容器内 Session 可持续；
- [ ] 删除 Session 后状态消失；
- [ ] 后端容器重启后旧 Session 不存在；
- [ ] Compose 默认没有持久化 WorldState 的 volume。

### Learning Gate

- [ ] Hint 与评分规则确定；
- [ ] 错误动作反馈不会泄露后续全部答案；
- [ ] 完成后能生成复盘；
- [ ] 评分关注学习路径而非真实攻击强度。

### UI Gate

- [ ] 用户能看到当前 Objective；
- [ ] 用户能看到线索 / Evidence；
- [ ] 用户能输入自然语言和模拟命令；
- [ ] 世界变化有可见反馈；
- [ ] Mobile / Desktop 都能完成核心流程。

## 12. Evaluation

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

建议 Golden Trajectory：

```text
create session
→ scan
→ inspect web
→ discover credential
→ simulated access
→ mission complete
→ report
```

## 13. Deliverables

一次完整执行至少返回：

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

## 14. Return Contract

返回 Master：

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
