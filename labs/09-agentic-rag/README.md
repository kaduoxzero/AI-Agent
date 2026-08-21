# Lab 09｜Agentic RAG：Query Rewrite、Evidence Sufficiency 与 Retrieval Budget

> 目标：让 Agent 自主决定“是否需要检索、怎么改写 Query、证据够不够、是否继续检索”，但由 Runtime 强制限制检索预算。

## 1. 学习目标

完成后应能够：

- 区分固定 RAG Pipeline 与 Agentic RAG；
- 实现 Query Rewrite；
- 对 Evidence 做 Sufficiency 判断；
- 在证据不足时进行第二轮检索；
- 使用 `max_retrieval_rounds` 防止无限搜索；
- 在最终回答中只引用实际检索到的 Evidence。

## 2. 专业名词通义

- **Query Rewrite**：把用户原始问题改写为更适合检索系统的 Query。
- **Evidence Sufficiency**：判断现有证据是否足够支持回答，而不是只看“搜到了几条”。
- **Retrieval Budget**：允许执行的最大检索轮数、Query 数量或成本。
- **Adaptive Retrieval**：根据任务和当前证据动态决定是否继续检索。

## 3. 运行

```bash
cd labs/09-agentic-rag
python app.py
```

## 4. 流程

```text
User Query
 ↓
Need Retrieval?
 ↓ yes
Rewrite Query
 ↓
Retrieve
 ↓
Evidence Sufficient?
 ├─ yes → Answer
 └─ no  → Rewrite / Retrieve again
             ↓
          Budget reached?
```

## 5. 工程原则

Agent 可以决定“下一轮搜什么”，但不应该决定“可以无限搜”。

```text
Planning = model / agent policy
Budget   = deterministic runtime policy
```

## 6. 验收标准

- [ ] 有显式 Retrieval Budget；
- [ ] Evidence 不足时不会直接编造答案；
- [ ] 第二轮 Query 与第一轮不同；
- [ ] Citation 只指向真实 Evidence；
- [ ] 达到预算后明确返回 `evidence_insufficient`；
- [ ] 能说明如何替换成真实 Vector DB / Web Search Adapter。
