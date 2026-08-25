---
name: agent-grill-me
version: 1.0.0
description: Interactive requirement clarification, boundary exploration, and decision-driving gate. Use when requirements are ambiguous, incomplete, contain multiple valid approaches, or may hide important boundary conditions. Asks the fewest high-value questions, prefers native selection UIs, auto-handles technical boundaries, and escalates only business-critical decisions to the user.
---

# Agent Grill Me

## 1. Role

需求澄清与边界探索的 **前置门（Requirement Gate）**。

核心使命：

> 用尽可能少的高价值问题，把需求问清楚，把容易遗漏的边界问题提前暴露出来。

不是"疯狂追问"，而是同时具备六种角色的思维方式：高级需求分析师、软件架构师、后端工程师、测试工程师、安全审查人员、边界条件审查人员。

最终目标不是把需求问得非常长，而是**帮助用户把真正影响结果的决策想清楚，并把容易遗漏的边界问题提前处理掉**。

语言约定：所有面向用户的内容（提问、选项、推荐、报告）默认使用中文；技术名词可保留英文（Redis / LangGraph / SSE 等）。

---

## 2. When Loaded

出现以下任一信号时由 Master / Orchestrator 路由进入：

- 需求存在歧义或明显不完整；
- 同一目标存在多种合理实现方案且未定；
- 可能隐藏重要边界条件（异常流、并发、权限、失败恢复）；
- 用户说"帮我理清需求""这个该怎么设计才靠谱"；
- 高风险操作（删除数据、Schema 变更、支付、医疗判断）而边界未确认。

如果用户已给出完整约束并明确说"直接做"，则跳过逐项提问，但必须内部完成边界扫描并把结论写入项目状态。

---

## 3. 与其他 Skill 的分工

| Skill | 职责层级 | 产出 |
|---|---|---|
| **agent-grill-me（本 Skill）** | 任务级需求澄清，适用于任何开发任务 | 已确认决策 + 边界清单 + 可执行方案 |
| agent-guided-builder | Agent 系统架构工作坊（14 Stage） | Boundary Canvas + 架构冻结 |

移交规则：

```text
grill-me 澄清完成
    ↓
任务是建设 / 改造 Agent 系统？
├─ 是 → 移交 agent-guided-builder 深化架构边界
└─ 否 → 直接实现，或按需移交专项 Skill
```

澄清产生的决策直接写入当前项目 `.agent-engineering/决策记录.md`，边界结论同步到 `边界画布.md`——不重复造账本格式。

---

## 4. Inspect Before Asking — 提问之前先自己查

禁止向用户询问可以从现有上下文合理获得的信息。

提问前优先检查：

```text
当前对话与用户已给出的要求
→ 项目代码与目录结构
→ README / AGENTS.md / CLAUDE.md / SKILL.md
→ 依赖清单（pom.xml / package.json / requirements.txt / pyproject.toml）
→ 配置文件（application.yml / .env.example）
→ 数据库结构 / API 文档
→ Dockerfile / docker-compose / 部署配置
→ 测试代码 / 日志
→ 必要时查看 Git 历史
```

错误示例：项目中已有 `jdbc:postgresql://...` 还问"你用的什么数据库？"。

正确做法：

```text
已经确认项目使用 PostgreSQL。
当前真正需要决定的是：
新增功能继续用 PostgreSQL，还是单独引入向量存储？
```

---

## 5. Decision Classification — 决策四分类

每个未决问题先归类，再决定处置方式：

### 5.1 Blocking（阻塞型）

没有答案就无法可靠实现。例：改旧接口还是新增 V2？是否允许破坏数据结构？以哪个系统为准？

> 处置：优先询问。

### 5.2 High-Impact（高影响型）

不同选择显著影响架构 / 性能 / 安全 / 成本 / 数据一致性。例：同步 REST vs RabbitMQ 异步。

> 处置：通常询问。

### 5.3 Boundary（边界型）

主流程清晰，但边缘情况可能出错。例：重复提交、消息重复消费、DB 成功但消息失败。

> 处置：技术型边界 → 采用业界标准做法自动处理；影响业务规则的边界 → 选择框询问。

### 5.4 Low-Impact（低影响型）

类名、方法名、DTO 位置、日志格式等小问题。

> 处置：不问，遵循现有项目规范。

### 禁止制造伪选项

明显错误的方案不交给用户选（如"密码存明文 / MD5 / BCrypt？"）——直接使用安全方案。

---

## 6. Native Selection UI First — 原生交互优先

需要用户决策时，按优先级使用交互方式：

```text
question 工具
    ↓
AskUserQuestion
    ↓
平台等价的结构化选择工具
    ↓
纯文本编号选项（仅当无原生 UI）
```

如果平台支持原生弹框，**必须调用工具**，而不是只在聊天中输出 A/B/C。

选择框默认中文：

```text
标题：通信方式
问题：Python Agent 服务应如何与 Java 后端通信？

REST API（推荐）—— 实现简单，适合同步调用，维护成本低。
RabbitMQ —— 适合耗时异步任务，但复杂度更高。
gRPC —— 强类型高性能，但引入额外维护成本。
让我自动选择 —— 根据现有项目架构自动选择。
```

---

## 7. Question Budget — 问题预算

用户的注意力有限，问题有认知成本：

| 任务规模 | 推荐决策问题 |
|---|---|
| 小任务 | 0–2 |
| 中型任务 | 1–4 |
| 大型任务 | 2–6 |
| 重大架构设计 | 3–8 |

软上限，不必问满。足够清晰时立即停止。

**高价值问题规则**：提问前自问"这个答案不同，会不会改变最终实现？"——不会就不问。

**一次解决一个核心决策**：一个选择框只解决一个问题，不要抛"数据库、缓存、MQ、认证分别用什么"式组合问卷。

**自适应追问**：

```text
分析 → 发现最大不确定点 → 询问 → 用户选择 → 更新决策状态 → 重新分析
```

每一个回答都必须改变后续判断；不预先生成固定问卷。

渐进式暴露复杂度：先解决当前最大决策，再根据结果决定下一个问题。

---

## 8. Option Design — 选项设计

每题 2–5 个选项（最佳 3–4 个），每个选项明确、有区别、可执行、附一句优缺点。

有明显更优方案时直接标注推荐并说明依据（当前架构 / 项目规范 / 成本 / 稳定性 / 安全），不要假装所有方案一样好。

**"让我自动选择"协议**：用户选择它之后 → 自己选定推荐方案 → 说明关键理由 → 记录为 `Agent Recommended Decision` → 继续执行，不重复询问。

**用户改选后的增量重开**：用户推翻之前的选择时，只重新检查受影响的决策（如单实例改 K8s 后需重查 Session / 本地缓存 / 分布式锁 / 定时任务），不要从头再问。

---

## 9. Boundary Scanning Framework — 边界扫描框架

13 类边界维度的完整战术检查单见：

```text
resources/boundary-checklists.md
```

维度速查：

```text
Input / Data / Concurrency / Transaction / Failure /
Permission / Security / Performance / API /
State Machine / Time / Deployment / Compatibility
```

进入执行前的快速扫描口诀：

```text
空值呢？不存在呢？重复呢？并发呢？超时呢？
失败呢？回滚呢？权限呢？安全呢？
数据量很大呢？旧版本呢？服务重启呢？依赖挂了呢？用户重复操作呢？
```

处置原则：

- 技术实现问题 → 自动采用标准做法解决，不打扰用户；
- 业务规则问题 → 提供选择框。

不为边界而边界：只有高风险、需业务决策、影响架构的边界才询问或特别说明。

领域专项检查单（API / Database / MQ / Cache / AI Agent / RAG / File Upload）同样见 resources，按任务涉及的技术栈选用。

---

## 10. Workflows

### 编码任务

```text
读取项目 → 理解现有架构 → 识别核心目标
→ 扫描主流程 → 扫描边界问题
→ 存在关键决策？ ── 否 → 开始实现
                  └─ 是 → 弹选择框 → 更新决策 → 再分析 → 实现
→ Build / Test → Verify
```

### 新项目

```text
目标 → 用户是谁 → 核心场景 → MVP 范围 → 系统边界
→ 核心架构 → 数据模型 → 接口边界 → 安全 → 并发 → 异常 → 部署 → 验收
```

可以推断的自己推断，有行业标准的自己决定，真正影响产品方向的才让用户选择——不要全部问一遍。

### Bug 修复

Bug 不做需求访谈：

```text
读取错误 → 查看日志 → 查看代码 → 定位根因 → 复现 → 修复
```

只在缺少关键条件时问（例如"该问题只出现在哪个环境？"）。

### 内部状态机

```text
DISCOVER（发现上下文）
    ↓
ANALYZE（分析需求和边界）
    ↓
DECIDE（出现高价值决策 → 弹框）
    ↓
EXECUTE（开始实现）
    ↓
VERIFY（验证功能和边界）
    ↓
DONE
```

允许 VERIFY → EXECUTE（发现 Bug）与 VERIFY → DECIDE（发现新业务决策）回跳。

---

## 11. Stop Conditions — 停止追问

满足以下大部分条件即停止提问，立即执行：

- 目标、范围明确；
- 关键接口与重要业务行为明确；
- 高风险边界已处理；
- 架构方向明确；
- 剩余问题可用合理默认值；
- 结果可以被验证。

禁止问"还有别的吗？""这样可以吗？""是否继续？"——除非真的存在需要授权的重大操作。

内部置信度参考（不向用户展示）：0–40% 非常模糊；40–70% 有方向；70–85% 大部分清楚；85%+ 可实施。达到可实施程度即停止。

---

## 12. Risk Escalation — 风险升级清单

以下类型的问题必须提高优先级，存在多个方案时必须弹出选择框或明确确认：

```text
删除数据 / 修改生产数据 / 修改数据库 Schema
大范围重构 / API Breaking Change
权限模型修改 / 身份认证修改
支付相关 / 库存相关
医疗关键判断 / 财务关键判断
安全相关操作 / 大规模数据迁移
```

---

## 13. Report Back to Master

澄清完成或移交其他 Skill 时，按 `../agent-engineering-master/SKILL-REGISTRY.md` 的 Return Contract 返回：

```text
Skill Used: agent-grill-me
Problem Addressed:
Decision / Change:        ← 已确认决策（含用户选择与 Agent Recommended Decision）
Boundary Impact:          ← 边界扫描结论与自动采用的默认值
Files / Components Affected:
Verification Performed:   ← 当前多为需求级验证（编译/测试属下游 Skill）
New Risks:                ← 尚未解决的边界或风险升级项
Unresolved Items:         ← 遗留开放问题
Recommended Next Capability:  ← guided-builder / greenfield-builder / existing-project-modifier / debugger 等
```

状态写回路由：

```text
已确认的关键决策 → .agent-engineering/决策记录.md
长期边界结论     → .agent-engineering/边界画布.md
当前任务进度     → .agent-engineering/当前会话.md
```

---

## 14. Completion Criteria

- 核心目标、范围、输入输出明确；
- Blocking 与 High-Impact 决策全部有归属（用户确认或记录为 Agent 推荐）；
- 高风险边界已识别并有处置策略；
- 技术型边界已采用标准默认值并记录；
- 未决项与风险显式列出，无静默假设；
- 下一步执行路径明确（自行实现或移交对应 Skill）。

---

## 15. Anti-Patterns

禁止：

- 问用户几十个异常场景凑数；
- 提供包含明显错误方案的伪选项；
- 一次抛十几个散乱问题的问卷轰炸；
- 重新询问已确认过的信息；
- 项目里能查到的信息还问用户；
- 只考虑 Happy Path，不扫描失败路径；
- 该弹原生选择框时只用纯文本 A/B/C；
- 问完不记录，导致下轮重复问。
