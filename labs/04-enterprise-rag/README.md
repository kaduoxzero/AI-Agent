# Lab 04｜Enterprise RAG：ACL、Metadata、Rerank 与 Citation

> 目标：从“把文档塞进向量库”升级到真正可治理的企业检索链路。

## 1. 学习目标

完成后应能够：

- 在 Retrieval 前执行 Tenant / ACL 过滤；
- 使用 Metadata 限定检索空间；
- 将 Recall 与 Rerank 分成两个阶段；
- 生成可追溯 Citation；
- 在没有命中证据时显式返回 Evidence Insufficient；
- 理解向量数据库只是 RAG 的一个组件，不是完整 RAG 系统。

## 2. 专业名词通义

- **ACL（Access Control List）**：访问控制列表，规定哪些主体能读取某份文档。
- **Metadata Filter**：按 tenant、department、document_type、date 等结构化字段先过滤文档。
- **Recall / Candidate Retrieval**：第一阶段尽量找全可能相关候选。
- **Rerank**：对候选结果进行第二次精排。
- **Citation**：最终回答所引用的具体证据来源。

## 3. 为什么实验默认不用真实向量数据库

本实验重点是 RAG 架构而不是某个数据库 SDK。默认 Retrieval 使用本地 token-overlap baseline，让所有人不配置外部服务也能运行。

真实项目只需要替换 `Retriever.search()` 内部实现为：

```text
pgvector
Milvus
Qdrant
Elasticsearch
OpenSearch
Vector + BM25 Hybrid
```

ACL、Metadata、Rerank、Citation 等上层设计保持不变。

## 4. 运行

```bash
cd labs/04-enterprise-rag
python app.py
```

## 5. 实验链路

```text
Query
 ↓
Identity / Tenant
 ↓
ACL + Metadata Filter
 ↓
Candidate Retrieval
 ↓
Rerank
 ↓
Evidence
 ↓
Answer + Citation
```

## 6. 实验任务

分别执行：

```bash
python app.py --tenant tenant-a --query "供应商交付异常"
python app.py --tenant tenant-b --query "供应商交付异常"
```

观察两个 Tenant 的检索结果完全隔离。

再尝试查询没有证据支持的问题，确认系统不会伪造 Citation。

## 7. 生产化要求

真实项目建议把以下对象都设计成独立 Adapter：

```text
DocumentStore
Retriever
Reranker
PermissionFilter
CitationBuilder
```

这样 Embedding Model、Vector DB 或 Reranker 替换时不会侵入业务层。

## 8. 验收标准

- [ ] Tenant A 永远看不到 Tenant B 文档；
- [ ] 检索结果带 document_id；
- [ ] Rerank 和 Candidate Retrieval 分离；
- [ ] 最终结果带 Citation；
- [ ] 无证据时不会编造结论；
- [ ] 能说明如何把 Retriever 替换成 pgvector / Qdrant。
