# Reference Agent Platform Starter

> 这是知识库的最小可运行生产架构脚手架。它不是完整产品，而是为毕业项目提供稳定的工程起点。

## 1. 目标

Starter 先建立这些边界：

```text
Client
  ↓
FastAPI Task API
  ↓
Task Contract
  ↓
Task Store / Queue Adapter（后续替换）
  ↓
Agent Worker / Runtime（后续接入）
  ↓
PostgreSQL / Redis
```

第一版故意使用 In-Memory Task Store，让 API 可以立即运行；后续 Lab 再把它逐步替换为 PostgreSQL + Redis Queue。

## 2. 目录

```text
starter/
├─ apps/
│  └─ api/
│     └─ main.py
├─ packages/
│  └─ contracts.py
├─ Dockerfile
├─ docker-compose.yml
└─ pyproject.toml
```

## 3. 运行方式 A：本地 Python

```bash
cd reference-architecture/starter
python -m venv .venv
.venv\Scripts\activate
pip install -e .
uvicorn apps.api.main:app --reload --port 8000
```

访问：

```text
GET  /health
POST /tasks
GET  /tasks/{task_id}
POST /tasks/{task_id}/cancel
```

FastAPI Swagger：

```text
http://127.0.0.1:8000/docs
```

## 4. 运行方式 B：Docker Compose

```bash
docker compose up --build
```

启动：

- API: `8000`
- PostgreSQL: `5432`
- Redis: `6379`

## 5. 专业名词通义

- **Task API**：面向前端和外部系统的长任务控制接口，不把 Agent 执行绑定在一个同步 HTTP 请求里。
- **Contract**：跨 API、Worker、Queue 使用的稳定结构化数据模型。
- **Adapter**：隔离具体数据库、队列、模型 Provider 的实现层。
- **Reference Architecture**：推荐的工程边界和组合方式，不是要求所有业务逐行复制。

## 6. 下一步扩展顺序

建议严格按顺序升级：

```text
M1 In-Memory Task API
 ↓
M2 PostgreSQL Task Repository
 ↓
M3 Redis Queue + Worker
 ↓
M4 Agent Runtime
 ↓
M5 Checkpoint / Resume
 ↓
M6 HITL Approval
 ↓
M7 AG-UI / SSE Event Stream
 ↓
M8 Eval / Trace / Security
```

## 7. 生产边界

Starter 里的 In-Memory Store 仅用于教学：

```text
进程重启 → 数据丢失
多副本 → 状态不一致
```

因此生产阶段必须替换为耐久存储。

同样，真实 Agent Worker 不应该直接写在 FastAPI Handler 内长期执行，应通过 Queue / Worker 解耦。

## 8. 验收标准

- [ ] `docker compose up --build` 可以启动依赖；
- [ ] 可以创建 Task；
- [ ] 可以查询 Task；
- [ ] 可以取消 Task；
- [ ] API Contract 与内部 Store 解耦；
- [ ] 能解释为什么 Agent 长任务不能依赖同步 HTTP 生命周期；
- [ ] 能说明如何把 In-Memory Store 替换为 PostgreSQL Repository。
