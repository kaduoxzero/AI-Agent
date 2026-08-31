---
name: agent-enterprise-handover
version: 1.0.0
description: Enterprise-grade project and engineering handover orchestrator. Use for ownership transfer, developer replacement, leave/rotation handoff, module handover, Agent-to-Agent context transfer, project takeover, or auditing whether a project can continue without the original owner. Produces evidence-backed business, architecture, code, data, runtime, operations, permission, risk, runbook, knowledge-transfer and acceptance artifacts instead of a simple status summary.
---

# Agent Enterprise Handover

## Objective

把“写一份交接文档”升级为一次完整的 **Ownership Transfer（所有权转移）+ Knowledge Transfer（知识转移）+ Asset Transfer（资产转移）+ Operability Transfer（可运营能力转移）**。

最终目标不是“文档看起来完整”，而是：

> 假设原负责人从交接完成后立即无法联系，接手人仍然能够独立理解项目、启动系统、修改代码、验证功能、发布版本、回滚、排障、恢复服务并继续推进后续工作。

本 Skill 是交接流程的 Master / Aggregator，负责发现、编排、证据聚合、缺口审计、验收和最终交接结论；它不应重复实现仓库中已有专项 Skill 的专业能力。

---

## 1. Trigger & Scope

出现以下任一意图时使用：

- 项目整体交接、离职交接、调岗/轮岗交接；
- 某模块、服务、Agent、RAG、数据库、前端或后端移交；
- 开发做到一半换人继续；
- 接手别人项目，需要判断资料是否完整；
- 生成“新人可以直接接手”的交接包；
- 把口头知识、聊天记录、个人经验沉淀成 Runbook；
- 审查现有交接文档是否达到可接手标准；
- Agent-to-Agent / Coding Agent-to-Agent 上下文交接；
- 阶段结束时形成可追踪的项目快照。

如果只是周报、工作总结、版本说明，不使用本 Skill。

---

## 2. Enterprise Handover Definition

完整交接必须同时覆盖：

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

任何一个维度缺失，都不能仅因为“有文档”判定交接完成。

---

## 3. Evidence Classification

所有关键结论必须标记证据等级：

| Level | 标记 | 含义 |
|---|---|---|
| A | `VERIFIED` | 通过代码、Git、配置、运行、测试、日志、数据库或监控实际验证 |
| B | `DOCUMENTED` | 来自正式文档，但尚未实际验证 |
| C | `REPORTED` | 来自交接人/用户口述 |
| D | `INFERRED` | 根据代码或上下文合理推断 |
| E | `UNKNOWN` | 当前无法确认 |

强制规则：

1. `INFERRED` 不能写成已确认事实；
2. `REPORTED` 的高风险信息尽量升级为 `VERIFIED`；
3. 启动、发布、回滚、备份恢复、关键权限、生产配置等 Critical Item 不允许只依赖 `REPORTED`；
4. 无法确认时明确写 `UNKNOWN / 待确认`，禁止编造。

---

## 4. Handover Modes

### H1 — Full Project Handover

完整项目或 Owner 更换，启用全部交接域。

### H2 — Module Handover

只交接某模块/服务/子系统，同时描述上下游依赖和系统边界。

### H3 — In-Progress Development Handover

重点：当前分支、修改文件、完成状态、失败测试、临时实现、Next Exact Action。

### H4 — Operations Handover

重点：环境、服务、端口、中间件、发布、回滚、日志、监控、告警、备份、事故处理。

### H5 — AI / Agent Handover

重点：Agent、Workflow、State、Router、Prompt、Tool、Skill、Memory、RAG、Model、Evaluation、Guardrail、Tracing、Cost。

### H6 — Product / Business Handover

重点：业务背景、业务规则、目标用户、产品状态、Roadmap、指标、Stakeholder、历史决策。

### H7 — Temporary Handover

请假、短期代管等，生成精简 Handover Card。

### H8 — Takeover Audit

从接手人视角寻找缺口、SPOF、权限问题和无法继续工作的地方。

### H9 — Agent-to-Agent Transfer

使用 Context Transfer Contract，保证下一 Agent 不重新猜测任务状态。

---

## 5. Orchestration Contract

本 Skill 作为交接聚合器，优先复用已有能力：

| 交接域 | 推荐专项 Skill |
|---|---|
| 范围/交接要求不清 | `agent-grill-me` |
| 架构边界 | `agent-architecture-reviewer` |
| 代码现状/影响面 | `agent-existing-project-modifier` |
| 故障复现/异常轨迹 | `agent-debugger` |
| RAG / Knowledge Base | `agent-rag-engineer` |
| Multi-Agent / Handoff | `agent-multi-agent-designer` |
| 测试/回归/证据 | `agent-eval-hardening` |
| 权限/Secret/安全边界 | `agent-security-reviewer` |
| Runbook/SRE/发布 | `agent-productionizer` |
| 性能/容量/成本 | `agent-performance-cost-optimizer` |

遵守 Master 动态加载规则：

- Primary Skill = 1；
- Supporting Skills <= 2；
- 不一次加载全部 Skill；
- 按交接阶段顺序调用，专项完成后返回本 Skill 聚合。

专项 Skill 不可用时，本 Skill 使用自身检查清单完成最低限度审计，不能直接跳过。

---

## 6. Lifecycle

```text
0. Scope & Ownership Freeze
        ↓
1. Asset Inventory
        ↓
2. Repository & System Discovery
        ↓
3. Business / Architecture / Code / Data Capture
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

不能因为文档已生成就跳过 7~9。

---

# 7. Phase 0 — Scope & Ownership Freeze

建立 Handover Charter：

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

如果用户已提供，不重复询问；如果能从仓库、项目状态、Git、配置或文档获得，优先自行发现。

### Scope Matrix

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

# 8. Phase 1 — Asset Inventory

## Code Assets

检查 Repository / Monorepo / Submodule、默认/Release/Hotfix 分支、Tag/Release、Private Package、Script、Migration、Seed、Git LFS。

## Documentation Assets

检查 README、PRD、Architecture、ADR、API、Database、Runbook、Test、Incident/Postmortem、Security、Roadmap、Meeting Notes、Recording。

每份文档标记：`CURRENT / OUTDATED / PARTIAL / UNKNOWN`。

## Runtime Assets

检查 Server / VM / Container / Kubernetes、DB、Redis、MQ、Elasticsearch、Vector DB、Config Center、Object Storage、Domain、DNS、Certificate、CI/CD、Monitoring、Logging、Tracing。

## External Assets

检查 OAuth、微信生态、邮件/短信、Cloud、LLM/Embedding Provider、支付/地图/外部 API、Vendor。

## Access Assets

只记录：

```text
Resource
Required Role
Permission Level
Apply Method
Owner
Status
```

禁止保存真实密码、API Key、Token、Private Key。

---

# 9. Phase 2 — Repository & System Discovery

如果可以访问代码，不允许只根据 README 交接。

最低顺序：

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

## Git Snapshot

记录：

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

强制检查未提交修改、未 Push Commit、未合并 Branch、Stash、冲突、临时文件、本地绝对路径、明文 Secret、个人电脑独有脚本。

## Repository Map

只保留高价值目录，例如：

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

不机械输出 `node_modules`、`target`、`dist`、`.idea`、`__pycache__`。

## Critical Entrypoints

定位 Application、Controller/API、Core Service、Repository/DAO、Job/Scheduler、Consumer/Producer、Workflow/Agent、Config、Test Entrypoint。

---

# 10. Business & Product Handover

必须回答：

- 项目为什么存在；
- 给谁使用；
- 核心目标；
- 核心业务流程；
- 哪些规则不在代码/PRD；
- 哪些异常流程需要人工介入；
- 哪些功能实际在使用；
- 哪些功能已经停用或名存实亡。

建立 Business Glossary：

| Term | 中文/业务名 | Definition | Source |
|---|---|---|---|

核心流程至少区分：

```text
Normal Flow
Exception Flow
Compensation Flow
Manual Flow
```

产品状态使用：`DONE / PARTIAL / IN_PROGRESS / BLOCKED / TODO / VERIFY / DEFERRED / CANCELLED`。

---

# 11. Architecture & Decision Handover

必须说明系统边界、组件关系、同步调用、异步链路、数据流、外部依赖、单点、核心状态、缓存和队列。

关键设计必须记录 Why，不只写 What。

ADR：

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

优先记录：为什么使用当前 DB/Redis/MQ，为什么拆或不拆微服务，为什么采用当前 Agent 架构/模型，为什么某些兼容代码不能轻易删除。

---

# 12. Code Handover

每个核心模块至少说明：

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

主动识别 Code Hotspot：高频修改、高复杂度、高事故、高耦合、缺测试、历史兼容区域。

以下默认 Danger Zone：Authentication、Authorization、Payment、Inventory、Transaction、Distributed Lock、Public API、Database Migration、Encryption、Permission、Model Guardrail、Critical Workflow State。

扫描：`TODO / FIXME / HACK / TEMP / Deprecated / Hard-coded Secret / Magic Number / Empty Catch / Disabled Validation / Mock / Bypass / Local Path`。

发现项进入 Technical Debt Register，不隐藏。

---

# 13. Data & Database Handover

记录：

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

关键表：

| Table | Purpose | Critical Fields | Relationships | Risk |
|---|---|---|---|---|

数据分类至少区分：核心业务数据、可重建数据、缓存数据、审计日志、PII/敏感数据、临时数据、不可恢复数据。

Data Lifecycle：

```text
Create → Read → Update → Archive → Delete → Backup → Restore
```

Migration 必须确认升级方式、向后兼容、生产执行顺序、失败处理、回滚能力。

---

# 14. API & Contract Handover

| API | Method | Caller | Auth | Status | Owner |
|---|---|---|---|---|---|

重要接口说明 Request、Response、Error Code、Auth、Idempotency、Timeout、Retry、Rate Limit、Compatibility。

特别标记 Public、Internal、Deprecated、Experimental、Mock、Temporary、Callback、Webhook、Third-party。

---

# 15. Environment / Build / Startup

严格区分 Local、Development、Test、Staging/Pre-production、Production。

Environment Matrix：

| Item | Local | Test | Staging | Prod |
|---|---|---|---|---|

记录 OS、JDK、Maven/Gradle、Node/npm/pnpm、Python/Conda、Docker、必要 IDE 版本。

Secret 只记录：

```text
Secret Name
Secret Store / Location
Access Method
Owner
Rotation Policy
```

Build：

```text
Build Command
Artifact
Artifact Location
Dependency Source
Private Registry
Success Signal
```

Startup Runbook：

```text
Preconditions
Dependency Order
Commands
Ports
Health Check
Success Signal
Common Failure
```

Verification：

```text
Verification ID:
Precondition:
Command / Action:
Expected:
Actual:
Evidence:
Status:
```

禁止仅写“项目可以正常运行”。

---

# 16. Testing Handover

盘点 Unit、Integration、API、E2E、Regression、Smoke、Performance、Security、AI Eval。

Baseline：

```text
Total Tests
Passed
Failed
Skipped
Coverage
Known Flaky Tests
Known Untested Critical Paths
```

没有测试必须明确列为缺口，不能写“待后续完善”后仍判 Full Handover。

---

# 17. Release & Rollback Handover

完整项目/运维交接必须有 Release Runbook：

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

Rollback 必须回答：谁决定、触发条件、代码/配置如何回滚、数据库如何处理、数据不兼容怎么办、回滚后如何验证。

核心系统能发布但没有明确回滚时，至少标记 P0/P1 Operational Risk。

---

# 18. Observability & Incident Handover

Logs：平台/路径、关键日志、Trace ID/Request ID、检索方法、核心错误识别。

Metrics 根据项目选择 QPS、P50/P95/P99、Error Rate、CPU/Memory、DB Connections、Queue Lag、LLM Latency、Token Usage、Tool Success Rate。

Alert：

```text
Alert:
Meaning:
Severity:
First Action:
Owner:
Escalation:
```

重大事故：

| Date | Incident | Impact | Root Cause | Fix | Lesson |
|---|---|---|---|---|---|

高频故障 Runbook：

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

# 19. Backup / Recovery / Continuity

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

有备份但未验证 Restore，不得把“可恢复”写为 VERIFIED。

---

# 20. Security & Permission Handover

检查 Authentication、Authorization/RBAC、Secrets、Certificate、Firewall/Whitelist、Sensitive Data、Audit Log、Dependency Vulnerability、Privileged Tools、Production Access。

Permission Matrix：

| Resource | Role | Permission | Apply Method | Owner | Status |
|---|---|---|---|---|---|

禁止把凭据写进交接文档。

---

# 21. Third-party / Vendor Handover

| Service | Usage | Owner | SLA | Expiry | Fallback | Risk |
|---|---|---|---|---|---|---|

重点识别：单管理员账号、个人 API Key、合同到期、无替代 Provider、第三方回调仅原负责人掌握。

---

# 22. AI / Agent Extension

检测到 AI 项目时强制启用。

## Agent Inventory

| Agent | Responsibility | Input | Output | Tools | Boundary |
|---|---|---|---|---|---|

## Workflow

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

## State

区分 Global State、Workflow State、Agent State、Session State、Persistent State、Checkpoint。

## Prompt

记录 Prompt Type、Location、Version、Dynamic Variables、Owner、Fallback、Change Risk。

## Model

记录 Provider、Model、Reasoning Level、Sampling、Max Tokens、Timeout、Retry、Fallback、Selection Rationale、Cost/Latency Baseline。

## Tool / MCP

每个 Tool 说明 Purpose、Input、Output、Permission、Side Effect、Failure Strategy、HITL Requirement。MCP 增加 Server、Transport、Auth、Exposed Tools。

## Memory

区分 Conversation / Session / Long-term / User / Business Memory，并明确 Persistence 和删除策略。

## RAG

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

## Evaluation

记录 Dataset、Golden Cases、Metrics、Baseline、Latest Result、Known Failure Cases、Regression Gate。

Failure Case 建议保留 Input、Wrong Output、Expected、Root Cause、Workaround/Fix。

---

# 23. Ownership / RACI / Escalation

RACI：R=Responsible，A=Accountable，C=Consulted，I=Informed。

| Activity | R | A | C | I |
|---|---|---|---|---|
| Requirement | | | | |
| Code Change | | | | |
| Release | | | | |
| DB Migration | | | | |
| Production Incident | | | | |
| Security Incident | | | | |

记录 Escalation Path：

```text
L1 → L2 → Technical Owner → Business Owner / Management
```

必须说明什么问题升级到谁，而不是只列联系人。

---

# 24. Hidden Knowledge / SPOF / Bus Factor

主动寻找：

```text
只有某个人知道的命令
个人电脑上的脚本
聊天记录中的业务规则
未提交 SQL
个人账号下的第三方资源
手工发布步骤
特殊缓存清理
本地 Mock / 临时绕过
没有文档的历史兼容规则
“这个只能问 XXX”
```

这些进入 Tribal Knowledge Register。

某模块知识/权限只掌握在一人手里，标记 `Knowledge SPOF / Bus Factor = 1`。

---

# 25. TODO / Issue / Debt / Risk Registers

TODO 必须包含：

```text
TODO-ID
Task
Context
Priority
Location
Dependency
Recommended Approach
Acceptance Criteria
Owner
```

Known Issue：

```text
ISSUE-ID
Severity
Impact
Trigger
Root Cause
Workaround
Permanent Fix
Verification
```

Technical Debt：

```text
DEBT-ID
Description
Reason
Impact
Risk
Suggested Solution
Priority
```

Risk：

```text
RISK-ID
Category
Probability
Impact
Level
Trigger
Mitigation
Contingency
Owner
```

Priority：P0=生产/安全/数据损坏/核心不可用；P1=核心功能或可运营性严重影响；P2=重要但有绕行；P3=普通优化。

---

# 26. Knowledge Transfer / Recording

复杂项目建议：

```text
Session 1 — Business & Product
Session 2 — Architecture & Code
Session 3 — Data & External Dependencies
Session 4 — Runtime / Release / Incident
Session 5 — AI / Agent（如适用）
Session 6 — Open Questions & Acceptance
```

组织允许录屏时建立 Recording Index：

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

不能只有长视频没有时间索引。

---

# 27. Shadow & Reverse Shadow

Shadow：原负责人操作，接手人观察。

Reverse Shadow：接手人操作，原负责人观察。

至少验证：

```text
Clone / Checkout
Build
Run
核心 Smoke Test
修改一个小功能
执行测试
定位一个已知问题
查询日志/监控
```

重要系统增加 Release、Rollback、Backup Restore、Incident Drill。

关键 Reverse Shadow 无法完成时，交接不得标记 COMPLETE。

---

# 28. Day 0 / 1 / 3 / 7 Acceptance

## Day 0 — Access Ready

Repository、文档、Dev/Test、DB、Monitoring、必要 Third-party 权限到位。

## Day 1 — Runtime Ready

```text
Clone → Build → Run → Health Check → Core Smoke Test → Read Logs
```

## Day 3 — Development Ready

能解释架构、定位核心代码、完成小修改、运行测试、定位普通 Bug。

## Day 7 — Ownership Ready

能独立常规开发、常规发布、普通事故处理，并知道高风险问题升级路径。

## Day 30 — Dependency Review

长期项目检查是否仍依赖原负责人，并补充新发现的 Tribal Knowledge。

---

# 29. Acceptance Gates

必须经过：

- Gate A — Scope Ready；
- Gate B — Asset Ready；
- Gate C — Knowledge Ready；
- Gate D — Runtime Ready；
- Gate E — Development Ready；
- Gate F — Operations Ready；
- Gate G — Security & Permission Ready；
- Gate H — Ownership Ready；
- Gate I — Reverse Shadow Passed。

---

# 30. Critical Blocker Override

出现以下任一项，不允许判定 COMPLETE：

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
关键数据无恢复策略且业务要求可恢复
Reverse Shadow 关键项失败
```

---

# 31. Handover Score — 200

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

```text
180–200  Level A — Ready
160–179  Level B — Ready with Minor Gaps
130–159  Level C — Conditional Handover
100–129  Level D — High Dependency
<100     Level E — Handover Failed
```

Critical Blocker Override 高于总分。

---

# 32. Documentation Drift / Security Audit

必须检查：

```text
README vs Code
Architecture vs Actual Dependencies
API Doc vs Controller / Schema
Database Doc vs Migration
Config Doc vs Actual Config
Runbook vs Actual Command
Test Doc vs Current Test Suite
TODO vs Git / Issue State
```

同时扫描 `.env`、application config、Docker Compose、Shell/PowerShell、README、CI Config、Prompt/Tool Config 中的 Secret、个人账号、本地绝对路径、localhost-only dependency、个人目录模型/数据、认证绕过和临时白名单。

发现 Secret 时不要复制，只报告暴露位置并要求迁移/轮换。

---

# 33. Project Artifacts

默认在当前业务项目创建：

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
├─ 12-AI-Agent专项.md
├─ 13-已知问题与技术债.md
├─ 14-风险与SPOF.md
├─ 15-RACI与升级路径.md
├─ 16-KT与录屏索引.md
├─ 17-交接验收.md
└─ 18-最终交接报告.md
```

小型项目可以合并；无 AI 时不创建 AI 专项空文件。

项目实例正文默认简体中文；技术标识符保留英文；`skills/templates/` 永远只读。

本 Skill 可读取：

```text
../templates/handover-master.md
../templates/handover-evidence-register.md
../templates/handover-runbook.md
../templates/handover-risk-register.md
../templates/handover-acceptance.md
```

---

# 34. Temporary Handover Contract

临时交接允许压缩：

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

# 35. Agent-to-Agent Context Transfer

必须输出：

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

禁止“继续完成 / 继续优化 / 按之前方案继续”。Next Exact Action 应具体到文件、函数、测试或命令。

---

# 36. Incremental Interview Rule

无法访问项目资料时，按：

```text
Scope → Business → Architecture → Code/Data → Environment → Operations → Risk → Acceptance
```

逐阶段获取信息，不一次抛几十个问题。

处理优先级：

```text
已有信息
→ 仓库可发现
→ 项目状态可读取
→ 安全默认值
→ Agent 合理建议
→ 用户关键决策
```

已回答的信息不重复询问。

---

# 37. Final Audit Simulation

宣布完成前模拟：

1. 原负责人立即无法联系，我能启动项目吗？
2. 核心 API 500，我知道从哪里排查吗？
3. 数据库连接失败，我知道配置、Owner、影响范围吗？
4. 今天需要发布，我能独立完成吗？
5. 发布失败，我能安全回滚吗？
6. 核心数据异常，我知道备份/恢复路径吗？
7. 第三方失效，我知道联系人和替代方案吗？
8. 业务问“为什么这样设计”，我能找到决策依据吗？
9. 接手人是否真正操作过，而不是只看过文档？
10. 是否仍有“只能问原负责人”的关键知识？

核心问题任一答案为“否”，必须进入 Critical Gap 或 Risk。

---

# 38. Final Status

只允许：

- `COMPLETE`：关键 Gate 全通过、无 Critical Blocker、Reverse Shadow 通过；
- `CONDITIONAL`：可以接手，但存在明确非关键缺口；
- `INCOMPLETE`：存在关键知识、资产、运行或权限缺口；
- `BLOCKED`：因权限、资产、人员、环境或数据无法继续交接。

Final Handover Report 至少包含：

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

第一项动作不能写“熟悉项目”，应具体到 Checkout、启动依赖、Health Check、Smoke Test 等操作。

---

## Report Back to Master

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
Next Exact Action:
```

交接过程中触发专项 Skill 时，专项结果先按其 Return Contract 返回本 Skill，再由本 Skill 聚合后返回 Master。

---

## Completion Criteria

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
- 已输出明确状态，而不是模糊的“基本完成”；
- 已说明接手后的 Next Exact Action。

最终判断标准始终只有一个：

> 原负责人退出后，项目是否仍然可以持续演进。
