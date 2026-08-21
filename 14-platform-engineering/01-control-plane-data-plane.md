# Agent Platform Engineering：Control Plane 与 Data Plane

> 目标：从“开发一个 Agent”升级到“建设一个可以管理大量 Agent、模型、Tool、Prompt、Skill、Policy 和运行实例的平台”。

## 1. 为什么需要 Agent Platform

当系统只有 1~3 个 Agent 时，可以把配置写在代码里；当企业内部出现几十到数百个 Agent 后，问题会迅速变成：

- Agent 谁创建、谁负责、谁能上线；
- Agent 使用哪个模型、哪个 Prompt 版本；
- Agent 可以调用哪些 Tool；
- Tool 的权限、Secret 和租户边界如何控制；
- 不同团队如何复用 MCP Server / Skill；
- Agent 运行失败后如何定位；
- 如何统一 Eval、发布、回滚和审计。

这时需要的已经不是单个 Agent Framework，而是 **Agent Platform**。

## 2. 专业名词通义

- **Control Plane（控制面）**：负责“管理和配置”，通常不直接执行用户任务，例如 Registry、Policy、版本、发布、权限和治理。
- **Data Plane（数据面 / 执行面）**：真正处理 Agent Run、Model Call、Tool Call、RAG、Workflow 的运行层。
- **Registry（注册中心）**：保存 Agent、Tool、Skill、Model 等资源的可发现元数据与版本。
- **Desired State（期望状态）**：平台声明“某个 Agent 应该以什么版本、配置和权限运行”。

## 3. 总体架构

```text
                         Control Plane

   Agent Registry   Tool Registry   Skill Registry
          │              │               │
   Prompt Version    Policy Engine   Model Catalog
          │              │               │
          └──────── Deployment / Release ────────┐
                                                 │
─────────────────────────────────────────────────┼────
                                                 │
                         Data Plane              ↓

User → API → Task Service → Queue → Agent Runtime
                                  ├─ Model Gateway
                                  ├─ Tool Gateway / MCP
                                  ├─ RAG / Memory
                                  ├─ Sandbox
                                  ├─ Checkpoint
                                  └─ Event / Trace
```

## 4. Control Plane 应管理什么

### 4.1 Agent Definition

建议 Agent 不只是一个 Prompt，而是版本化资源：

```yaml
id: research-agent
version: 3.2.0
owner: risk-team
model_policy: research-default
tools:
  - web.search
  - web.fetch
skills:
  - source-verification
runtime_policy: long-task-standard
security_policy: internet-readonly
```

### 4.2 Tool / MCP Registry

注册信息至少包括：

```text
tool_id
version
owner
input_schema
output_schema
permission_level
side_effect
rate_limit
required_scopes
health_status
```

不要只保存一个 Tool description。

### 4.3 Prompt / Skill Version

Prompt 和 Skill 都是可部署资产，应支持：

```text
Draft → Eval → Approved → Canary → Production → Deprecated
```

### 4.4 Policy

Policy Engine 用于执行确定性规则：

```text
用户是否允许调用该 Tool？
Agent 是否可以访问该 Tenant？
金额超过多少必须 HITL？
某类数据是否禁止发送到外部模型？
```

不要把这类规则交给 LLM 自己判断。

## 5. Data Plane 的职责

Data Plane 关注执行：

```text
接受 Task
→ 加载 Agent Definition
→ 构建 Context
→ 执行 Agent Loop / Graph
→ 调 Model / Tool
→ 保存 Checkpoint
→ 发出 Event
→ 返回 Artifact
```

Data Plane 应尽量做到：

- Runtime 无状态或最小本地状态；
- 持久状态放 durable store；
- Agent Definition 可缓存；
- 运行实例可以水平扩展。

## 6. Agent Release

推荐 Agent 也采用发布流水线：

```text
Change Prompt / Model / Tool / Workflow
          ↓
Static Validation
          ↓
Eval Suite
          ↓
Security Eval
          ↓
Staging
          ↓
Canary
          ↓
Production
```

## 7. 多租户

每一个 Run 都应显式携带：

```text
tenant_id
user_id
agent_id
agent_version
task_id
trace_id
```

所有 RAG、Memory、Tool、Artifact、Trace 查询都必须带 Tenant 边界。

### 反模式

```text
全平台共享一个 Vector DB namespace
所有 Agent 共用一个管理员 Token
Prompt 只存在代码里且无版本
Tool 变更后没有 Eval
```

## 8. 平台最小落地版本

不要第一天就造“Agent Kubernetes”。推荐分阶段：

### Phase 1

```text
Agent Config in Git
+ Model Gateway
+ Tool Registry
+ Trace
+ Eval
```

### Phase 2

```text
Agent Registry Service
+ Policy Engine
+ Version / Release
+ Tenant / RBAC
```

### Phase 3

```text
Control Plane UI
+ Dynamic Deployment
+ Fleet Health
+ Cost Governance
+ Agent Identity
```

## 9. 检查清单

- [ ] Agent 是否有唯一 ID、Owner 和 Version？
- [ ] Tool / Prompt / Skill 是否版本化？
- [ ] Policy 是否由确定性系统执行？
- [ ] Control Plane 与 Data Plane 是否解耦？
- [ ] 每个 Run 是否携带 Tenant / Agent / Trace 标识？
- [ ] Agent 变更是否经过 Eval Gate？
- [ ] 是否可以 Canary 与 Rollback？

## 10. 实训建议

将毕业项目改造为一个最小 Agent Platform：

1. PostgreSQL 建 `agent_definitions`、`tool_registry`、`agent_releases`；
2. Agent Worker 启动任务时按 `agent_id + version` 加载配置；
3. 新 Prompt 版本必须跑 Eval；
4. 只有通过阈值的版本可以标记为 Production；
5. Trace 中记录实际运行的所有 Version。