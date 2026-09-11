# Paper Range / 纸上靶场

Paper Range 是 AI-Agent 仓库里的叙事式安全推演实验场。它不是把真实扫描器包装进网页，而是把用户的自然语言/命令映射成 **Typed Action Contract → Simulated Runtime → WorldState → Narrative/Event → UI**。所有目标、服务、目录、凭据和结果都由模拟器生成，不向真实网络发包。

## 当前可玩链路

```text
选择 / 随机战役
  ↓
创建临时 Session
  ↓
端口侦察
  ↓
Web 初查
  ↓
隐藏路径枚举
  ↓
证据文件读取
  ↓
模拟 SSH 验证
  ↓
Flag + 学习报告
```

用户可以输入自然语言，也可以输入“看起来像命令”的文本；这些字符串只会被解析为 Typed Intent，不会交给系统 shell：

```text
nmap -p- <scene-target>              → scan_ports
curl http://<scene-target>           → inspect_web
dirsearch -u http://<scene-target>   → enumerate_paths
cat /discovered/evidence             → inspect_file
ssh user@<scene-target>               → ssh_access
```

自然语言示例：

```text
我先扫描所有 TCP 端口
检查一下 Web 服务
枚举隐藏目录
读取刚才发现的证据文件
用发现的训练身份登录主机
```

## 场景

当前包含 6 个虚构战役：

- `废弃研究所`：Web / Linux 入门；
- `企业内网残影`：服务发现 / 内网剧情；
- `地下交易市场`：叙事侦察 / Web；
- `市政档案馆断电夜`：Web / Evidence Trail；
- `轨道中继站静默协议`：Ops / Telemetry；
- `赤港夜班货运站`：Industrial / Narrative Ops。

每个战役目前都有 5 个核心 Objective：

1. 扫描开放端口；
2. 调查 Web 服务；
3. 枚举隐藏路径；
4. 读取证据文件；
5. 建立模拟访问。

## 剧情秘密边界

`GET /api/scenarios` 只返回前端需要的公开战役元数据。以下信息保留在后端完整 `Scenario` 中，不会在进入战役前下发给浏览器：

- 隐藏路径；
- Web 观察正文；
- 证据文件正文；
- 训练密码；
- 最终 Flag。

当前 UI 为了显示模拟 SSH 快捷提示，仍会得到剧情用户名；密码和完成条件不会提前暴露。

## Session 生命周期

```text
container start
  ↓
全新的 SessionStore
  ↓
本次运行期间持续复用 WorldState / Clue / Event / Score
  ↓
container stop/remove
  ↓
内存状态消失
  ↓
下一次启动 = 新世界
```

当前实现：

- 不写 PostgreSQL；
- 不写 Redis；
- 不写宿主机文件；
- `docker-compose.yml` 不挂载游戏数据卷；
- 后端容器重启即丢失全部游戏 Session。

## 一键启动

从仓库根目录：

```bash
cd projects/paper-range
docker compose up --build
```

打开：

```text
http://127.0.0.1:8080
```

健康检查：

```text
http://127.0.0.1:8080/health
```

## 本地开发

后端：

```bash
cd projects/paper-range/backend
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
uvicorn app.main:app --reload --port 8000
```

前端：

```bash
cd projects/paper-range/frontend
npm install
npm run dev
```

Vite 会把 `/api` 代理到 `127.0.0.1:8000`。

## API

```text
GET    /health
GET    /api/scenarios
POST   /api/sessions
GET    /api/sessions/{session_id}
POST   /api/sessions/{session_id}/actions
POST   /api/sessions/{session_id}/hint
GET    /api/sessions/{session_id}/report
DELETE /api/sessions/{session_id}
```

创建随机战役：

```json
{}
```

创建指定战役：

```json
{
  "scenario_id": "abandoned-lab"
}
```

执行动作：

```json
{
  "input": "枚举隐藏目录"
}
```

## 学习循环

每个 Session 记录：

- Score；
- Action Count；
- Hint Count；
- Invalid Action Count；
- 完成 Objective；
- Clue / Event；
- 最终 Grade 与学习报告。

Hint 每次扣 10 分；无效动作和场景外目标会扣少量分。场景外 IP 会 fail-closed，Runtime 只接受当前虚构 Scenario 注册的目标。

## AI-Agent Skill 集成

仓库已经注册 `agent-paper-range-designer`，用于设计 Paper Range 的 simulation-only Scenario / Action / WorldState / Story / Learning / Theme contracts，并由 Master / Project Orchestrator 路由相关任务。

## 下一阶段

当前重点已经从“能不能玩”转向“内容规模和表现力”：

1. Theme Pack 注册机制，从 3 套扩展到 10+，最终目标 40 套；
2. Story Graph / Branch / Consequence，让不同动作改变剧情路径；
3. SSE / WebSocket 事件流，让 Agent、剧情和终端反馈逐步出现；
4. 增加更多 simulation-only 工具动作，例如 HTTP 变体、日志检索、资产关系调查；
5. E2E 浏览器测试和 Docker smoke test；
6. 场景生成器与难度/评分策略进一步数据化。
