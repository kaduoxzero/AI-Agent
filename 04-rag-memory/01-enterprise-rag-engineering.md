# 企业级 RAG：从文档接入到可评估知识系统

## 1. RAG 不是“向量数据库 + LLM”

完整 RAG Pipeline：

```text
Source
 ↓
Parse
 ↓
Clean
 ↓
Chunk
 ↓
Metadata
 ↓
Embedding / Sparse Index
 ↓
Retrieval
 ↓
Rerank
 ↓
Context Build
 ↓
Generation
 ↓
Citation
 ↓
Evaluation
```

每一步都可能成为大型项目的质量瓶颈。

## 2. 文档接入

来源可能包括：

- PDF；
- Word；
- HTML；
- Markdown；
- Excel；
- 数据库；
- Wiki；
- API；
- 邮件。

解析后推荐统一 Document Schema：

```json
{
  "document_id": "...",
  "content": "...",
  "source": "...",
  "title": "...",
  "page": 12,
  "section": "3.2",
  "updated_at": "...",
  "tenant_id": "...",
  "acl": []
}
```

## 3. Chunking

Chunk 太大：召回内容噪声高。

Chunk 太小：上下文碎片化。

策略：

- fixed size；
- recursive；
- semantic；
- section-aware；
- table-aware。

企业文档通常应该尽量保留标题层级、页码和业务实体。

## 4. Embedding 与索引

### Dense Retrieval

语义向量搜索。

### Sparse Retrieval

BM25 等关键词搜索。

### Hybrid Search

```text
Dense Score
+
Sparse Score
→ Fusion
```

业务术语、编号、药品名、错误码等场景往往需要 Hybrid。

## 5. Rerank

第一阶段召回追求 Recall，Reranker 追求前几条的 Precision。

```text
Retriever Top 50
 ↓
Reranker
 ↓
Top 5
```

不要直接把 50 个 Chunk 全塞模型。

## 6. Metadata Filter 与权限

企业 RAG 必须把权限过滤前置到 Retrieval 层。

```text
User Identity
 ↓
ACL / Tenant Filter
 ↓
Retrieval
```

不能先把未授权文档检索给 LLM，再要求它“不要说”。

## 7. Citation

回答应能追溯：

```text
Answer Claim
 ↓
Document ID
Page / Section
Chunk ID
```

Citation 是 RAG 可审计性的基础。

## 8. Knowledge Freshness

需要处理：

```text
New Document
Update Document
Delete Document
Permission Change
```

典型方案：

- CDC；
- Event Queue；
- Incremental Index；
- Versioned Index。

## 9. RAG Evaluation

至少评估：

### Retrieval

- Recall@K；
- Precision@K；
- MRR / NDCG（需要时）。

### Generation

- Faithfulness；
- Answer Relevance；
- Citation Correctness；
- Completeness。

## 10. 反模式

### 所有文档同一种 Chunk

不同文档结构差异很大。

### 只有向量搜索

精确关键词和业务 ID 可能失败。

### 权限只在生成层控制

存在泄漏风险。

### 没有知识更新机制

Demo 能跑，生产很快变旧。

## 11. 检查清单

- [ ] 是否保留文档结构和来源？
- [ ] Chunk 是否针对文档类型设计？
- [ ] 是否 Hybrid Retrieval？
- [ ] 是否 Rerank？
- [ ] 是否在 Retrieval 层做 ACL？
- [ ] 是否有 Citation？
- [ ] 是否有增量更新？
- [ ] 是否有 Retrieval Eval？
