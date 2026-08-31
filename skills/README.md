# Agent Engineering Skills

> 面向 Codex / Coding Agent / Engineering Agent 的可复用 Agent 工程技能集。目标不是提供几个“万能提示词”，而是把 **引导式需求澄清、从 0 到 1、半路接手、架构审查、故障排查、企业级项目交接、RAG、Multi-Agent、评测、安全、生产化与性能治理** 固化为可重复执行的工程流程。

仓库整体采用根目录 `LICENSE` 中的 **GNU GPL v3.0**；`skills/` 作为本仓库组成部分遵循同一仓库级许可。

---

# 推荐入口：Agent Engineering Master

正常情况下，用户不需要手动选择十几个 Skill，只需要把下面这个 Skill 作为主入口：

```text
skills/agent-engineering-master/SKILL.md
```

它会在后续任务中根据当前项目状态动态加载、组合和切换其他专项 Skill：

```text
User Goal
   ↓
agent-engineering-master
   ↓
Runtime Bootstrap（Runtime + 项目状态引导）
   ↓
识别当前阶段 / 风险 / 缺失决策
   ↓
按需加载专项 Skill
   ↓
执行 + 验证
   ↓
更新当前项目 .agent-engineering/
   ↓
重新路由，直到完成
```

专项 Skill 是能力模块；`agent-engineering-master` 是整个任务生命周期的调度入口。

## 权威文件（Single Source of Truth）

| 内容 | 唯一权威位置 |
|---|---|
| 机器可读注册表（status / category） | `../runtime/skill-registry.yaml` |
| Skill 能力语义、动态路由、切换契约 | `agent-engineering-master/SKILL-REGISTRY.md` |
| 项目状态隔离、模板只读、多项目规则 | `agent-engineering-master/PROJECT-STATE-POLICY.md` |
| 15 类边界画布结构 | `templates/agent-boundary-canvas.md` |
| 统一复杂度阶梯 | `agent-greenfield-builder/SKILL.md`（其他文件引用同一标准块） |
| 企业级交接执行协议 | `agent-enterprise-handover/SKILL.md` |
| 部署 / 更新提示词 | `DEPLOY.md` |

每个 Skill 目录包含 `SKILL.md`（执行协议）与 `skill.yaml`（机器可读 manifest，version 与 frontmatter 保持一致）。

---

# Guided Agent Engineering

这套 Skills 不要求 Agent “收到需求就直接写代码”。

对于关键边界还没有形成的项目，推荐流程：

```text
agent-engineering-master
  ↓
agent-guided-builder
  ↓
Boundary Canvas + Decision Ledger
  ↓
Architecture Freeze
  ↓
agent-greenfield-builder / agent-existing-project-modifier
  ↓
专项 Skill
  ↓
Implementation + Eval + Production
```

`agent-guided-builder` 会让 Agent 像架构师 / 教练一样逐步带用户做关键决策：一次只推进一个主要决策阶段；优先提供 A/B/C/D 选项；明确推荐项并解释 Trade-off 与 Boundary Impact；已确认的信息进入 Decision Ledger，不重复询问。

如果用户明确说“按最佳方案直接做”，Master 会内部完成 Boundary Canvas 和 Decision Ledger 并直接执行；只有无法安全推断且可能造成不可逆高风险后果的决定才暂停。

---

# Enterprise Handover

项目交接不等于生成一篇 Markdown 总结。

当用户提出“交接项目、离职交接、模块移交、接手别人项目、检查交接是否完整、Agent-to-Agent handover”等需求时，Master 会路由到：

```text
skills/agent-enterprise-handover/SKILL.md
```

该 Skill 将交接拆成四种真实转移：

```text
Knowledge Transfer       知识转移
Asset Transfer           资产转移
Responsibility Transfer  责任转移
Operability Transfer     可运营能力转移
```

默认流程：

```text
Scope Freeze
   ↓
Asset Inventory
   ↓
Repository / System Discovery
   ↓
Business / Architecture / Code / Data Capture
   ↓
Runtime / Release / Rollback / Incident
   ↓
Risk / Technical Debt / Hidden Knowledge / SPOF
   ↓
Knowledge Transfer + Shadow
   ↓
Reverse Shadow
   ↓
Acceptance Gates
   ↓
Final Handover Report
```

关键结论按照 `VERIFIED / DOCUMENTED / REPORTED / INFERRED / UNKNOWN` 分级，避免把口述或推测当成已验证事实。

完整项目不能仅凭“文档已经发给接手人”判定完成。核心仓库、启动能力、生产 Owner、发布/回滚、权限或 Reverse Shadow 任一关键 Gate 失败时，必须判定为 `CONDITIONAL / INCOMPLETE / BLOCKED`。

交接实例默认写入业务项目：

```text
<project>/.agent-engineering/交接/
```

`skills/templates/` 仅提供只读结构模板，不保存任何具体项目的交接数据。

---

# 目录

```text
skills/
├─ README.md                         本文件
├─ DEPLOY.md                         一键部署 / 更新提示词
├─ SKILL-MANIFEST-TEMPLATE.yaml      Skill 清单模板
├─ agent-engineering-master/         唯一推荐主入口（Runtime 编排）
│  ├─ SKILL.md
│  ├─ SKILL-REGISTRY.md              能力注册表（SSoT）
│  ├─ PROJECT-STATE-POLICY.md        项目状态策略（SSoT）
│  └─ resources/                     Runtime v2 与命名规范参考
├─ agent-project-orchestrator/       任务路由与编排判断
├─ agent-grill-me/                   需求澄清前置门（最少高价值问题 + 边界探索）
├─ agent-guided-builder/             引导式边界设计工作坊
├─ agent-greenfield-builder/         从 0 到 1 构建
├─ agent-existing-project-modifier/  已有项目安全修改
├─ agent-enterprise-handover/        企业级项目交接 / 接手 / Ownership Transfer / 验收
├─ agent-architecture-reviewer/      架构审查
├─ agent-debugger/                   故障排查
├─ agent-rag-engineer/               RAG / Agentic RAG 工程
├─ agent-multi-agent-designer/       Multi-Agent 架构设计
├─ agent-eval-hardening/             评测 / 回归 / 发布门禁
├─ agent-productionizer/             生产化改造
├─ agent-security-reviewer/          安全审查与加固
├─ agent-performance-cost-optimizer/ 性能与成本优化
└─ templates/                        共享只读模板库（实例化到业务项目）
   ├─ project-state.yaml
   ├─ agent-boundary-canvas.md
   ├─ decision-ledger.md
   ├─ current-session.md
   ├─ project-intake.md
   ├─ architecture-summary.md
   ├─ change-impact.md
   ├─ verification-report.md
   ├─ handover-master.md
   ├─ handover-evidence-register.md
   ├─ handover-runbook.md
   ├─ handover-risk-register.md
   └─ handover-acceptance.md
```

动态路由表、触发信号与运行时 Skill 切换示例见 `agent-engineering-master/SKILL-REGISTRY.md`，本文件不再维护副本。

---

# 项目状态模型

```text
skills/templates/                  共享只读模板
        ↓ instantiate / copy
<project>/.agent-engineering/      每个业务项目独占状态，可更新
```

完整规则见 `agent-engineering-master/PROJECT-STATE-POLICY.md`。核心原则：

> Template is immutable. Project State is project-scoped. Session State is task-scoped. Cross-project state sharing is opt-in, never implicit.

交接专项实例默认使用：

```text
<project>/.agent-engineering/交接/
```

但交接过程中发现的长期有效边界、架构决策和验证结论仍需同步回项目长期状态，而不是只留在交接包里。

---

# 核心思想

> 一个专业 Agent Engineering Skill 的价值，不是告诉模型“你是资深工程师”，而是让它知道 **现在应该问什么、哪些不该问、什么时候调用哪一个专项 Skill、怎么考虑边界、什么时候开始编码、如何验证，以及失败后如何恢复**。

对于交接场景，再增加一个标准：

> 不是“资料有没有给出去”，而是“原负责人退出后，新 Owner 是否仍能独立让项目继续演进”。
