# Agentic RAG 与高级检索架构

## 1. 传统 RAG 与 Agentic RAG

传统 RAG：

```text
Question
 ↓
Retrieve once
 ↓
Generate
```

Agentic RAG：

```text
Question
 ↓
Agent decides whether to retrieve
 ↓
Query Rewrite / Decomposition
 ↓
Retrieve
 ↓
Evaluate Evidence
 ↓
Enough?
├─ YES → Answer
└─ NO → Retry / another source
```

## 2. 为什么需要 Agentic RAG

适用于：

- 多跳问题；
- 内外部多数据源；
- 第一次检索可能失败；
- 需要交叉验证；
- Research 任务。

简单 FAQ 不一定需要 Agentic RAG。

## 3. Query Rewrite

将用户自然语言转换为更适合检索的 Query。

例如：

```text
“这个病人最近是不是越来越差？”
```

转换：

```text
patient_id=xxx recent BP glucose symptom trend risk
```

但要保存原始 Query，避免 Rewrite 改变用户真实意图。

## 4. Query Decomposition

复杂问题拆成子问题：

```text
分析公司供应链风险
├─ 核心供应商是谁？
├─ 最近有哪些负面事件？
├─ 哪些供应商集中度过高？
└─ 是否存在区域风险？
```

然后并行检索。

## 5. Multi-Source Retrieval

```text
Planner
├─ Internal KB
├─ Database
├─ Search Engine
└─ API
```

最终 Evidence 层统一保存：

```json
{
  "claim": "...",
  "source_type": "kb",
  "source_id": "...",
  "content": "...",
  "timestamp": "...",
  "confidence": 0.9
}
```

## 6. Retrieval Evaluator

检索后先判断证据是否足够，而不是立刻回答。

Evaluator 可检查：

- 是否覆盖问题；
- 来源是否可信；
- 是否存在冲突；
- 是否足够新；
- 是否需要更多证据。

## 7. Corrective / Adaptive 思路

可以设计：

```text
Evidence low quality
→ rewrite query
→ switch source
→ broaden retrieval
→ web search
```

不要机械循环，必须设置最大重试次数。

## 8. GraphRAG 与 Knowledge Graph

当问题依赖实体关系、多跳关系或全局主题时，可以考虑图结构。

例如：

```text
Company
 ├─ supplies_from → Supplier
 ├─ located_in → Region
 └─ affected_by → Event
```

图不是向量数据库的替代品，通常是补充。

## 9. Retrieval Budget

Agentic RAG 可能疯狂查询。

建议控制：

```yaml
retrieval_budget:
  max_queries: 8
  max_documents: 100
  max_rerank_items: 50
  max_web_searches: 3
```

## 10. 生产架构

```text
User
 ↓
Intent / Router
 ↓
Retrieval Planner
 ↓
┌──────────┬──────────┬──────────┐
KB         DB         Web
└──────────┴──────────┴──────────┘
 ↓
Evidence Store
 ↓
Evaluator
 ↓
Synthesizer
 ↓
Citation
```

## 11. 检查清单

- [ ] 是否真的需要 Agentic RAG？
- [ ] 是否保留原始 Query？
- [ ] 多源 Evidence 是否统一 Schema？
- [ ] 是否评估 Evidence Sufficiency？
- [ ] 是否限制检索轮数？
- [ ] 是否处理来源冲突？
- [ ] 是否保留 Citation？
