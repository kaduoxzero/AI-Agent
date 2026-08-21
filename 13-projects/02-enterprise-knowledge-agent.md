# 企业知识库 Agent：从 RAG Demo 到生产平台

## 1. 目标

构建一个可用于企业真实内部资料的知识 Agent，支持：

- 文档权限；
- 多数据源；
- Agentic Retrieval；
- Citation；
- 多轮 Context；
- Feedback；
- Eval；
- Audit。

## 2. 总体架构

```text
                 ┌──────── Ingestion Pipeline ────────┐
Documents → Parse → Chunk → Metadata → Index → Version
                 └─────────────────────────────────────┘

User
 ↓
Auth
 ↓
Query API
 ↓
Router
 ↓
Query Rewrite
 ↓
Permission Filter
 ↓
Hybrid Retrieval
 ↓
Rerank
 ↓
Evidence Evaluator
 ↓
Agent
 ↓
Citation / Guardrail
 ↓
Answer
```

## 3. 技术组件

### Backend

- Python FastAPI / Java Spring 均可；
- PostgreSQL；
- pgvector / vector DB；
- Redis；
- Object Storage；
- Queue。

### Agent

- LangGraph 或其他 Agent Runtime；
- Structured Output；
- Tool Registry。

## 4. 文档 Ingestion

```text
Upload / Sync
 ↓
Virus / type check
 ↓
Parser
 ↓
Normalize
 ↓
Chunk
 ↓
Metadata
 ↓
Embedding
 ↓
Index
```

### Metadata

至少：

```text
document_id
tenant_id
acl
source
version
updated_at
page
section
```

## 5. Query Path

### Intent

区分：

```text
simple faq
knowledge question
structured data query
research task
```

简单 FAQ 不必启动复杂 Research Agent。

### Permission

用户 ACL 在 Retrieval 前过滤。

### Hybrid Search

Dense + BM25。

### Rerank

控制最终 Context。

## 6. Agentic Retrieval

当第一次结果不足：

```text
Evidence Evaluator
 ↓ insufficient
Query Rewrite
 ↓
retrieve again
```

最大重试例如 2-3 次。

## 7. Citation

Answer 中每个重要事实尽量能映射到：

```text
doc_id + page + chunk_id
```

## 8. Memory

只保存真正有价值的信息。

例如用户长期偏好可以进入 Memory；一次知识问答检索结果通常不应永久写入用户 Memory。

## 9. Feedback

用户可以：

- 👍 / 👎；
- 标记 Citation 错；
- 提交正确答案；
- 请求人工审核。

反馈进入 Eval Dataset，而不是直接无审核写入知识库。

## 10. Evaluation

### Retrieval Dataset

```text
question → relevant_document_ids
```

### Answer Dataset

```text
question → expected facts / rubric
```

### Security Dataset

测试：

- 无权限文档；
- Prompt Injection 文档；
- 跨 Tenant 查询；
- 恶意上传。

## 11. API

```text
POST /documents
GET /documents/{id}
POST /knowledge/tasks
GET /tasks/{id}
GET /tasks/{id}/events
POST /feedback
```

## 12. Production Checklist

- [ ] 文档更新能否增量同步？
- [ ] ACL 是否在 Retrieval 前？
- [ ] Citation 是否可追溯？
- [ ] 是否有 Retrieval / Answer Eval？
- [ ] Prompt Injection 文档是否测试？
- [ ] Tenant 是否隔离？
- [ ] Feedback 是否经过审核再成为知识？
- [ ] 是否统计无答案率和人工升级率？
