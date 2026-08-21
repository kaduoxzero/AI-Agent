# 专项 Agent 架构：Coding、Research、Data 与 Browser Agent

## 1. 为什么专项 Agent 架构不同

Agent 的核心 Loop 类似，但“工作环境、验证器、Tool 和 State”不同。

## 2. Coding Agent

### 架构

```text
Issue / Task
 ↓
Understand
 ↓
Plan / Todo
 ↓
Code Search
 ↓
Read Files
 ↓
Patch
 ↓
Run Tests / Build
 ↓
Inspect Failure
 ↓
Revise
 ↓
Review Diff
 ↓
Result
```

### 必备 Tool

- repository search；
- read file；
- patch；
- shell；
- test runner；
- git diff。

### 必备工程能力

```text
Sandbox
Filesystem
Git
Test
Context Compaction
Todo
Checkpoint
```

### Validator

Coding Agent 最大优势是存在强验证器：

```text
compile
test
lint
static analysis
```

优先这些，而不是只让 Review Agent 读代码。

### 常见错误

- 修改前不搜索调用点；
- 只修代码不补测试；
- Shell 无隔离；
- Context 塞整个 Repo；
- 测试失败后无限重试。

## 3. Research Agent

### 架构

```text
Question
 ↓
Research Plan
 ↓
Query Decomposition
 ↓
Parallel Search
 ↓
Fetch Sources
 ↓
Evidence Extraction
 ↓
Cross Validation
 ↓
Synthesis
 ↓
Citation
 ↓
Quality Review
```

### 核心 State

```text
research_questions
sources
evidence
claims
conflicts
citations
```

### 关键原则

Final Report 不直接基于搜索摘要，而应基于 Evidence Store。

### Source Quality

考虑：

- authority；
- freshness；
- primary vs secondary；
- conflict。

## 4. Data Agent

### 架构

```text
User Question
 ↓
Intent
 ↓
Schema / Metadata Retrieval
 ↓
Plan
 ↓
SQL / Python
 ↓
Execute in controlled environment
 ↓
Validate Result
 ↓
Explain / Visualize
```

### 安全

默认 Read-only。

SQL：

```text
AST validation
allowlist schema
row limit
timeout
read-only transaction
```

不要让 LLM 直连生产数据库 admin account。

### Validation

- SQL 是否执行成功；
- 数据量是否异常；
- aggregation 是否符合问题；
- 是否泄露未授权列。

## 5. Browser Agent

### 架构

```text
Observe
 ↓
Plan next action
 ↓
DOM / Browser Tool
 ↓
Verify
 ↓
Continue
```

重点：每次 Action 后 Verify。

高风险 Submit / Purchase / Delete 必须审批。

## 6. 四类 Agent 对比

| Agent | 核心环境 | 最强验证器 | 主要风险 |
|---|---|---|---|
| Coding | Sandbox Repo | tests/compiler | RCE / destructive edit |
| Research | Web + KB | source/citation eval | misinformation |
| Data | DB/Python | query/result validation | data leakage |
| Browser | browser session | page state verification | prompt injection/action misuse |

## 7. 组合

大型项目经常：

```text
Research Agent
+ Data Agent
+ Coding Agent
```

由 Orchestrator 统一协调，而不是把所有 Tool 塞给一个 Agent。
