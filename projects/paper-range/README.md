# Paper Range / 纸上靶场

Paper Range 是 AI-Agent 仓库里的叙事式安全推演实验场。用户的自然语言或“命令”会被映射为 **Typed Action Contract → Simulated Runtime → WorldState → Story Graph → Narrative/Event → UI**。所有目标、服务、目录、凭据和结果都由模拟器生成，不向真实网络发包。

## 当前版本

当前后端 API 版本：**0.5.0 / Live Story UI**

本版本在 Story Graph v1 上新增：

- 前端 Story Graph 节点可视化；
- `focused` / `broad` 显式分支选择控件；
- World Tags / Consequences 可视化；
- `GET /api/sessions/{session_id}/events` SSE 事件流；
- EventSource 重连游标和 `Last-Event-ID` 支持；
- Agent / Narrative / Reward 事件逐条推送到终端和 Live Intel；
- Nginx 为 SSE 关闭 buffering，并延长流式连接读取超时。

SSE 只读取当前进程内的 `GameEvent`。它不会新增数据库、Redis、宿主机持久化，也不会向真实目标发送请求。

## 当前可玩链路

```text
选择 / 随机战役
  ↓
创建临时 Session + 随机 Theme Pack
  ↓
端口侦察
  ↓
Web 初查
  ↓
Story Graph：调查方式选择
  ├─ focused：定向、低噪声、只优先暴露高置信度证据路径
  └─ broad：广覆盖、更多可见路径、产生 noisy-enumeration Consequence（-3 分）
  ↓
隐藏路径枚举
  ↓
证据文件读取
  ↓
模拟 SSH 验证
  ↓
Flag + 学习报告
```

用户既可以输入自然语言，也可以输入看起来像命令的文本；这些字符串只会被解析为 Typed Intent，不会交给系统 shell：

```text
nmap -p- <scene-target>              → scan_ports
curl http://<scene-target>           → inspect_web
approach focused                     → select_approach(focused)
approach broad                       → select_approach(broad)
dirsearch -u http://<scene-target>   → enumerate_paths
cat /discovered/evidence             → inspect_file
ssh user@<scene-target>              → ssh_access
```

自然语言示例：

```text
我先扫描所有 TCP 端口
检查一下 Web 服务
我选择低噪声调查
枚举隐藏目录
读取刚才发现的证据文件
用发现的训练身份登录主机
```

## Story Graph / WorldState

每个 Session 维护轻量 Story Graph：

```text
recon
  ↓
web-investigation
  ↓
approach-decision
  ├─ focused → path-enumeration
  └─ broad   → path-enumeration
  ↓
evidence-review
  ↓
access-validation
  ↓
complete
```

前端会直接标出当前节点、已完成节点、锁定分支、World Tags 和不可回滚 Consequences。

WorldState 包含：

- `story_node`：当前剧情节点；
- `story_branch`：当前已锁定分支；
- `world_tags`：例如 `ephemeral-world`、`simulation-only`、`low-noise-recon`、`noisy-enumeration`；
- `consequences`：当前局已经发生、不可回滚的剧情后果。

`focused` 不扣分，写入 `low-noise-recon`，路径枚举只优先显示高置信度证据路径。`broad` 扣 3 分，写入 `noisy-enumeration`，会展示当前场景的全部隐藏路径。分支一旦写入 WorldState，就不能在同一 Session 中改写。直接跳过选择继续枚举时默认锁定 `focused`，保持旧命令链兼容。

## SSE Live Event Stream

浏览器连接：

```text
GET /api/sessions/{session_id}/events?after=<event-seq>
Accept: text/event-stream
```

`GameEvent.seq` 同时作为 SSE `id`：

```text
id: 12
event: game_event
data: {"seq":12,"kind":"agent","text":"..."}
```

浏览器重连时可通过 `Last-Event-ID` 继续消费未显示事件。服务端会发送 heartbeat；Session 完成时发送 `session_complete` 控制事件并结束该流。Action HTTP 响应负责更新 WorldState，SSE 负责事件演出，两者共享同一个进程内临时 Session。

## 场景

当前包含 6 个虚构战役：

- `废弃研究所`：Web / Linux 入门；
- `企业内网残影`：服务发现 / 内网剧情；
- `地下交易市场`：叙事侦察 / Web；
- `市政档案馆断电夜`：Web / Evidence Trail；
- `轨道中继站静默协议`：Ops / Telemetry；
- `赤港夜班货运站`：Industrial / Narrative Ops。

每个战役目前有 5 个核心 Objective：扫描开放端口、调查 Web、枚举隐藏路径、读取证据、建立模拟访问。Story Graph 分支选择属于 WorldState 决策节点，不单独计为 Objective。

## Theme Pack

每个新 Session 会从注册表随机选择 Theme Pack。当前已有 12 套：

`inferno`、`blood-moon`、`black-site`、`ash-cathedral`、`neon-crypt`、`reactor-amber`、`plague-green`、`ice-vault`、`violet-null`、`rust-foundry`、`signal-blue`、`obsidian-gold`。

Theme Pack 通过共享 CSS variables 控制 Shell、Panel、Terminal、Agent、Story Graph、进度条和完成界面。最终目标仍是 40 套。

## 剧情秘密边界

`GET /api/scenarios` 只返回公开战役元数据。隐藏路径、Web 观察正文、证据文件正文、训练密码和最终 Flag 都保留在后端完整 `Scenario` 中。当前 UI 为了显示模拟 SSH 快捷提示仍会得到剧情用户名，但密码和完成条件不会提前暴露。

## Session 生命周期

```text
container start
  ↓
全新的 SessionStore
  ↓
本次运行持续复用 WorldState / Story Graph / Clue / Event / Score / Theme
  ↓
SSE 只读取当前 Session 的 GameEvent
  ↓
container stop/remove
  ↓
内存状态消失
  ↓
下一次启动 = 新世界
```

当前不写 PostgreSQL、不写 Redis、不写宿主机文件，`docker-compose.yml` 不挂载游戏数据卷；后端容器重启即丢失全部游戏 Session。

## 一键启动

```bash
cd projects/paper-range
docker compose up --build
```

打开 `http://127.0.0.1:8080`，健康检查为 `http://127.0.0.1:8080/health`。

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
GET    /api/sessions/{session_id}/events
POST   /api/sessions/{session_id}/actions
POST   /api/sessions/{session_id}/hint
GET    /api/sessions/{session_id}/report
DELETE /api/sessions/{session_id}
```

## 学习循环

每个 Session 记录 Score、Action/Hint/Invalid Count、Objective、Story Node/Branch、World Tags/Consequences、Clue/Event，以及最终 Grade 和学习报告。Hint 每次扣 10 分；`broad` 分支扣 3 分；无效动作和场景外目标会扣少量分。场景外 IP 始终 fail-closed，Runtime 只接受当前虚构 Scenario 注册的目标。

## AI-Agent Skill 集成

仓库已经注册 `agent-paper-range-designer`，用于设计 Paper Range 的 simulation-only Scenario / Action / WorldState / Story / Learning / Theme contracts，并由 Master / Project Orchestrator 路由相关任务。

## 下一阶段

1. 将 12 套 Theme Pack 扩展到最终目标 40 套，并增加场景/主题匹配权重；
2. 增加更多 simulation-only 工具动作，例如 HTTP 变体、日志检索、资产关系调查；
3. Story Graph v2：多层分支、条件节点、可组合 Consequence；
4. E2E 浏览器测试、SSE 断线重连测试和 Docker smoke test；
5. 场景生成器与难度/评分策略进一步数据化。
