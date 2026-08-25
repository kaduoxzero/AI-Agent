---
name: agent-rag-engineer
version: 1.1.0
description: Design, build, review, or upgrade RAG and Agentic RAG systems for Agent projects. Use when the system needs enterprise knowledge ingestion, retrieval, metadata filtering, tenant isolation, reranking, evidence and citations, query rewriting, multi-hop retrieval, freshness, or retrieval evaluation.
---

# Agent RAG Engineer

## Objective

把“接一个向量库”升级为真正可评估、可追溯、可隔离、可维护的知识系统。

## Core Principle

RAG 的核心不是 Vector DB，而是：

```text
Knowledge Lifecycle
+ Retrieval Quality
+ Evidence Contract
+ Access Control
+ Evaluation
```

## 1. Define Knowledge Boundary

先明确：

- 数据来源；
- 更新频率；
- 权限模型；
- Tenant / Department / User Scope；
- 文档类型；
- 是否需要结构化数据联合查询；
- 是否需要实时 Web / API 数据。

## 2. Ingestion Pipeline

推荐：

```text
Source
→ Parse
→ Normalize
→ Deduplicate
→ Chunk
→ Metadata
→ Embed
→ Index
→ Version
```

必须保留：

- document_id；
- chunk_id；
- source_uri；
- tenant_id；
- version；
- updated_at；
- document_type；
- access scope。

## 3. Chunking

不要只用固定字符数。

根据内容考虑：

- semantic boundary；
- heading hierarchy；
- table / code / list；
- overlap；
- parent-child chunk；
- small-to-big retrieval。

Chunk 策略必须进入 Eval，而不是凭感觉决定。

## 4. Retrieval Pipeline

成熟检索通常是：

```text
Query
→ Intent / Rewrite
→ Metadata Filter
→ Candidate Retrieval
→ Hybrid Search
→ Rerank
→ Deduplicate
→ Evidence Pack
```

可组合：

- Dense Retrieval；
- BM25 / Sparse；
- Hybrid；
- Metadata Filter；
- Reranker；
- Query Expansion；
- Multi-Query；
- Parent Retrieval；
- Graph / SQL Retrieval。

## 5. Agentic RAG

只有当 Agent 需要动态决定以下行为时才升级为 Agentic RAG：

- 是否检索；
- 检索哪个知识源；
- 是否改写 Query；
- 是否继续检索；
- 是否调用 SQL / API / Web；
- 是否根据 Evidence 缺口补搜。

必须设置：

- max retrieval rounds；
- max sources；
- timeout；
- cost budget；
- stop criteria。

## 6. Evidence Contract

所有检索结果优先转换为统一 Evidence：

```text
Evidence
├─ source_type
├─ source_id
├─ chunk_id
├─ content
├─ score
├─ metadata
├─ citation
└─ retrieved_at
```

生成模块不应依赖某个 Vector DB 的原生返回结构。

## 7. Grounded Generation

Prompt 必须区分：

```text
System instruction
User question
Trusted structured context
Retrieved untrusted content
Citation requirement
Abstention rule
```

外部文档内容默认视为 **不可信数据**，不能自动提升为 System Instruction。

## 8. Tenant Isolation

企业 RAG 必须在检索前施加权限过滤，而不是生成后再过滤。

禁止：

```text
Retrieve all tenants
→ LLM decides what can be shown
```

正确方向：

```text
Identity
→ Access Scope
→ Metadata Filter
→ Retrieval
```

## 9. Freshness

为可更新知识设计：

- version；
- tombstone / delete；
- reindex；
- incremental ingestion；
- freshness SLA；
- cache invalidation。

## 10. RAG Evaluation

至少评估：

### Retrieval

- Recall@K；
- Precision@K；
- MRR / NDCG（需要时）；
- correct source hit rate；
- tenant leakage = 0。

### Generation

- groundedness；
- citation correctness；
- answer relevance；
- abstention correctness；
- unsupported claim rate。

## 11. Failure Cases

必须覆盖：

- 无命中；
- 低质量命中；
- 冲突文档；
- 过期文档；
- 恶意 Prompt Injection 文档；
- 超长文档；
- 表格；
- 多租户；
- 同名实体；
- 多跳问题。

## 12. Migration Rule

更换 Vector DB / Embedding / Reranker 时：

- 保持 Evidence Contract；
- 保留 Golden Query Set；
- 新旧索引并行对比；
- 不直接删除旧索引；
- 达到 Eval Gate 后再切换。

## Anti-Patterns

禁止：

- 只测“最终回答看起来不错”；
- 不保存 source_id；
- 不做 metadata filter；
- 把 TopK 调大当成解决召回问题；
- 把整份文档塞进 Context；
- 所有问题都强制检索；
- 让 LLM 决定权限。

## Report Back to Master

完成后，按 `../agent-engineering-master/SKILL-REGISTRY.md` 的 Return Contract 返回；Retrieval / Generation Eval 结果应写入 Verification Performed，检索预算与 Agentic 升级决策写入 Decision / Change。

---

## Completion Criteria

- Ingestion 可重复执行；
- Evidence 可追溯；
- Tenant 隔离有测试；
- Retrieval 有 Golden Set；
- Citation 可验证；
- 无命中时能正确拒答或降级；
- RAG 组件可独立替换而不破坏 Agent Contract。
