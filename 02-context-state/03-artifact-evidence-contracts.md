# Agent Artifact、Evidence 与数据契约工程

> 目标：让 Agent 之间不再依赖大段自然语言“聊天式协作”，而是通过可验证、可持久化、可测试的结构化产物协作。

## 1. 为什么自然语言协作不够

Multi-Agent Demo 常见：

```text
Research Agent：我查了一些资料，我认为……
 ↓
Risk Agent：根据你的描述，我认为……
```

问题：

- 信息难以验证；
- 来源丢失；
- 无法稳定测试；
- Retry 时不知道哪些结果可以复用；
- Agent 间上下文越来越大；
- Schema 演进困难；
- Trace 只能看到文本，无法做自动质量检查。

生产系统应尽量升级为：

```text
Agent → Typed Artifact → Agent
```

## 2. 专业名词通义

- **Artifact（产物）**：Agent 执行过程中或最终生成的可独立保存成果，例如 Report、CodePatch、Plan、CSV、EvidenceSet。
- **Evidence（证据）**：支持某个 Claim 的可追溯信息，必须能够定位来源。
- **Claim（主张）**：Agent 输出中需要被事实支持的结论。
- **Data Contract（数据契约）**：模块之间约定的字段、类型、语义、版本和兼容规则。
- **Provenance（来源血缘）**：数据从哪里来、何时获得、经过哪些处理。

## 3. Artifact 设计原则

一个好 Artifact 应尽可能：

```text
Typed
Versioned
Serializable
Persistable
Traceable
Validatable
Composable
```

例如：

```python
class ResearchArtifact(BaseModel):
    schema_version: str
    task_id: str
    query: str
    evidence: list[Evidence]
    gaps: list[str]
    created_at: datetime
```

## 4. Evidence Schema

推荐：

```python
class Evidence(BaseModel):
    id: str
    claim: str
    source_type: Literal["web", "kb", "db", "tool"]
    source_uri: str | None
    source_id: str | None
    excerpt: str | None
    observed_at: datetime
    confidence: float | None
    tenant_id: str | None
```

注意：`confidence` 不能代替真实 Citation。

## 5. Claim 与 Evidence 分离

错误：

```json
{"analysis": "供应商风险很高，因为新闻很多"}
```

推荐：

```json
{
  "claims": [
    {
      "id": "c1",
      "text": "过去 30 天出现 3 次交付异常",
      "evidence_ids": ["e1", "e2", "e3"]
    }
  ]
}
```

Reviewer 可以自动验证：

```text
每个高影响 Claim 是否都有 Evidence？
Evidence 是否存在？
Citation 是否仍可访问？
Claim 是否超出 Evidence 支持范围？
```

## 6. Plan 也应是 Artifact

不要只保存 Planner 的自然语言：

```text
第一步查资料，第二步……
```

推荐 Task DAG：

```python
class PlanNode(BaseModel):
    id: str
    type: str
    agent: str
    depends_on: list[str]
    status: str
    input_refs: list[str]
    output_ref: str | None
```

好处：

- 可以并行；
- 可以 Retry 单节点；
- 可以可视化；
- 可以 Eval；
- 可以 Resume。

## 7. ToolResult Contract

Tool 不要随意返回字符串。

错误：

```python
return "查到了 3 条数据"
```

推荐：

```python
class SupplierMetricsResult(BaseModel):
    supplier_id: str
    metrics: list[Metric]
    as_of: datetime
    source: str
    warnings: list[str]
```

LLM 可以消费结构化结果，确定性代码也能验证。

## 8. Schema Versioning

Artifact 必须考虑演进。

```json
{
  "schema_version": "2.1",
  "artifact_type": "risk_assessment"
}
```

原则：

- 新增可选字段优先保持向后兼容；
- 删除 / 重命名字段需要新版本；
- Runtime / Consumer 应明确支持的版本；
- 长任务 Checkpoint 可能跨版本恢复，需要 Migration。

## 9. Artifact Store

不要把所有产物塞 State。

推荐：

```text
State
 ├─ artifact_refs
 ├─ current_plan_ref
 └─ evidence_set_ref

Artifact Store
 ├─ report.json
 ├─ evidence.json
 ├─ result.csv
 └─ patch.diff
```

大文件放 Object Storage，数据库保存 Metadata 和 Reference。

## 10. Artifact 生命周期

```text
Created
 ↓
Validated
 ↓
Reviewed
 ↓
Approved / Rejected
 ↓
Published / Consumed
 ↓
Archived
```

对于高风险 Artifact，应记录：

```text
producer_agent
agent_version
model
prompt_version
reviewer
approval_id
trace_id
```

## 11. Multi-Agent 协作示例

```text
Research Agent
 ↓ ResearchArtifact
Evidence Store
 ↓
Risk Agent
 ↓ RiskAssessmentArtifact
Reviewer
 ↓ ReviewArtifact
HITL
 ↓ ApprovalArtifact
Report Generator
```

这样 Agent 之间交换“业务对象”，而不是不断转述历史消息。

## 12. Artifact 与 Memory 的区别

```text
Artifact：任务产物，强调可验证、可引用、可交付
Memory：用于后续推理的长期信息
State：当前 Run 的控制状态
Context：某一 Turn 输入模型的信息
```

不要自动把所有 Artifact 写进 Memory。

## 13. Artifact 与 Event 的区别

```text
Event：发生了什么
Artifact：产生了什么
```

例如：

```text
Event = ReportCreated(report_id=R1)
Artifact = R1 的真实报告内容
```

## 14. Eval

Artifact 让 Eval 更可靠：

```text
Schema Validity
Citation Coverage
Required Fields
Evidence Freshness
Business Rule
Diff / Regression
```

而不是所有评估都依赖 LLM-as-a-Judge。

## 15. 实训

把毕业项目所有 Worker 输出改为 Typed Artifact：

- Router → RoutingDecision；
- Planner → TaskPlan；
- Research → EvidenceSet；
- Data → DataSnapshot；
- Risk → RiskAssessment；
- Reviewer → ReviewResult；
- HITL → ApprovalDecision；
- Final → ReportArtifact。

要求 Agent State 中只保存 ID / Reference，不保存完整大对象。

## 16. 检查清单

- [ ] Agent 间核心协作是否有 Typed Artifact？
- [ ] Artifact 是否有 Schema Version？
- [ ] Evidence 是否可追溯？
- [ ] Claim 与 Evidence 是否建立明确映射？
- [ ] 大 Artifact 是否从 State 中分离？
- [ ] Retry 是否可以复用已验证 Artifact？
- [ ] Artifact 是否能被确定性 Eval？