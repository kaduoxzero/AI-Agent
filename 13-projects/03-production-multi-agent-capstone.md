# 毕业项目：生产级 Research + RAG + Data Multi-Agent 平台

> 这是整套知识库的综合项目。目标不是做一个演示页面，而是完整覆盖大型 Agent 项目需要的架构、状态、任务、权限、评估和部署。

## 1. 业务目标

用户输入复杂研究任务，例如：

> “结合公司内部供应链资料、数据库指标和最近公开新闻，分析供应商 A 的风险，列出证据、风险等级和可执行建议。”

系统需要：

1. 识别任务类型；
2. Planner 拆任务；
3. Research Agent 查询公开来源；
4. RAG Agent 查询内部资料；
5. Data Agent 查询结构化指标；
6. Risk Agent 基于 Evidence 分析；
7. Reviewer 检查事实和 Citation；
8. 高风险建议需要人工确认；
9. 任务可暂停、恢复、取消；
10. 全链路 Eval / Trace。

## 2. 总体架构

```text
                         Web UI
                           ↓
                     API Gateway
                           ↓
                Auth / Tenant / Policy
                           ↓
                      Task Service
                           ↓
                          Queue
                           ↓
                    Agent Runtime
                           ↓
                        Router
                           ↓
                        Planner
             ┌─────────────┼─────────────┐
             ↓             ↓             ↓
        Research Agent   RAG Agent     Data Agent
             ↓             ↓             ↓
           Search        KB/MCP        DB Tool
             └─────── Evidence Store ─────┘
                           ↓
                       Risk Agent
                           ↓
                       Reviewer
                           ↓
                     Policy / HITL
                           ↓
                        Report
                           ↓
                       Artifact
```

外围：

```text
Checkpoint
Memory
Tracing
Evaluation
Metrics
Audit
Sandbox
Cost Budget
```

## 3. Monorepo 建议

```text
agent-platform/
├─ apps/
│  ├─ api/
│  ├─ worker/
│  └─ web/
├─ packages/
│  ├─ agent-core/
│  ├─ workflows/
│  ├─ tools/
│  ├─ retrieval/
│  ├─ memory/
│  ├─ security/
│  ├─ evals/
│  └─ observability/
├─ prompts/
├─ skills/
├─ tests/
│  ├─ unit/
│  ├─ integration/
│  ├─ evals/
│  └─ security/
├─ deploy/
└─ docs/
```

## 4. 核心 State

```python
class TaskState(TypedDict):
    task_id: str
    tenant_id: str
    user_query: str
    intent: str
    plan: list[dict]
    evidence: list[dict]
    analysis: dict | None
    report: str | None
    pending_approval: dict | None
    errors: list[dict]
    budget: dict
    status: str
```

不要在 State 中保存所有原始大文档；保存 Artifact / Document Reference。

## 5. Evidence Schema

```python
class Evidence(BaseModel):
    id: str
    claim: str
    source_type: Literal["web", "kb", "db"]
    source_id: str
    content: str
    observed_at: datetime
    confidence: float
```

所有 Agent 通过 Evidence 协作，而不是互相传整段自然语言聊天。

## 6. Router

输出：

```json
{
  "needs_web": true,
  "needs_kb": true,
  "needs_data": true,
  "risk_level": "high"
}
```

Router 可用快模型。

## 7. Planner

Planner 生成 Task DAG：

```json
[
  {"id": "t1", "agent": "rag", "depends_on": []},
  {"id": "t2", "agent": "data", "depends_on": []},
  {"id": "t3", "agent": "research", "depends_on": []},
  {"id": "t4", "agent": "risk", "depends_on": ["t1","t2","t3"]}
]
```

前三个并行。

## 8. Research Agent

Tool：

```text
search_web
fetch_page
```

职责只产生可引用 Evidence，不做最终风险结论。

## 9. RAG Agent

职责：

- Query Rewrite；
- ACL Retrieval；
- Rerank；
- Evidence Extract。

内部文档绝不能绕过 tenant ACL。

## 10. Data Agent

只读数据库 Tool：

```text
get_supplier_metrics
get_incident_history
```

优先业务 Tool，不让模型生成任意生产 SQL。

## 11. Risk Agent

输入只使用经过验证的 Evidence。

输出：

```json
{
  "risk_level": "high",
  "reasons": [...],
  "recommended_actions": [...],
  "confidence": 0.86
}
```

## 12. Reviewer

组合：

```text
Schema validation
Citation validation
LLM rubric
Rule engine
```

Reviewer 发现 Evidence 不足可以路由回特定 Worker，而不是让所有 Worker 重跑。

## 13. HITL

例如“暂停采购”属于高影响建议：

```text
Risk Agent proposes
 ↓
Policy → require approval
 ↓
Task WAITING_APPROVAL
 ↓
Human reviews evidence
 ↓
approve / reject / edit
```

## 14. Runtime Budget

```yaml
max_duration_seconds: 300
max_model_calls: 40
max_tool_calls: 60
max_parallel_workers: 5
max_research_queries: 8
max_cost_usd: 2.0
```

## 15. Task Backend

```text
POST /tasks
GET /tasks/{id}
GET /tasks/{id}/events
POST /tasks/{id}/cancel
POST /tasks/{id}/resume
POST /tasks/{id}/approvals/{id}
GET /tasks/{id}/artifacts
```

## 16. Persistence

保存：

```text
Task metadata → PostgreSQL
Checkpoint → PostgreSQL / durable store
Artifacts → Object Storage
Cache → Redis
Vectors → pgvector / vector DB
Trace → observability backend
```

## 17. Security

必须测试：

### Prompt Injection

公开网页中的恶意指令不能调用内部 Tool。

### Tool Permission

Research Agent 没有 Write Tool。

### Tenant Isolation

Tenant A RAG 不可看到 Tenant B 文档。

### Memory

外部 Evidence 不自动进入长期 Memory。

### Sandbox

如果加入 Coding Worker，必须隔离运行。

## 18. Evaluation Suite

### Router

route accuracy >= 95%。

### Retrieval

Recall@K / Citation Correctness。

### Task

复杂任务成功率。

### Trajectory

- 是否遗漏必须 Worker；
- 是否错误调用 Tool；
- 是否超过预算；
- 是否产生不必要 Handoff。

### Security

Critical security cases 必须 100% 阻止危险 Action。

## 19. Observability

Trace：

```text
Task
├─ Router span
├─ Planner span
├─ RAG worker span
├─ Data worker span
├─ Research worker span
├─ Risk span
├─ Reviewer span
└─ Approval span
```

Metrics：

```text
success_rate
p95_duration
cost_per_task
tool_failure_rate
human_approval_rate
citation_error_rate
```

## 20. Deployment

本地：Docker Compose。

生产：

```text
Load Balancer
API replicas
Queue
Worker replicas
PostgreSQL
Redis
Object Storage
Vector DB
Observability
```

Worker 根据 Queue Lag 扩缩容。

## 21. CI/CD

```text
Unit Test
→ Tool Test
→ Workflow Test
→ Agent Eval
→ Security Eval
→ Build
→ Staging
→ Smoke Eval
→ Canary
→ Production
```

## 22. 里程碑

### M1：Single Agent Baseline

完成 Tool + RAG + Trace。

### M2：Workflow

加入 Router / Planner / Reviewer。

### M3：Multi-Agent

拆 Research / RAG / Data。

### M4：Production

Queue、Checkpoint、HITL、Cancel、Resume。

### M5：Quality

Eval、Security、Canary、Cost Dashboard。

## 23. 最终验收标准

完成项目后，你应该能够解释并实现：

- 为什么使用 Multi-Agent；
- State 怎么设计；
- Context 怎么隔离；
- Tool 为什么最小权限；
- RAG 怎么做 ACL；
- Agent 如何恢复；
- 如何防 Prompt Injection；
- 如何评估 Trajectory；
- 如何控制 Token / Cost；
- 如何水平扩展 Worker；
- 如何做 CI/CD Eval Gate。

如果这些都可以独立设计和落地，就已经从“会写 Agent Demo”进入生产级 Agent Engineer。
