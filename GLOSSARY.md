# Agent Engineering 专业名词速查

> 本词典用于快速消除概念混淆。详细原理请进入对应章节。

| 术语 | 中文 / 通义 | 工程含义 |
|---|---|---|
| LLM | 大语言模型 | Agent 的主要推理模型 |
| Reasoning Model | 推理模型 | 更适合复杂规划、代码、逻辑任务的模型 |
| Token | 模型文本计量单位 | 影响上下文、成本和限额 |
| Context Window | 上下文窗口 | 一次模型调用能处理的信息范围 |
| Agent | 智能体 | 模型 + 指令 + 工具 + 运行行为 |
| Agent Loop | 智能体循环 | Model → Action → Observation → Next Step |
| Workflow | 工作流 | 主要由程序定义执行路径 |
| Agentic Workflow | 智能体式工作流 | 部分控制流由模型动态决定 |
| Orchestration | 编排 | 组织 Agent、Tool、Function 的执行关系 |
| Runtime | 运行时 | 执行 Agent Loop、状态、工具、恢复等能力 |
| Runner | 执行器 | 发起和管理 Agent Run |
| Harness | 智能体工程外壳 | Plan、Todo、Compaction、文件、权限、观测等长任务能力 |
| Prompt | 提示词 | 给模型的指令 |
| Context | 上下文 | 当前模型调用实际可见的信息 |
| State | 状态 | 工作流运行中持久 / 临时结构化数据 |
| Session | 会话 | 关联一系列交互和状态的逻辑范围 |
| Memory | 记忆 | 跨步骤或跨会话可再次使用的信息 |
| Compaction | 上下文压缩 | 将长历史压缩为继续工作所需的信息 |
| Structured Output | 结构化输出 | 按 JSON Schema / 类型生成机器可解析结果 |
| Tool | 工具 | Agent 可调用的外部执行能力 |
| Function Calling | 函数调用 | 模型按函数 Schema 产生结构化调用 |
| Side Effect | 副作用 | Tool 改变外部系统状态 |
| Idempotency | 幂等 | 重复请求不会造成重复副作用 |
| MCP | Model Context Protocol | Agent / AI 应用连接 Tool、Resource 的标准协议 |
| MCP Server | MCP 服务 | 通过 MCP 暴露 Tool / Resource 等能力 |
| Skill | 技能包 | 按需加载的专业规则、资源、脚本和工作方法 |
| Capability Registry | 能力注册表 | 管理 Agent、Skill、Tool 等能力元数据 |
| RAG | 检索增强生成 | 检索外部资料后再生成 |
| Agentic RAG | 智能体式 RAG | Agent 自主决定检索、重写和多轮查找 |
| Embedding | 向量表示 | 将语义映射到向量用于检索 |
| Vector DB | 向量数据库 | 存储 / 检索向量 |
| BM25 | 稀疏文本检索算法 | 适合关键词、编号等精确文本搜索 |
| Hybrid Search | 混合搜索 | Dense + Sparse Retrieval |
| Rerank | 重排序 | 对召回文档再次精排 |
| Chunk | 文档分块 | RAG 的检索粒度 |
| Evidence | 证据 | Agent 决策 / 回答依赖的可追溯事实 |
| ReAct | 推理 + 行动 | Reason → Action → Observation 循环 |
| Plan & Solve | 先规划后执行 | Planner 生成计划，Executor 执行 |
| ReWOO | 推理与观察解耦 | 先规划 Evidence / Tool，再集中求解 |
| LLMCompiler | LLM 任务编译思想 | 构造依赖图并并行执行 Tool |
| Reflection | 反思 | 生成后自检修正 |
| Reflexion | 语言强化式反思 | 使用外部反馈和 Episodic Memory 改进下一次尝试 |
| Evaluator-Optimizer | 评估-优化循环 | Generator 与 Evaluator 反复迭代 |
| LATS | Language Agent Tree Search | 多候选路径树搜索式 Agent |
| STORM | 研究 / 长文 Pattern | 多视角检索、知识组织、Outline 与写作 |
| Router | 路由器 | 决定下一 Node / Agent |
| Planner | 规划器 | 将目标拆成可执行任务 |
| Worker | 执行者 | 完成边界明确的子任务 |
| Supervisor | 主管 Agent | 中央调度多个 Agent |
| Handoff | 移交 | 将任务控制权交给另一个 Agent |
| Blackboard | 黑板模式 | 多 Agent 通过共享 State 协作 |
| Swarm | 蜂群 / 去中心化协作 | Agent 自主选择协作对象 |
| A2A | Agent2Agent Protocol | 独立 Agent 系统之间的互操作协议 |
| Agent Card | Agent 能力卡 | A2A 中描述远程 Agent 能力和连接信息 |
| Artifact | 任务产物 | 报告、文件、代码等稳定输出 |
| Checkpoint | 状态快照 | 用于恢复、HITL、调试 |
| Persistence | 持久化 | 将运行状态保存到耐久存储 |
| HITL | Human-in-the-Loop | 关键步骤由真人审核 / 输入 |
| Guardrail | 护栏 | 输入、输出、Tool 的验证 / 限制机制 |
| Sandbox | 沙箱 | 隔离 Shell、文件和代码执行环境 |
| Snapshot | 快照 | 保存某一时刻 Workspace 状态 |
| Browser Agent | 浏览器智能体 | 能观察并操作网页应用的 Agent |
| Computer Use | 电脑操作 | Agent 操作屏幕、鼠标、键盘等环境 |
| SSE | 服务端事件 | 单向流式推送协议 |
| WebSocket | 双向长连接 | Realtime / 高频双向事件常用 |
| WebRTC | 实时通信协议 | 浏览器低延迟音视频常用 |
| STT | 语音转文字 | Speech-to-Text |
| TTS | 文字转语音 | Text-to-Speech |
| VAD | 语音活动检测 | 判断用户开始 / 停止说话 |
| Barge-in | 插话中断 | 用户打断 Agent 正在播放的语音 |
| Eval | 评估 | 衡量 Agent 质量、行为和系统指标 |
| Golden Dataset | 黄金测试集 | 代表真实业务的固定评估数据 |
| LLM-as-a-Judge | 模型评审 | 用模型按 Rubric 评价输出 |
| Trajectory | 执行轨迹 | Agent 从输入到最终结果走过的动作路径 |
| Regression | 回归测试 | 修改后检查旧能力是否退化 |
| Red Team | 红队测试 | 主动使用对抗方式发现安全问题 |
| Trace | 链路 | 一次完整 Agent Task 的执行记录 |
| Span | 链路片段 | Trace 中单个 Model / Tool / Node 操作 |
| Observability | 可观测性 | Trace + Log + Metrics 等理解系统行为的能力 |
| Prompt Injection | 提示注入 | 恶意输入试图改变 Agent 指令层级 |
| Memory Poisoning | 记忆投毒 | 恶意内容进入长期 Memory 并持续影响行为 |
| Least Privilege | 最小权限 | Agent 只拥有任务必须的能力 |
| RBAC | 基于角色权限 | Role-Based Access Control |
| ABAC | 基于属性权限 | Attribute-Based Access Control |
| Audit | 审计 | 记录谁代表谁执行了什么操作 |
| Tenant Isolation | 租户隔离 | 不同客户数据 / 状态 / 缓存互不泄漏 |
| Queue | 消息队列 | 长任务异步调度与削峰 |
| Dead Letter | 死信 | 多次失败后单独保存待处理任务 |
| Backpressure | 背压 | 下游繁忙时限制上游继续产生任务 |
| Rate Limit | 限流 | 控制请求 / Token / 并发速率 |
| Model Routing | 模型路由 | 按任务选择不同能力 / 成本模型 |
| Fallback | 降级 / 备用 | 主模型 / Tool 失败后切换备用方案 |
| Canary | 金丝雀发布 | 小流量验证新版本 |
| Eval Gate | 评估门禁 | Eval 不达标阻止部署 |
