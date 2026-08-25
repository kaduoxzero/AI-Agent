# Agent Engineering Skills

> 面向 Codex / Coding Agent / Engineering Agent 的可复用 Agent 工程技能集。目标不是提供几个“万能提示词”，而是把 **引导式需求澄清、从 0 到 1、半路接手、架构审查、故障排查、RAG、Multi-Agent、评测、安全、生产化与性能治理** 固化为可重复执行的工程流程。

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
Project State Bootstrap（读取项目状态策略与注册表）
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
| Skill 能力注册、动态路由、切换契约 | `agent-engineering-master/SKILL-REGISTRY.md` |
| 项目状态隔离、模板只读、多项目规则 | `agent-engineering-master/PROJECT-STATE-POLICY.md` |
| 15 类边界画布结构 | `templates/agent-boundary-canvas.md` |
| 统一复杂度阶梯 | `agent-greenfield-builder/SKILL.md`（其他文件引用同一标准块） |
| 部署 / 更新提示词 | `DEPLOY.md` |

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

# 目录

```text
skills/
├─ README.md                        本文件
├─ DEPLOY.md                        一键部署 / 更新提示词
├─ agent-engineering-master/        唯一推荐主入口
│  ├─ SKILL.md
│  ├─ SKILL-REGISTRY.md             能力注册表（SSoT）
│  └─ PROJECT-STATE-POLICY.md       项目状态策略（SSoT）
├─ agent-project-orchestrator/      任务路由与编排判断
├─ agent-guided-builder/            引导式边界设计工作坊
├─ agent-greenfield-builder/        从 0 到 1 构建
├─ agent-existing-project-modifier/ 已有项目安全修改
├─ agent-architecture-reviewer/     架构审查
├─ agent-debugger/                  故障排查
├─ agent-rag-engineer/              RAG / Agentic RAG 工程
├─ agent-multi-agent-designer/      Multi-Agent 架构设计
├─ agent-eval-hardening/            评测 / 回归 / 发布门禁
├─ agent-productionizer/            生产化改造
├─ agent-security-reviewer/         安全审查与加固
├─ agent-performance-cost-optimizer/ 性能与成本优化
└─ templates/                       共享只读模板库（实例化到 <project>/.agent-engineering/）
   ├─ project-state.yaml
   ├─ agent-boundary-canvas.md
   ├─ decision-ledger.md
   ├─ current-session.md
   ├─ project-intake.md
   ├─ architecture-summary.md
   ├─ change-impact.md
   └─ verification-report.md
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

---

# 核心思想

> 一个专业 Agent Engineering Skill 的价值，不是告诉模型“你是资深工程师”，而是让它知道 **现在应该问什么、哪些不该问、什么时候调用哪一个专项 Skill、怎么考虑边界、什么时候开始编码、如何验证，以及失败后如何恢复**。
