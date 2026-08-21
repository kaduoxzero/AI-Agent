# Agent Registry、Versioning 与 Release Governance

> 目标：把 Agent、Prompt、Tool、Skill、Model Policy 从“代码里的配置”变成可以注册、评估、发布、回滚和审计的工程资产。

## 1. 为什么 Agent 也需要发布治理

Agent 行为不仅由代码决定，还由以下资产共同决定：

```text
Agent Definition
Prompt
Model
Tool
Skill
RAG Config
Memory Policy
Workflow
Runtime Policy
Security Policy
```

任何一个变化都可能改变线上行为。

所以：

> Agent Release ≠ Git Commit。

一次正式 Release 应明确绑定所有关键版本。

## 2. 专业名词通义

- **Registry（注册中心）**：保存资产 ID、版本、Owner、状态和元数据，并支持发现。
- **Release Manifest（发布清单）**：描述一次 Agent 发布实际绑定的所有组件版本。
- **Promotion（晋级）**：同一个制品从 Dev → Staging → Production，而不是重新随意构建。
- **Canary（金丝雀发布）**：只把少量流量分配到新版本，观察后再扩大。
- **Rollback（回滚）**：快速恢复到已知稳定 Release。

## 3. Registry 资源模型

### Agent Registry

```text
agent_id
version
owner
status
capabilities
runtime_policy
security_policy
created_at
```

### Tool Registry

```text
tool_id
version
schema
owner
side_effect
required_scopes
availability
```

### Prompt Registry

```text
prompt_id
version
hash
template
input_contract
output_contract
```

### Skill Registry

```text
skill_id
version
description
resources
compatible_agents
```

## 4. Release Manifest

```yaml
release_id: research-agent-2026.08.21.1
agent:
  id: research-agent
  version: 4.0.0
prompt:
  id: research-system
  version: 7
model_policy: research-high-quality-v3
tools:
  web.search: 2.1.0
  web.fetch: 1.4.0
skills:
  - source-verification@3.0.0
retrieval_policy: rag-v5
runtime_policy: long-task-v2
security_policy: internet-readonly-v4
```

Trace 中保存 `release_id`，即可复现一次线上行为所使用的配置组合。

## 5. 状态生命周期

推荐：

```text
DRAFT
 ↓
EVALUATING
 ↓
APPROVED
 ↓
STAGING
 ↓
CANARY
 ↓
PRODUCTION
 ↓
DEPRECATED
```

禁止未经 Eval 的 Draft 直接切 Production。

## 6. Eval Gate

Release 前必须运行与变更类型相关的 Eval。

例如 Prompt 修改：

```text
Task Eval
Tool Selection Eval
Security Eval
Cost Regression
```

Tool Schema 修改：

```text
Schema Compatibility
Integration Test
Trajectory Regression
Permission Test
```

## 7. Canary

推荐分流依据：

```text
5% tasks → candidate release
95% tasks → stable release
```

比较：

```text
success
quality
latency
cost
tool errors
human override
security events
```

自动扩大流量前必须定义阈值。

## 8. Rollback

Rollback 必须是平台能力，不是人工改代码：

```text
Production Pointer
candidate-v4 → stable-v3
```

注意 Checkpoint Compatibility：

> 一个由 v4 创建的长任务是否允许由 v3 Runtime 恢复？

必要时固定任务到原 Release 直到结束。

## 9. Ownership

每个资产必须有 Owner：

```text
Agent Owner
Tool Owner
Prompt Owner
Policy Owner
Dataset Owner
```

没有 Owner 的生产资产无法长期治理。

## 10. Change Audit

记录：

```text
who
what
old_version
new_version
why
approval
eval_result
release_time
rollback_time
```

不要只依赖 Git history，因为运行时配置可能来自平台数据库。

## 11. Compatibility

Tool / Artifact / Event Schema 需要声明兼容性。

```text
Agent v4 requires Tool >=2.0,<3.0
```

平台在 Release 阶段检查，不要等线上才发现。

## 12. 实训

给毕业项目实现：

```text
GET /agents
POST /agents/{id}/releases
POST /releases/{id}/evaluate
POST /releases/{id}/promote
POST /releases/{id}/rollback
```

要求：

- 生产 Release 不可直接编辑；
- 修改后生成新 Release；
- Canary 可以按 tenant / percentage 分流；
- Trace 保存 release_id；
- Eval 不达标禁止 promote。

## 13. 检查清单

- [ ] Agent 行为所依赖的所有资产是否可版本化？
- [ ] 是否有 Release Manifest？
- [ ] Trace 是否记录 release_id？
- [ ] 是否有 Eval Gate？
- [ ] 是否支持 Canary / Rollback？
- [ ] Checkpoint 是否考虑跨版本恢复？
- [ ] 每个资产是否有明确 Owner？