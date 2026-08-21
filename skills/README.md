# Agent Engineering Skills

> 面向 Codex / Coding Agent / Engineering Agent 的可复用 Agent 工程技能集。目标不是提供几个“万能提示词”，而是把 **引导式需求澄清、从 0 到 1、半路接手、架构审查、故障排查、RAG、Multi-Agent、评测、安全、生产化与性能治理** 固化为可重复执行的工程流程。

仓库整体采用根目录 `LICENSE` 中的 **GNU GPL v3.0**；`skills/` 作为本仓库组成部分遵循同一仓库级许可。

---

# 推荐入口：Agent Engineering Master

正常情况下，用户不需要手动选择十几个 Skill。

只需要把下面这个 Skill 作为主入口：

```text
skills/agent-engineering-master/SKILL.md
```

它会在后续任务中根据当前项目状态动态加载、组合和切换其他专项 Skill：

```text
User Goal
   ↓
agent-engineering-master
   ↓
识别当前阶段 / 风险 / 缺失决策
   ↓
按需加载专项 Skill
   ↓
执行当前阶段
   ↓
更新 Boundary Canvas / Decision Ledger / Shared State
   ↓
重新判断下一阶段
   ↓
切换其他 Skill
   ↓
Implementation / Eval / Security / Production
```

专项 Skill 是能力模块，`agent-engineering-master` 是整个任务生命周期的调度入口。

---

# 一键部署 Skills 提示词

下面这段提示词可以直接复制给 **Codex、Coding Agent 或其他支持 Skills 的工程 Agent**，让它把本仓库的 Agent Engineering Skills 部署到当前开发环境。

> 推荐直接使用完整版本。部署完成后，日常任务只需要使用 `agent-engineering-master`。

```text
请帮我部署 AI-Agent 仓库中的 Agent Engineering Skills。

来源仓库：
https://github.com/kaduoxzero/AI-Agent

目标内容：
仓库根目录下的 skills/ 目录。

部署要求：

1. 先检查当前 Agent / Coding Agent 环境支持的 Skills 机制、Skill 搜索路径、项目级 Skill 目录和用户级 Skill 目录。
2. 如果当前项目已经存在 Skills 目录或已有 Skill 约定，优先遵循现有项目规范，不要擅自创造新的非标准目录。
3. 如果平台同时支持“项目级 Skills”和“全局 / 用户级 Skills”，默认优先安装为项目级 Skills；只有我明确要求全局安装时才安装到用户级目录。
4. 将 AI-Agent 仓库中的完整 skills/ 能力体系部署到目标 Skills 目录，而不是只复制单个 SKILL.md。
5. 必须保留各 Skill 的目录层级、SKILL.md、SKILL-REGISTRY.md 和 templates/，确保 Skill 之间的相对引用关系可用。
6. 将以下 Skill 设置为唯一推荐主入口：
   agent-engineering-master
7. 其他 Skill 不需要我手动调用，它们作为 agent-engineering-master 的内部能力模块，由 Master Skill 在任务执行期间按需加载、组合和切换。
8. 部署时不要覆盖、删除或重命名我已有的无关 Skills。
9. 如果目标位置已经存在同名 AI-Agent Skills：
   - 先比较版本 / 文件差异；
   - 只更新本套 Skills 自己管理的文件；
   - 保留用户自行新增的无关文件；
   - 不要因为更新本 Skill 集而清空整个 Skills 目录。
10. 检查所有 SKILL.md 的 YAML Frontmatter、name、description 和相对路径是否有效。
11. 检查 agent-engineering-master 是否能够发现并引用以下能力：
   - agent-guided-builder
   - agent-greenfield-builder
   - agent-existing-project-modifier
   - agent-architecture-reviewer
   - agent-debugger
   - agent-rag-engineer
   - agent-multi-agent-designer
   - agent-eval-hardening
   - agent-productionizer
   - agent-security-reviewer
   - agent-performance-cost-optimizer
   - agent-project-orchestrator
12. 检查 templates/ 中的 Boundary Canvas、Decision Ledger、Guided Session State、Project Intake、Change Impact、Verification Report 是否完整。
13. 不要修改我的业务代码、Agent 实现、Prompt、依赖或配置；这一步只负责部署 Skills。
14. 不要因为你熟悉某个平台就猜测 Skill 安装路径。优先检查当前环境真实支持的位置和现有约定。
15. 如果当前平台无法原生安装 Skills，则保留原目录结构部署到项目中，并明确告诉我该平台应该如何引用 agent-engineering-master/SKILL.md；不要擅自改写 Skill 内容来适配。

部署完成后执行验证：

A. 能找到 agent-engineering-master/SKILL.md；
B. Master Skill 能读取 SKILL-REGISTRY.md；
C. Master Skill 能按需定位其他专项 Skill；
D. templates/ 可被读取；
E. 原有 Skills 未被破坏；
F. 不存在重复嵌套目录，例如 skills/skills/...；
G. 不存在只复制 Master Skill、却丢失被调用专项 Skill 的情况。

最后只需要给我输出：

- 实际部署位置；
- 部署 / 更新了哪些 Skill；
- 主入口路径；
- 是否通过上述验证；
- 如果当前 Agent 平台存在 Skills 加载限制，说明具体限制。

部署成功后的默认使用规则：
后续涉及 Agent 的设计、开发、修改、调试、RAG、Multi-Agent、Eval、安全、性能优化和生产化任务，优先从 agent-engineering-master 开始，由它自主调度其他 Skill，不需要再次让我选择专项 Skill。
```

## 更新已有 Skills

如果之前已经部署过，可以直接使用下面的简化提示词：

```text
请从 https://github.com/kaduoxzero/AI-Agent 更新我当前环境中已部署的 Agent Engineering Skills。

只同步仓库 skills/ 下属于本套 Skill 系统的内容，不要删除我的其他 Skills，也不要修改业务代码。

更新后确保：
1. agent-engineering-master 仍然是唯一推荐主入口；
2. Master 能动态调用其他专项 Skill；
3. SKILL-REGISTRY.md 与 templates/ 同步更新；
4. 所有 SKILL.md Frontmatter 有效；
5. 不产生 skills/skills/ 这类重复目录；
6. 输出实际更新文件和验证结果。
```

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

`agent-guided-builder` 会让 Agent 像架构师 / 教练一样逐步带用户做关键决策：

- 一次只推进一个主要决策阶段；
- 优先提供 A/B/C/D 选项；
- 明确推荐项；
- 解释推荐原因和 Trade-off；
- 说明选择会新增什么边界、权限、成本和故障面；
- 已确认的信息进入 Decision Ledger，不重复询问；
- 普通实现细节由 Agent 自主决定，不频繁打断用户。

如果用户明确说“按最佳方案直接做，不需要继续问”，Master Skill 应内部完成 Boundary Canvas 和 Decision Ledger，并直接执行；只有无法安全推断且可能造成不可逆高风险后果的决定才暂停。

---

# 目录

```text
skills/
├─ README.md
├─ agent-engineering-master/
│  ├─ SKILL.md
│  └─ SKILL-REGISTRY.md
├─ agent-project-orchestrator/
│  └─ SKILL.md
├─ agent-guided-builder/
│  └─ SKILL.md
├─ agent-greenfield-builder/
│  └─ SKILL.md
├─ agent-existing-project-modifier/
│  └─ SKILL.md
├─ agent-architecture-reviewer/
│  └─ SKILL.md
├─ agent-debugger/
│  └─ SKILL.md
├─ agent-rag-engineer/
│  └─ SKILL.md
├─ agent-multi-agent-designer/
│  └─ SKILL.md
├─ agent-eval-hardening/
│  └─ SKILL.md
├─ agent-productionizer/
│  └─ SKILL.md
├─ agent-security-reviewer/
│  └─ SKILL.md
├─ agent-performance-cost-optimizer/
│  └─ SKILL.md
└─ templates/
   ├─ project-intake.md
   ├─ change-impact.md
   ├─ verification-report.md
   ├─ agent-boundary-canvas.md
   ├─ decision-ledger.md
   └─ guided-session-state.md
```

---

# Master Skill 动态路由

| 当前任务 / 信号 | Master 应调用的 Skill |
|---|---|
| 需求模糊、边界未定 | `agent-guided-builder` |
| 从 0 到 1 | `agent-greenfield-builder` |
| 已有项目新增 / 修改 / 迁移 | `agent-existing-project-modifier` |
| 架构设计或结构问题 | `agent-architecture-reviewer` |
| Tool 不调用、死循环、状态异常 | `agent-debugger` |
| RAG / Retrieval / Embedding / Rerank | `agent-rag-engineer` |
| Supervisor / Handoff / Swarm / 多 Agent | `agent-multi-agent-designer` |
| Regression / Benchmark / 稳定性 | `agent-eval-hardening` |
| Prompt Injection / 越权 / HITL | `agent-security-reviewer` |
| Docker / Queue / Worker / Checkpoint / 上线 | `agent-productionizer` |
| Token / Latency / Concurrency / Cost | `agent-performance-cost-optimizer` |
| 不确定当前应该走哪条路径 | `agent-project-orchestrator` |

路由不是一次性的。

例如：

```text
Greenfield Builder
   ↓
实现中发现需要企业知识库
   ↓
RAG Engineer
   ↓
发现 Tool 有高风险写操作
   ↓
Security Reviewer
   ↓
回到实现
   ↓
Eval Hardening
   ↓
发现成本超标
   ↓
Performance Optimizer
   ↓
Productionizer
```

用户不需要重新指定 Skill。

---

# Agent Boundary Canvas

Guided Builder 固定检查 13 类边界：

```text
1. Goal Boundary
2. User Boundary
3. Input Boundary
4. Output Boundary
5. Autonomy Boundary
6. Knowledge Boundary
7. Tool Boundary
8. Side-Effect / Permission Boundary
9. State / Session / Memory / Checkpoint Boundary
10. Multi-Agent Boundary
11. Time / Token / Cost Boundary
12. Safety / HITL Boundary
13. Failure / Recovery Boundary
```

每类边界应被标记为：

```text
Required
Not Required
Deferred
Unknown
```

目的不是把系统做复杂，而是避免关键工程边界因为“没有想到”而缺失。

---

# Guided Workshop 阶段

```text
Stage 0   Problem Framing
Stage 1   Success / Failure / Acceptance
Stage 2   Need Agent or Not
Stage 3   Autonomy Boundary
Stage 4   Knowledge Boundary
Stage 5   Tool / Side-Effect Boundary
Stage 6   State / Memory / Checkpoint
Stage 7   Multi-Agent Boundary
Stage 8   Runtime / Reliability
Stage 9   Identity / Security / HITL
Stage 10  Evaluation
Stage 11  Observability / Operations
Stage 12  Architecture Freeze
Stage 13  Incremental Build
```

禁止一次性向用户抛出大量问题。每次只解决当前最重要的 1~3 个决策。

---

# 统一工程原则

所有 Skill 都遵守以下规则：

1. **先理解，再修改**：已有项目先建立 Baseline。
2. **边界先于框架**：先定义职责、自治、权限、数据和失败边界，再决定 LangGraph / SDK。
3. **确定性优先**：普通代码、规则、状态机能解决的问题不交给 LLM。
4. **Workflow 优先于自治**：固定流程优先 Workflow。
5. **Single Agent 优先于 Multi-Agent**：只有存在真实职责、权限、Context、并发或能力边界才拆 Agent。
6. **契约优先**：模块之间优先 Typed Contract / Schema / Artifact。
7. **最小权限**：Tool 默认拒绝，显式 Allowlist / Scope 授权。
8. **有界执行**：限制 Step、Model Call、Tool Call、Token、Cost、Retry 与 Time。
9. **可恢复**：长任务需要 Task State、Checkpoint、Resume、Idempotency 与 Cancellation。
10. **可观测**：关键路径需要 Trace、Event、Metric、Error Category。
11. **评测先于上线**：必须有 Regression / Eval Gate。
12. **安全失败**：越权、不确定或预算超限时 Fail Closed 或进入 HITL。
13. **不制造无关改动**：已有项目不顺手重构无关代码。
14. **不重复询问**：已经由用户、代码、配置或测试解决的问题不得重复问。

---

# Templates

- `templates/project-intake.md`：项目现状、目标、约束与风险。
- `templates/change-impact.md`：修改前影响面分析。
- `templates/verification-report.md`：测试、Eval、安全和残余风险记录。
- `templates/agent-boundary-canvas.md`：系统化检查职责、自治、知识、Tool、权限、State、Memory、Budget、安全和失败边界。
- `templates/decision-ledger.md`：持续记录重要架构选择及 Trade-off。
- `templates/guided-session-state.md`：多轮引导中保存阶段进度、已解决信息和下一项关键决策。

---

# 核心思想

> 一个专业 Agent Engineering Skill 的价值，不是告诉模型“你是资深工程师”，而是让它知道 **现在应该问什么、哪些不该问、什么时候调用哪一个专项 Skill、怎么考虑边界、什么时候开始编码、如何验证，以及失败后如何恢复**。
