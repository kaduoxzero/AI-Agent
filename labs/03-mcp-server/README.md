# Lab 03｜MCP Server：从 Tool 函数到标准化能力服务

> 目标：使用当前 MCP Python SDK v2 构建一个可被标准 MCP Client/Host 调用的能力服务，并通过 in-memory Client 做自动化测试。

## 1. 学习目标

完成后应能够：

- 理解 MCP Server、Tool、Resource 的职责；
- 使用 `MCPServer` 定义 Tool 和 Resource；
- 使用 MCP Client 进行无网络集成测试；
- 理解 Tool 业务函数与 MCP 协议层的边界；
- 知道生产部署还需要认证、Host Allowlist、Trace、限流与多 Worker 策略。

## 2. 专业名词通义

- **MCP Server**：把 Tool / Resource 等能力按 MCP 协议暴露出去的服务。
- **Host**：真正运行 Agent / AI 应用并连接 MCP Server 的宿主应用。
- **Resource**：可读取的上下文资源，不等同于会执行副作用的 Tool。
- **In-memory Client**：测试时直接连接 Python Server 对象，不启动端口和子进程。

## 3. 环境

MCP Python SDK 当前稳定线为 v2，要求 Python 3.10+。

```bash
cd labs/03-mcp-server
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 4. 运行 Server

开发模式：

```bash
mcp dev server.py
```

也可以在代码中挂载为 ASGI / Streamable HTTP 服务。真实生产不要只把开发模式直接暴露到公网。

## 5. 运行测试

```bash
pytest -q
```

测试使用 MCP SDK 的 `Client(mcp)` 直接连接 Server 对象，因此：

- 不占用端口；
- 不需要启动 subprocess；
- 适合 CI；
- 可以验证 Tool 契约。

## 6. 本实验提供的能力

```text
Tools
├─ get_supplier_risk(supplier_id)
└─ calculate_risk_score(delays, incidents)

Resources
└─ supplier://{supplier_id}
```

## 7. 生产化思考

实验完成后请继续回答：

```text
谁可以连接这个 MCP Server？
Server 如何知道调用者是谁？
不同 Agent 是否应该看到相同 Tool？
Write Tool 是否需要 Approval？
Tool 失败是否可安全重试？
多 Worker 如何共享状态？
Trace 如何导出？
```

MCP 只负责标准化协议，不会替你解决全部业务治理问题。

## 8. 验收标准

- [ ] Inspector 能列出 Tool；
- [ ] Tool 参数由类型提示生成 Schema；
- [ ] Resource 可以读取；
- [ ] `pytest` 能通过 in-memory Client 调 Tool；
- [ ] 能解释 MCP Tool 与普通 Python Function 的边界；
- [ ] 能解释为什么生产环境还需要 Auth / Policy / Audit。
