# Lab 18｜Agent Platform：Registry、Version、Canary 与 Rollback

> 目标：从“部署一个 Agent”升级到“管理很多 Agent、很多版本和不同发布策略”的平台工程视角。

## 1. 学习目标

完成后应能够：

- 用 AgentDefinition 描述运行配置；
- 将 Prompt / Model / Tool Set / Skill Set 版本化；
- 使用 Agent Registry 保存多个版本；
- 创建 Stable + Canary Release；
- 使用确定性流量分桶选择版本；
- 发生 Eval / SRE 问题时 Rollback；
- 理解 Control Plane 和 Data Plane 的职责边界。

## 2. 专业名词通义

- **Agent Registry**：保存 Agent 定义、版本和状态的注册表。
- **Release**：把某个 Agent Version 暴露给真实流量的发布对象。
- **Canary**：只让一小部分流量进入新版本，用线上指标验证风险。
- **Rollback**：撤销新版本流量，让系统恢复到已知稳定版本。
- **Control Plane**：管理 Agent / Tool / Policy / Release 等配置的控制面。
- **Data Plane**：真正执行每一次 Agent Task 的 Runtime / Worker。

## 3. 运行

```bash
cd labs/18-agent-platform
python app.py
```

## 4. Agent Definition

实验版本化：

```text
agent_id
version
prompt_version
model
allowed_tools
skills
max_steps
status
```

真实平台还应该加入：

```text
schema_version
model_settings
memory_policy
security_policy
budget_policy
eval_suite
owner
created_by
artifact_digest
```

## 5. Release Flow

```text
Agent v1 stable 100%
 ↓
register v2
 ↓
Eval Gate
 ↓
Canary: v1 90% / v2 10%
 ↓
Online Metrics
 ├─ healthy → promote v2
 └─ unhealthy → rollback v1
```

## 6. 工程原则

Worker 不应该自己决定“今天用哪个 Prompt Version”。

推荐：

```text
Task
 ↓
Release Resolver / Control Plane
 ↓
Immutable AgentDefinition
 ↓
Agent Runtime
```

Trace 必须记录最终解析到的：

```text
agent_version
prompt_version
model
skill_version
tool_version
release_id
```

否则生产问题无法复现。

## 7. 验收标准

- [ ] Registry 支持多个 Agent Version；
- [ ] Release 明确 Stable / Canary；
- [ ] 同一 routing key 始终得到稳定分桶；
- [ ] Canary 比例可配置；
- [ ] 可以 Rollback；
- [ ] Runtime 只消费解析后的 AgentDefinition；
- [ ] 能说明 Eval Gate 与 Canary 的区别；
- [ ] 能画出 Control Plane / Data Plane 架构。
