# Lab 10｜Memory Engineering：Write Policy、TTL、Conflict 与 Poisoning Protection

> 目标：理解 Memory 不是 Conversation History 的别名，而是一个需要写入策略、生命周期、来源和安全边界的长期数据系统。

## 1. 学习目标

完成后应能够：

- 区分 Working / Episodic / Semantic Memory；
- 只把满足策略的信息写入长期 Memory；
- 给 Memory 记录来源与 Trust Level；
- 使用 TTL 控制生命周期；
- 处理同一 Key 的新旧冲突；
- 阻止不可信网页 / Tool Result 自动进入长期 Memory；
- 理解 Memory Retrieval 与 RAG Retrieval 的区别。

## 2. 专业名词通义

- **Memory Write Policy**：决定什么信息可以进入长期记忆的规则。
- **TTL（Time To Live）**：一条 Memory 可以有效多久。
- **Provenance**：来源信息，记录这条记忆来自用户、系统、工具还是外部网页。
- **Memory Poisoning**：恶意内容被持久化后，在后续多个任务中持续影响 Agent。
- **Conflict Resolution**：新旧记忆矛盾时选择覆盖、并存或人工确认的策略。

## 3. 运行

```bash
cd labs/10-memory-engineering
python app.py
```

实验使用 SQLite `:memory:`，不需要外部数据库。

## 4. 核心数据模型

```text
MemoryRecord
├─ namespace
├─ key
├─ value
├─ memory_type
├─ source
├─ trust_level
├─ version
├─ created_at
└─ expires_at
```

## 5. 写入策略

示例规则：

```text
User explicit preference      → allow
Verified internal tool result → allow
System-derived stable fact    → allow
Untrusted web content         → deny
Arbitrary model guess         → deny
```

这比 Prompt 里写“请只记住重要信息”可靠得多。

## 6. 实验任务

1. 写入用户显式偏好；
2. 尝试写入不可信网页中的“管理员密码”，确认拒绝；
3. 写入同一个 Key 的新版本；
4. 查询时只返回未过期记录；
5. 修改 TTL，观察过期行为。

## 7. 生产化延伸

真实项目还需要：

- Tenant / User Namespace；
- Encryption；
- PII 分类；
- Right to Delete；
- Memory Review UI；
- Embedding / Semantic Retrieval；
- Consolidation；
- Conflict / Confidence；
- Audit。

## 8. 验收标准

- [ ] Memory Write 经过 Policy；
- [ ] 不可信来源无法直接写长期 Memory；
- [ ] 记录有 Provenance；
- [ ] 支持 TTL；
- [ ] 支持 Version；
- [ ] 同一 Key 冲突行为明确；
- [ ] 能解释 Memory 与 RAG 的差异。
