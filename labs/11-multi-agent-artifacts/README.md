# Lab 11｜Multi-Agent + Typed Artifact：从“Agent 聊天”到数据契约协作

> 目标：构建一个小型 Supervisor + Research + Data + Reviewer 系统，Agent 之间不传整段聊天历史，而是通过 Typed Artifact 协作。

## 1. 学习目标

完成后应能够：

- 明确每个 Agent 的职责边界；
- 让 Research / Data Worker 并行执行；
- 使用 Pydantic 定义 EvidenceSet / DataSnapshot / ReviewResult；
- 由 Supervisor 控制最大 Worker 和最大步骤；
- 避免 Worker 之间直接共享全部 Context；
- 理解 Typed Artifact 对测试、持久化和版本化的价值。

## 2. 专业名词通义

- **Typed Artifact**：有明确 Schema 的 Agent 任务产物，例如 EvidenceSet、CodePatch、RiskAssessment。
- **Supervisor**：负责拆任务、调 Worker、合并结果的上层控制器。
- **Context Isolation**：每个 Agent 只看到完成职责所需的信息，而不是共享全部会话历史。
- **Fan-out / Fan-in**：一个任务并行分发给多个 Worker，再把结果聚合回来。

## 3. 运行

```bash
cd labs/11-multi-agent-artifacts
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## 4. 架构

```text
                  Supervisor
                  /        \
                 ↓          ↓
          ResearchWorker  DataWorker
                 ↓          ↓
           EvidenceSet   DataSnapshot
                  \        /
                   ↓      ↓
                    Reviewer
                       ↓
                  ReviewResult
```

## 5. 为什么不用自然语言互传

错误示例：

```text
Research Agent：我查了这些……
Data Agent：我感觉……
Reviewer：结合大家刚才说的……
```

问题：

- 无法稳定解析；
- 难做 Schema Validation；
- 难持久化；
- 难重放；
- 难做版本迁移；
- 难做 Trajectory Eval。

推荐：

```text
Research → EvidenceSet
Data → DataSnapshot
Reviewer → ReviewResult
```

## 6. 实验任务

1. 正常并行执行 Research/Data；
2. 修改 Worker 返回非法字段，观察 Schema 校验；
3. 把 `max_workers` 降为 1，观察 Runtime 拒绝；
4. 增加第二个 Reviewer；
5. 为 Artifact 增加 `schema_version`。

## 7. 验收标准

- [ ] Worker 职责不同；
- [ ] Worker 不共享全部历史；
- [ ] Agent 之间通过 Typed Artifact 协作；
- [ ] Supervisor 有 max_workers / max_steps；
- [ ] Artifact 可 JSON 序列化；
- [ ] Reviewer 可以独立测试；
- [ ] 能说明什么时候应该使用 Multi-Agent，什么时候不应该拆。
