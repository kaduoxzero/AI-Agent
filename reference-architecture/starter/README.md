# Reference Agent Platform

> 这是知识库的可运行生产参考实现。默认离线测试不需要真实模型 Key；Docker Compose 模式会启用 PostgreSQL + Redis + 独立 Worker，展示大型 Agent 系统真正需要的 API / Queue / Runtime / HITL / Event 边界。

## 1. 当前能力

```text
Client
  ↓
FastAPI Task API
  ↓
Task Repository ───────── PostgreSQL
  ↓
Redis Queue
  ↓
Agent Worker
  ↓
Agent Runtime
  ├─ Runtime Budget
  ├─ Model Gateway
  ├─ Tenant-scoped RAG
  ├─ Tool Gateway + Scope
  ├─ Policy / HITL
  └─ Typed Artifact / Evidence
  ↓
Task Event Store ──────── Redis
```

当前已经实现：

- Typed Task / Budget / Evidence / Artifact / Event Contract；
- In-Memory Adapter，用于单元测试和本地理解；
- PostgreSQL Task Repository；
- Redis Task Queue；
- API / Worker 进程分离；
- Provider-agnostic Model Gateway；
- Tenant ACL 优先的参考 Retriever；
- Tool Scope 与 Tool Gateway；
- Human Approval Gate；
- cooperative cancellation；
- Runtime step / model / tool budget；
- Redis Task Event；
- Docker Compose；
- API 与 Runtime 自动测试。

## 2. 目录

```text
starter/
├─ apps/
│  ├─ api/main.py
│  └─ worker/main.py
├─ packages/
│  ├─ config.py
│  ├─ contracts.py
│  ├─ dependencies.py
│  ├─ events.py
│  ├─ memory.py
│  ├─ model_gateway.py
│  ├─ policy.py
│  ├─ queueing.py
│  ├─ rag.py
│  ├─ repositories.py
│  ├─ runtime.py
│  └─ tools.py
├─ tests/
├─ Dockerfile
├─ docker-compose.yml
└─ pyproject.toml
```

## 3. 本地测试模式

没有 `DATABASE_URL` / `REDIS_URL` 时自动使用 In-Memory Adapter：

```bash
cd reference-architecture/starter
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
# source .venv/bin/activate

pip install -e ".[dev]"
pytest -q
uvicorn apps.api.main:app --reload --port 8000
```

该模式适合 API Contract 和 Runtime 单元测试。由于 API 与独立 Worker 不能跨进程共享 Python 内存队列，完整异步执行请使用 Docker Compose。

## 4. 完整异步模式

```bash
docker compose up --build
```

启动：

- API / Swagger：`http://127.0.0.1:8000/docs`
- PostgreSQL：`5432`
- Redis：`6379`
- Worker：独立容器消费 Redis Queue

Docker 模式使用：

```text
DATABASE_URL=postgresql+asyncpg://...
REDIS_URL=redis://...
```

API 和 Worker 都调用 `create_all` 初始化教学表结构。正式生产系统应改为 Alembic migration。

## 5. API

```text
GET  /health
POST /tasks
GET  /tasks/{task_id}
GET  /tasks/{task_id}/events?start=0
POST /tasks/{task_id}/cancel
POST /tasks/{task_id}/approval
```

创建任务：

```json
{
  "tenant_id": "tenant-a",
  "user_id": "user-001",
  "query": "结合内部资料和公开新闻分析供应商风险",
  "budget": {
    "max_steps": 12,
    "max_model_calls": 8,
    "max_tool_calls": 12,
    "max_cost_usd": 1.0
  }
}
```

高影响请求，例如“暂停采购”，Runtime 不继续执行，而会进入：

```text
WAITING_APPROVAL
```

审批：

```json
{
  "approve": true,
  "reason": "已核验证据",
  "actor_id": "reviewer-001"
}
```

批准后 Task 重新入队；拒绝后进入 `CANCELLED`。

## 6. 专业名词通义

- **Repository Adapter**：把 Domain 与 PostgreSQL 等具体存储实现隔离。
- **Task Queue**：API 只接收任务，Worker 异步执行，避免 Agent 生命周期依赖 HTTP 请求生命周期。
- **Cooperative Cancellation**：API 写入取消意图，Worker 在安全边界读取并停止，而不是直接 kill 进程。
- **Runtime Budget**：由程序强制限制 Step / Model Call / Tool Call，而不是 Prompt 里提醒模型节省成本。
- **Typed Artifact**：Agent 最终产物使用稳定 Schema，而不是只能读取自然语言聊天历史。
- **Event Store**：记录 `TaskCreated / PlanCreated / ToolCompleted / ApprovalRequested / RunCompleted` 等运行事件，供 UI、Trace、Eval 使用。
- **Durable Mode**：Task 和 Queue 都由外部耐久系统承载，API/Worker 可重启和水平扩容。

## 7. 已实现与下一阶段边界

当前实现已经跨过“单进程 Demo”阶段，但仍有明确升级空间：

```text
当前
Postgres Task + Redis Queue + Worker + Runtime + HITL + Event

下一阶段
Checkpoint / Resume
→ Artifact Object Storage
→ Real Model Provider + Model Routing
→ MCP Tool Gateway
→ pgvector / Hybrid RAG
→ Long-term Memory Store
→ AG-UI / SSE
→ OpenTelemetry Trace
→ Eval Gate
→ Agent Registry / Canary / Rollback
```

这些能力在本仓库 18 个 Labs 中都有独立训练，再逐步并入 Reference Platform。

## 8. 生产注意事项

Reference Platform 用于教学和架构基线，不代表可以原样处理高风险生产业务。正式上线至少继续补：

- Alembic migration；
- Secret Manager / Credential Broker；
- AuthN / AuthZ / Tenant Boundary；
- Durable Checkpoint；
- Object Storage；
- OpenTelemetry；
- distributed rate limit；
- idempotency key；
- retry / DLQ；
- security eval；
- backup / restore；
- SLO / alert / runbook。

## 9. 验收标准

- [ ] API 与 Worker 不在同一同步调用链；
- [ ] Docker 模式 Task 持久化到 PostgreSQL；
- [ ] Redis Queue 可以由 Worker 消费；
- [ ] Task Event 可查询；
- [ ] Runtime Budget 能让任务 Fail Closed；
- [ ] 高影响任务进入 HITL；
- [ ] Tenant A 的 RAG 不返回 Tenant B 文档；
- [ ] Tool Call 需要 Scope；
- [ ] 结果以 Artifact + Evidence 返回；
- [ ] 单元测试不依赖真实付费模型 API。
