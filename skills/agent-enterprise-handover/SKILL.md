---
name: agent-enterprise-handover
version: 1.0.0
description: Enterprise-grade project and engineering handover orchestrator. Use for ownership transfer, developer replacement, leave/rotation handoff, module handover, Agent-to-Agent context transfer, project takeover, or auditing whether a project can continue without the original owner. Produces evidence-backed business, architecture, code, data, runtime, operations, permission, risk, runbook, knowledge-transfer and acceptance artifacts instead of a simple status summary.
---

# Agent Enterprise Handover

## 1. Objective

把“写一份交接文档”升级为一次完整的 **Ownership Transfer（所有权转移）+ Knowledge Transfer（知识转移）+ Asset Transfer（资产转移）+ Operability Transfer（可运营能力转移）**。

最终目标不是“文档看起来完整”，而是：

> 假设原负责人从交接完成后立即无法联系，接手人仍然能够独立理解项目、启动系统、修改代码、验证功能、发布版本、回滚、排障、恢复服务并继续推进后续工作。

本 Skill 是交接流程的 **Master / Aggregator**，负责发现、编排、证据聚合、缺口审计、验收和最终交接结论；它不应重复实现仓库中已有专项 Skill 的专业能力。

---

## 2. When to Use

出现以下任一意图时使用本 Skill：

- 项目整体交接、离职交接、调岗交接、轮岗交接；
- 某个模块、服务、Agent、RAG、数据库、前端或后端交给其他人；
- 开发做到一半需要换人继续；
- 接手别人项目，需要判断资料是否完整；
- 需要生成“新人接手后可以直接干活”的交接包；
- 需要把口头知识、聊天记录、个人经验沉淀成 Runbook；
- 需要审查现有交接文档是否达到可接手标准；
- 需要 Agent-to-Agent / Coding Agent-to-Agent 上下文交接；
- 需要在项目结束、阶段结束、Sprint 结束时形成可追踪的交接快照。

如果只是写普通周报、工作总结、日报、版本说明，不使用本 Skill。

---

## 3. Handover Definition

一次完整交接必须同时覆盖四个维度：

```text
Knowledge Transfer
  业务背景 / 架构理由 / 历史决策 / 隐性知识 / 已知坑

Asset Transfer
  Repo / 文档 / 数据 / 配置 / 环境 / 外部资源 / 权限入口

Responsibility Transfer
  Owner / RACI / 审批 / 发布责任 / 事故升级路径

Operability Transfer
  启动 / 开发 / 测试 / 发布 / 回滚 / 监控 / 排障 / 恢复
```

任何一个维度缺失，都不能仅因为“有文档”而判定交接完成。

---

## 4. Evidence Classification

所有关键结论必须标记证据等级，避免把口述、推测和事实混在一起。

| Level | 标记 | 含义 |
|---|---|---|
| A | `VERIFIED` | 通过代码、Git、配置、运行、测试、日志、数据库或监控实际验证 |
| B | `DOCUMENTED` | 来自正式文档，但尚未实际验证 |
| C | `REPORTED` | 来自交接人/用户口述 |
| D | `INFERRED` | 根据代码或上下文合理推断 |
| E | `UNKNOWN` | 当前无法确认 |

规则：

1. `INFERRED` 不能写成已确认事实；
2. `REPORTED` 的高风险信息必须尽量升级为 `VERIFIED`；
3. 启动、发布、回滚、备份恢复、生产权限等 Critical Item 不允许仅依赖 `REPORTED`；
4. 无法确认时明确写 `UNKNOWN / 待确认`，禁止补全想象中的答案。

---

## 5. Handover Modes

先识别交接模式，可组合使用。

### H1 — Full Project Handover

完整项目或 Owner 更换。启用全部交接域。

### H2 — Module Handover

只交接某模块/服务/子系统。必须同时描述上下游依赖和系统边界。

### H3 — In-Progress Development Handover

功能开发一半换人。重点：当前分支、修改文件、完成状态、失败测试、临时实现、Next Exact Action。

### H4 — Operations Handover

重点：环境、服务、端口、中间件、发布、回滚、日志、监控、告警、备份、事故处理。

### H5 — AI / Agent Handover

重点：Agent、Workflow、State、Router、Prompt、Tool、Skill、Memory、RAG、Model、Evaluation、Guardrail、Tracing、Cost。

### H6 — Product / Business Handover

重点：业务背景、业务规则、目标用户、产品状态、Roadmap、业务指标、Stakeholder、历史决策。

### H7 — Temporary Handover

请假、短期代管等，生成精简版 Handover Card，不强制完整项目资产盘点。

### H8 — Takeover Audit

接手别人项目，重点不是“帮原负责人整理”，而是从接手人视角找缺口、SPOF 和无法继续工作的地方。

### H9 — Agent-to-Agent Transfer

使用压缩的 Context Transfer Contract，保证下一 Agent 不需要重新猜测任务状态。

---

## 6. Orchestration Role

本 Skill 作为交接聚合器，应优先复用现有 Skill：

| 交接域 | 推荐专项 Skill |
|---|---|
| 需求/交接范围不清 | `agent-grill-me` |
| 项目结构、架构边界 | `agent-architecture-reviewer` |
| 已有项目代码现状与影响面 | `agent-existing-project-modifier` |
| 故障、异常、已知问题复现 | `agent-debugger` |
| RAG / Knowledge Base | `agent-rag-engineer` |
| Multi-Agent / Handoff | `agent-multi-agent-designer` |
| 测试、回归、验证证据 | `agent-eval-hardening` |
| 权限、Secret、Injection、安全边界 | `agent-security-reviewer` |
| Runbook、服务化、SRE、运行能力 | `agent-productionizer` |
| 延迟、容量、Token、成本 | `agent-performance-cost-optimizer` |

遵守 Master 的动态加载限制：

- 任一时刻 Primary Skill = 1；
- Supporting Skills <= 2；
- 不允许一次加载全部 Skill；
- 按交接阶段顺序执行，处理完一个域后返回本 Skill 聚合结果。

如果专项 Skill 不可用，本 Skill必须使用自身检查清单完成最低限度审计，而不是直接跳过该域。

---

## 7. Handover Lifecycle

统一生命周期：

```text
0. Scope & Ownership Freeze
        ↓
1. Asset Inventory
        ↓
2. Repository & System Discovery
        ↓
3. Business / Architecture Knowledge Capture
        ↓
4. Runtime / Operations Capture
        ↓
5. Risk / Debt / Hidden Knowledge Audit
        ↓
6. Handover Package Generation
        ↓
7. Knowledge Transfer & Shadow
        ↓
8. Reverse Shadow
        ↓
9. Acceptance Gates
        ↓
10. Archive & Ownership Transfer
```

不能因为文档已经生成就跳过 7~9 阶段。

---

# 8. Phase 0 — Scope & Ownership Freeze

先建立 Handover Charter。

必须明确：

```text
项目名称：
交接类型：
交接原因：
交接范围：
明确不在交接范围：
原 Owner：
新 Owner：
业务 Owner：
技术 Owner：
审批/验收人：
目标完成时间：
涉及环境：Local / Dev / Test / Staging / Prod
```

如果用户已提供，不重复询问。

如果能从仓库、项目状态、Git、配置或已有文档中自动获得，优先自行发现。

### Scope Matrix

复杂项目创建：

| Domain | In Scope | Current Owner | New Owner | Status |
|---|---|---|---|---|
| Business | | | | |
| Product | | | | |
| Frontend | | | | |
| Backend | | | | |
| Database | | | | |
| AI / Agent | | | | |
| Infrastructure | | | | |
| Security | | | | |
| Operations | | | | |
| Third-party | | | | |

---

# 9. Phase 1 — Asset Inventory

交接前建立资产清单，至少检查：

## 9.1 Code Assets

- Repository / Monorepo / Submodule；
- 默认分支、Release 分支、Hotfix 分支；
- Tag / Release；
- Private Package / Internal Library；
- Script / Migration / Seed；
- Git LFS / 大文件资产。

## 9.2 Documentation Assets

- README；
- PRD / Requirement；
- Architecture；
- ADR / Decision Record；
- API 文档；
- Database / ER；
- Runbook；
- Test Plan / Test Cases；
- Incident / Postmortem；
- Security；
- Roadmap；
- Meeting Notes / Recording。

每份文档必须标记：`CURRENT / OUTDATED / PARTIAL / UNKNOWN`。

## 9.3 Runtime Assets

- Server / VM / Container / Kubernetes；
- MySQL / PostgreSQL / Redis / MQ / Elasticsearch / Vector DB；
- Nacos / Config Center；
- Object Storage；
- Domain / DNS / Certificate；
- CI/CD；
- Monitoring / Logging / Tracing。

## 9.4 External Assets

- OAuth；
- 微信/企业微信/小程序/公众号；
- 邮件/短信；
- 云平台；
- LLM / Embedding Provider；
- 支付/地图/外部 API；
- Vendor / Supplier。

## 9.5 Access Assets

只记录：

```text
Resource
Required Role
Permission Level
Apply Method
Owner
Status
```

禁止在普通交接文档中记录真实密码、API Key、Token、Private Key。

---

# 10. Phase 2 — Repository & System Discovery

如果能够访问代码，不允许只根据 README 生成交接。

最低 Discovery 顺序：

```text
README
→ Repository Tree
→ Build Files
→ Configuration
→ Entrypoints
→ Core Modules
→ Database / Migration
→ API
→ Tests
→ Scripts
→ CI/CD
→ Deployment
→ Git History
```

## 10.1 Git Snapshot

必须记录：

```text
Repository:
Remote:
Default Branch:
Current Branch:
Latest Commit:
Latest Tag:
Working Tree:
Ahead / Behind:
Stash:
Untracked Files:
Submodule:
Git LFS:
```

强制检查：

- 未提交修改；
- 未 Push Commit；
- 未合并 Branch；
- Stash；
- 冲突；
- 临时文件；
- 本地绝对路径；
- 明文 Secret；
- 仅存在个人电脑的脚本。

存在任一项时进入 `Handover Blocker / Risk`，不得默认为无影响。

## 10.2 Repository Map

只保留高价值目录：

```text
project/
├─ docs/
├─ backend/
├─ frontend/
├─ agent/
├─ migrations/
├─ scripts/
├─ tests/
└─ deploy/
```

禁止机械列出 `node_modules`、`target`、`dist`、`.idea`、`__pycache__` 等无交接价值目录。

## 10.3 Critical Entrypoints

必须定位：

- Application Entrypoint；
- Controller / API Entrypoint；
- Core Service；
- Repository / DAO；
- Job / Scheduler；
- Consumer / Producer；
- Workflow / Agent Entrypoint；
- Config Entrypoint；
- Test Entrypoint。

---

# 11. Phase 3 — Business & Architecture Knowledge Capture

## 11.1 Business Context

必须回答：

- 项目为什么存在？
- 给谁使用？
- 核心目标是什么？
- 最核心的业务流程是什么？
- 哪些业务规则不在代码里或不在 PRD 里？
- 哪些异常流程需要人工介入？
- 当前真正被使用的功能有哪些？
- 哪些功能名义存在但实际上已经停用？

## 11.2 Business Glossary

建立术语表，防止不同团队同词不同义。

| Term | 中文/业务名 | Definition | Source |
|---|---|---|---|

## 11.3 Core Flow

至少区分：

```text
Normal Flow
Exception Flow
Compensation Flow
Manual Flow
```

## 11.4 Architecture

必须说明：

- 系统边界；
- 组件关系；
- 同步调用；
- 异步链路；
- 数据流；
- 外部依赖；
- 单点；
- 核心状态；
- 关键缓存；
- 关键队列。

## 11.5 Why / ADR

关键设计不能只写 What，必须记录 Why。

ADR 最低字段：

```text
Decision:
Context:
Options:
Chosen:
Reason:
Trade-off:
Rejected Options:
Impact:
Revisit Condition:
```

优先捕获：

- 为什么使用当前数据库；
- 为什么使用 Redis / MQ；
- 为什么拆/不拆微服务；
- 为什么选择当前 Agent 架构；
- 为什么采用当前模型；
- 为什么有看起来“不合理但不能轻易删除”的兼容逻辑。

---

# 12. Code Handover

每个核心模块至少形成：

```text
模块：
职责：
入口：
关键类/函数：
上游：
下游：
状态/数据：
配置：
异常处理：
测试：
已知问题：
修改风险：
```

## 12.1 Code Hotspot

主动识别：

- 高频修改区；
- 高复杂度区；
- 高事故区；
- 高耦合区；
- 缺测试区；
- 历史兼容区。

## 12.2 Danger Zone

下列区域应默认高风险：

```text
Authentication
Authorization
Payment
Inventory
Transaction
Distributed Lock
Public API
Database Migration
Encryption
Permission
Model Guardrail
Critical Workflow State
```

明确标记：

`DO NOT MODIFY WITHOUT IMPACT ANALYSIS`

## 12.3 Code Smell Handover Audit

至少扫描：

```text
TODO / FIXME / HACK / TEMP
Deprecated
Hard-coded Secret
Magic Number
Empty Catch
Disabled Validation
Mock / Bypass
Local Path
Commented-out Critical Code
```

发现内容进入 Technical Debt Register，不允许隐藏。

---

# 13. Data & Database Handover

必须记录：

```text
Database Type / Version
Schema
Timezone
Encoding
Connection Pool
Migration Tool
Latest Migration
Pending Migration
Backup
Restore
Replication / HA
```

## 13.1 Critical Tables

| Table | Purpose | Critical Fields | Relationships | Risk |
|---|---|---|---|---|

## 13.2 Data Classification

至少区分：

- 核心业务数据；
- 可重建数据；
- 缓存数据；
- 审计日志；
- PII / 敏感数据；
- 临时数据；
- 不可恢复数据。

## 13.3 Data Lifecycle

描述：

```text
Create → Read → Update → Archive → Delete → Backup → Restore
```

## 13.4 Migration Rule

必须确认：

```text
如何升级？
是否向后兼容？
生产执行顺序？
失败后如何处理？
是否支持回滚？
```

---

# 14. API & Contract Handover

建立 API Inventory：

| API | Method | Caller | Auth | Status | Owner |
|---|---|---|---|---|---|

重要接口说明：

```text
Request
Response
Error Code
Auth
Idempotency
Timeout
Retry
Rate Limit
Compatibility
```

特别标记：

`PUBLIC / INTERNAL / DEPRECATED / EXPERIMENTAL / MOCK / TEMPORARY / CALLBACK / WEBHOOK / THIRD-PARTY`

---

# 15. Environment Handover

严格区分：

```text
Local
Development
Test
Staging / Pre-production
Production
```

不要把不同环境的主机、数据库、配置混在同一段落。

## 15.1 Environment Matrix

| Item | Local | Test | Staging | Prod |
|---|---|---|---|---|

## 15.2 Toolchain

记录版本：

```text
OS
JDK
Maven / Gradle
Node / npm / pnpm
Python / Conda
Docker
IDE（若有强依赖）
```

## 15.3 Secrets Policy

文档只记录：

```text
Secret Name
Secret Store / Location
Access Method
Owner
Rotation Policy
```

不得复制真实 Secret。

---

# 16. Build / Startup / Verification

## 16.1 Build

必须说明：

```text
Build Command
Artifact
Artifact Location
Dependency Source
Private Registry
Success Signal
```

## 16.2 Startup Runbook

接手人应能复制命令执行。

记录：

```text
Preconditions
Dependency Order
Commands
Ports
Health Check
Success Signal
Common Failure
```

## 16.3 Dependency Order

例如：

```text
MySQL
 ↓
Redis
 ↓
Config Center
 ↓
Backend
 ↓
Agent Service
 ↓
Frontend
```

## 16.4 Verification

禁止写“项目可以正常运行”而没有证据。

每个核心能力至少提供：

```text
Verification ID:
Precondition:
Command / Action:
Expected:
Actual:
Evidence:
Status:
```

---

# 17. Testing Handover

至少盘点：

```text
Unit
Integration
API
E2E
Regression
Smoke
Performance
Security
AI Eval
```

记录 Baseline：

```text
Total Tests
Passed
Failed
Skipped
Coverage
Known Flaky Tests
Known Untested Critical Paths
```

如果没有测试，明确写缺口，不允许写“待后续完善”后继续判定 Full Handover。

---

# 18. Release & Rollback Handover

完整项目或运维交接必须包含 Release Runbook。

## 18.1 Release

```text
Who Can Release
Approval
Release Window
Pre-check
Build
Deploy
Migration
Smoke Test
Monitoring Window
Success Criteria
```

## 18.2 Rollback

必须回答：

- 谁决定回滚；
- 触发条件；
- 代码如何回滚；
- 配置如何回滚；
- 数据库如何处理；
- 数据不兼容如何处理；
- 回滚后如何验证。

如果核心系统“能发布但不能明确回滚”，至少标记 P0/P1 Operational Risk。

---

# 19. Observability & Incident Handover

## 19.1 Logs

明确：

```text
日志平台/路径
关键日志文件
Trace ID / Request ID
如何检索
如何识别核心错误
```

## 19.2 Metrics

根据项目选择：

```text
QPS
P50 / P95 / P99
Error Rate
CPU / Memory
DB Connections
Queue Lag
LLM Latency
Token Usage
Tool Success Rate
```

## 19.3 Alert

每个关键 Alert：

```text
Alert:
Meaning:
Severity:
First Action:
Owner:
Escalation:
```

## 19.4 Incident History

重大事故记录：

| Date | Incident | Impact | Root Cause | Fix | Lesson |
|---|---|---|---|---|---|

## 19.5 Troubleshooting Tree

高频问题建立决策树，不要只写零散经验。

Runbook 条目统一使用：

```text
Symptom
Impact
Diagnosis
Commands
Resolution
Verification
Rollback
Escalation
```

---

# 20. Backup / Recovery / Continuity

重要系统检查：

```text
Backup Scope
Frequency
Retention
Storage
Encryption
Restore Procedure
Restore Test Date
RTO
RPO
Failover / DR
Owner
```

如果有备份但从未验证 Restore，不得把“可恢复”标记为 VERIFIED。

---

# 21. Security & Permission Handover

至少检查：

```text
Authentication
Authorization / RBAC
Secrets
Certificate
Firewall / Whitelist
Sensitive Data
Audit Log
Dependency Vulnerability
Privileged Tools
Production Access
```

## Permission Matrix

| Resource | Role | Permission | Apply Method | Owner | Status |
|---|---|---|---|---|---|

禁止在交接文档里直接保存凭据。

---

# 22. Third-party / Vendor Handover

建立 Dependency Register：

| Service | Usage | Owner | SLA | Expiry | Fallback | Risk |
|---|---|---|---|---|---|---|

必须识别：

- 只有一个管理员账号；
- API Key 属于个人账号；
- 服务合同即将到期；
- 无替代 Provider；
- 第三方回调配置只有原负责人知道。

---

# 23. AI / Agent Handover Extension

检测到 AI 项目时强制启用。

## 23.1 Agent Inventory

| Agent | Responsibility | Input | Output | Tools | Boundary |
|---|---|---|---|---|---|

## 23.2 Workflow

说明：

```text
START
 ↓
Intent / Router
 ↓
Agent / Workflow
 ↓
Tool / RAG
 ↓
Validator / Guardrail
 ↓
HITL（如需要）
 ↓
END
```

## 23.3 State

区分：

```text
Global State
Workflow State
Agent State
Session State
Persistent State
Checkpoint
```

## 23.4 Prompt

记录：

```text
Prompt Type
Location
Version
Dynamic Variables
Owner
Fallback
Change Risk
```

禁止只复制 Prompt 而不说明用途和变量。

## 23.5 Model

记录：

```text
Provider
Model
Reasoning Level
Temperature / Sampling
Max Tokens
Timeout
Retry
Fallback
Selection Rationale
Cost / Latency Baseline
```

## 23.6 Tool / MCP

每个 Tool：

```text
Purpose
Input
Output
Permission
Side Effect
Failure Strategy
HITL Requirement
```

MCP 增加：Server / Transport / Auth / Exposed Tools。

## 23.7 Memory

区分：Conversation / Session / Long-term / User / Business Memory，并明确 Persistence 和删除策略。

## 23.8 RAG

记录：

```text
Data Source
Loader / Parser
Cleaning
Chunk Strategy
Embedding
Vector DB / Collection
Retriever
Top-K
Rerank
Metadata / ACL
Citation
Update Pipeline
Evaluation
```

## 23.9 Evaluation

至少记录：

```text
Dataset
Golden Cases
Metrics
Baseline
Latest Result
Known Failure Cases
Regression Gate
```

AI Failure Case 建议保留：

```text
Input
Wrong Output
Expected
Root Cause
Workaround / Fix
```

---

# 24. Ownership / RACI / Escalation

完整交接必须建立责任关系。

RACI：

- R — Responsible，实际执行；
- A — Accountable，最终负责；
- C — Consulted，需要咨询；
- I — Informed，需要同步。

| Activity | R | A | C | I |
|---|---|---|---|---|
| Requirement | | | | |
| Code Change | | | | |
| Release | | | | |
| DB Migration | | | | |
| Production Incident | | | | |
| Security Incident | | | | |

同时记录 Escalation Path：

```text
L1 → L2 → Technical Owner → Business Owner / Management
```

明确“什么问题升级到谁”，而不是只给联系人列表。

---

# 25. Hidden Knowledge & SPOF Audit

主动寻找以下隐性依赖：

```text
只有某个人知道的命令
只存在个人电脑的脚本
聊天记录中的业务规则
未提交 SQL
个人账号下的第三方资源
手工发布步骤
特殊缓存清理
本地 Mock / 临时绕过
没有文档的历史兼容规则
“这个只能问 XXX”
```

这些内容进入 `Tribal Knowledge Register`。

如果某模块知识或权限只掌握在一个人手里，标记：

`Knowledge SPOF / Bus Factor = 1`

并作为交接风险处理。

---

# 26. Technical Debt / Issue / Risk Registers

## 26.1 TODO

禁止：

```text
继续优化
完善系统
处理剩余问题
```

必须写成：

```text
TODO-ID:
Task:
Context:
Priority:
Location:
Dependency:
Recommended Approach:
Acceptance Criteria:
Owner:
```

## 26.2 Known Issue

```text
ISSUE-ID:
Severity:
Impact:
Trigger:
Root Cause:
Workaround:
Permanent Fix:
Verification:
```

## 26.3 Technical Debt

```text
DEBT-ID:
Description:
Reason:
Impact:
Risk:
Suggested Solution:
Priority:
```

## 26.4 Risk

```text
RISK-ID:
Category:
Probability:
Impact:
Level:
Trigger:
Mitigation:
Contingency:
Owner:
```

Priority 使用：

- P0：生产、安全、数据损坏或核心不可用；
- P1：核心功能或可运营性严重受影响；
- P2：重要问题，有绕行方案；
- P3：普通优化。

---

# 27. Knowledge Transfer Procedure

文档只是 KT 的一个载体。

复杂项目建议按 Session 切分：

```text
Session 1 — Business & Product
Session 2 — Architecture & Code
Session 3 — Data & External Dependencies
Session 4 — Runtime / Release / Incident
Session 5 — AI / Agent（如适用）
Session 6 — Open Questions & Acceptance
```

如果组织允许录屏，建立 Recording Index：

```text
Recording:
Date:
Participants:
00:00 项目背景
08:30 架构
20:10 数据库
32:00 发布
45:30 故障排查
```

不要只有一个长视频而没有时间索引。

---

# 28. Shadow & Reverse Shadow

## Shadow

原负责人操作，接手人观察：

- 启动；
- 修改；
- 测试；
- 发布；
- 日志查询；
- 常见排障。

## Reverse Shadow

接手人实际操作，原负责人仅观察。

推荐至少验证：

```text
Clone / Checkout
Build
Run
核心业务 Smoke Test
修改一个小功能
执行测试
定位一个已知问题
查询日志/监控
```

重要系统增加：

```text
Release
Rollback
Backup Restore
Incident Drill
```

接手人无法独立完成关键 Reverse Shadow 时，交接不得标记 COMPLETE。

---

# 29. Day 0 / Day 1 / Day 3 / Day 7 Acceptance

## Day 0 — Access Ready

- Repository；
- 文档；
- Dev/Test；
- 数据库；
- Monitoring；
- 必要 Third-party 权限。

## Day 1 — Runtime Ready

接手人能够：

```text
Clone → Build → Run → Health Check → Core Smoke Test → Read Logs
```

## Day 3 — Development Ready

能够：

- 理解架构；
- 修改小功能；
- 运行测试；
- 定位普通 Bug。

## Day 7 — Ownership Ready

能够：

- 独立完成常规开发；
- 独立完成常规发布；
- 独立处理普通事故；
- 知道高风险问题升级路径。

## Day 30 — Dependency Review（长期项目）

检查是否仍大量依赖原负责人，并把新发现的 Tribal Knowledge 补入文档。

---

# 30. Acceptance Gates

交接必须经过 Gate，而不是凭感觉签字。

## Gate A — Scope Ready

交接范围与 Owner 明确。

## Gate B — Asset Ready

核心代码、文档、数据、外部资源可以访问。

## Gate C — Knowledge Ready

业务、架构、关键决策、Known Issues 已被捕获。

## Gate D — Runtime Ready

接手人可独立启动并完成核心 Health/Smoke 验证。

## Gate E — Development Ready

接手人可修改、测试、定位普通问题。

## Gate F — Operations Ready

发布、回滚、日志、监控、告警、故障处理明确。

## Gate G — Security & Permission Ready

必要权限已到位且凭据管理符合安全要求。

## Gate H — Ownership Ready

RACI、Escalation、最终 Owner 明确。

## Gate I — Reverse Shadow Passed

接手人实际完成关键操作。

---

# 31. Critical Blocker Override

出现以下任一情况，不允许判定 `COMPLETE`，即使评分很高：

```text
核心仓库无法访问
接手人无法启动项目
关键代码仍只存在原负责人本地
生产 Owner 不明确
关键数据库关系未知
发布流程只有原负责人知道
无法说明核心回滚方案
关键权限未移交
关键 Secret 只保存在个人设备
核心未提交修改未处置
核心数据无恢复策略且业务要求可恢复
Reverse Shadow 关键项失败
```

---

# 32. Handover Score — 200 Points

| Domain | Score |
|---|---:|
| Business & Product | 15 |
| Architecture & Decisions | 20 |
| Code & Repository | 20 |
| Data & API | 20 |
| Environment / Build / Run | 20 |
| Test & Verification | 15 |
| Release / Rollback / Operations | 20 |
| Security & Permission | 10 |
| Risk / Debt / Hidden Knowledge | 15 |
| Ownership / RACI | 10 |
| Knowledge Transfer | 10 |
| Reverse Shadow | 15 |
| Documentation Consistency | 10 |
| **Total** | **200** |

结果：

```text
180–200  Level A — Ready
160–179  Level B — Ready with Minor Gaps
130–159  Level C — Conditional Handover
100–129  Level D — High Dependency
<100     Level E — Handover Failed
```

Critical Blocker Override 优先级高于总分。

---

# 33. Documentation Drift Audit

交接期间必须检查事实和文档是否漂移：

```text
README vs Code
Architecture Doc vs Actual Dependencies
API Doc vs Controller / Schema
Database Doc vs Migration
Config Doc vs Actual Config
Runbook vs Actual Command
Test Doc vs Current Test Suite
TODO vs Git / Issue State
```

输出：

| Document | Reality | Difference | Severity | Action |
|---|---|---|---|---|

---

# 34. Security / Local Dependency Audit

主动检查：

```text
.env
application*.yml
config*.py / ts / js
Docker Compose
Shell / PowerShell
README
CI Config
Prompt / Tool Config
```

寻找：

- Secret；
- 本地绝对路径；
- 个人账号；
- localhost-only dependency；
- 个人目录模型/数据；
- 绕过认证；
- 临时白名单。

发现 Secret 时不要复制到交接文档，只报告暴露位置并要求轮换/迁移。

---

# 35. Project Handover Artifacts

默认在当前业务项目下创建：

```text
<project>/.agent-engineering/交接/
├─ 00-交接总览.md
├─ 01-资产清单.md
├─ 02-业务与产品.md
├─ 03-架构与关键决策.md
├─ 04-代码与仓库.md
├─ 05-数据与接口.md
├─ 06-环境与配置.md
├─ 07-运行手册.md
├─ 08-测试与验证.md
├─ 09-发布与回滚.md
├─ 10-监控与故障.md
├─ 11-安全与权限.md
├─ 12-AI-Agent专项.md          # 仅 AI 项目
├─ 13-已知问题与技术债.md
├─ 14-风险与SPOF.md
├─ 15-RACI与升级路径.md
├─ 16-KT与录屏索引.md
├─ 17-交接验收.md
└─ 18-最终交接报告.md
```

规则：

- 小型项目可以合并，不为了形式创建空文件；
- 正文默认简体中文；
- 技术标识符保留英文；
- `skills/templates/` 是只读模板，不能写入项目数据；
- 用户指定其他输出目录时遵从用户要求；
- 交接过程的关键阶段结论仍应按项目状态策略同步到 `.agent-engineering/` 的长期状态和 `history/`。

---

# 36. Required Templates

本 Skill 可读取：

```text
../templates/handover-master.md
../templates/handover-evidence-register.md
../templates/handover-runbook.md
../templates/handover-risk-register.md
../templates/handover-acceptance.md
```

模板只负责结构，不允许直接写入模板文件保存项目数据。

---

# 37. Minimal Output for Temporary Handover

临时交接允许压缩为：

```text
任务/模块：
最终目标：
当前状态：
已完成：
正在进行：
未完成：
阻塞：
相关文件：
相关环境：
验证方法：
已知问题：
注意事项：
下一步精确动作：
临时代管 Owner：
```

---

# 38. Agent-to-Agent Context Transfer Contract

Agent-to-Agent 交接时必须输出：

```text
Goal:
Scope:
Out of Scope:
Current State:
Completed:
In Progress:
Blocked:
Files Changed:
Relevant Components:
Decisions Made:
Constraints:
Assumptions:
Known Issues:
Verification Evidence:
Unresolved Questions:
Next Exact Action:
Return / Stop Condition:
```

禁止使用：

```text
继续完成
继续优化
按照之前方案继续
处理剩余内容
```

`Next Exact Action` 应具体到文件、函数、测试或命令。

---

# 39. Incremental Interview Rule

无法访问代码或资料时，采用阶段式访谈：

```text
Scope
→ Business
→ Architecture
→ Code/Data
→ Environment
→ Operations
→ Risk
→ Acceptance
```

一次只询问当前阶段最关键的信息，不要一次抛出几十个问题。

优先级：

```text
已有信息
→ 仓库可发现
→ 项目状态可读取
→ 安全默认值
→ Agent 合理建议
→ 用户关键决策
```

用户已经回答的信息不得重复询问。

---

# 40. Final Audit Simulation

宣布完成前，模拟以下场景：

1. 原负责人立即无法联系，我能启动项目吗？
2. 核心 API 出现 500，我知道从哪里开始排查吗？
3. 数据库连接失败，我知道配置、Owner 和影响范围吗？
4. 今天需要发布，我能独立完成吗？
5. 发布失败，我能安全回滚吗？
6. 核心数据异常，我知道备份和恢复路径吗？
7. 第三方服务不可用，我知道联系人和替代方案吗？
8. 业务问“为什么这样设计”，我能找到决策依据吗？
9. 接手人是否真正执行过，而不是只看过文档？
10. 是否仍有“只能问原负责人”的关键知识？

核心问题任一答案为“否”，必须进入 Critical Gap 或 Risk。

---

# 41. Final Status

最终状态只允许：

### COMPLETE

关键 Gate 全通过、无 Critical Blocker、Reverse Shadow 通过。

### CONDITIONAL

可以接手，但存在明确的非关键缺口和限期补齐事项。

### INCOMPLETE

存在关键知识、资产、运行或权限缺口。

### BLOCKED

因权限、资产、人员、环境或数据原因无法继续完成交接。

---

# 42. Final Handover Report

最终至少输出：

```text
项目：
交接类型：
Based on Commit / Version：
交接状态：
交接评分：
Critical Gates：
Critical Gaps：
Major Risks：
Remaining Dependencies：
New Owner：
Acceptance Evidence：
接手后的第一项实际动作：
```

“第一项实际动作”不能写“熟悉项目”。

应类似：

```text
Checkout main → 启动依赖 → 启动 backend → 调用 /health → 执行核心 smoke test。
```

---

# 43. Return Contract to Master

返回 `agent-engineering-master` 时至少提供：

```text
Skill Used: agent-enterprise-handover
Handover Mode:
Scope:
Evidence Level Summary:
Artifacts Generated / Updated:
Critical Gates:
Handover Score:
Status:
Critical Gaps:
Major Risks:
Ownership Changes:
Verification Performed:
Unresolved Items:
Recommended Next Capability:
```

如果交接过程中触发专项 Skill，结果先按各 Skill Return Contract 返回本 Skill，再由本 Skill聚合后返回 Master。

---

# 44. Completion Criteria

只有满足以下条件才算本 Skill 执行完成：

- 已明确 Scope 与新旧 Owner；
- 已完成核心资产盘点；
- 已获得当前 Git / 代码 / 系统状态；
- 已覆盖业务、架构、代码、数据、环境、运行、权限、风险；
- 已记录 Known Issues / Technical Debt / Hidden Knowledge；
- 已形成可执行 Runbook；
- 已给出可重复的验证方法；
- 完整项目已覆盖 Release / Rollback / Incident；
- AI 项目已覆盖 Agent / Workflow / Prompt / Tool / RAG / Eval；
- 已执行一致性审计；
- 已完成或明确安排 KT / Shadow / Reverse Shadow；
- 已进行 Acceptance Gate 判定；
- 已输出明确状态而非模糊的“基本完成”；
- 已说明接手后的 Next Exact Action。

最终判断标准始终只有一个：

> 原负责人退出后，项目是否仍然可以持续演进。
