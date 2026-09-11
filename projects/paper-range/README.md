# Paper Range / 纸上靶场

Paper Range 是 AI-Agent 仓库里的叙事式安全推演实验场。它不是把真实扫描器包装进网页，而是把用户的自然语言/命令映射成 **Action Contract → WorldState → Narrative/Event → UI**，所有网络目标和结果都由模拟器生成。

## 当前 MVP Vertical Slice

已经打通：

```text
选择/随机战役
  ↓
创建临时 Session
  ↓
输入自然语言或模拟命令
  ↓
Action Classifier
  ↓
Simulated Tool Runtime
  ↓
WorldState / Objective / Clue 更新
  ↓
React UI 实时展示
  ↓
完成任务并获得 Flag
```

当前包含 3 个虚构战役：

- `废弃研究所`：Web / Linux 入门；
- `企业内网残影`：服务发现 / 内网剧情；
- `地下交易市场`：叙事侦察 / Web。

当前实现的模拟动作：

- `nmap -p- <scene-target>` / “扫描所有 TCP 端口”；
- `curl http://<scene-target>` / “调查 Web 服务”；
- `ssh <story-user>@<scene-target>` / “登录主机”；
- `status` / `help`。

> 这些动作不会调用系统 `nmap`、`curl`、`ssh`，也不会向网络发包。输入场景之外的 IP 会被 Runtime 拒绝。

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

## Session 生命周期

这是本项目必须保持的语义：

```text
container start
  ↓
全新的 SessionStore
  ↓
本次运行期间持续复用 WorldState / Clue / Event
  ↓
container stop/remove
  ↓
内存状态消失
  ↓
下一次启动 = 新世界
```

实现上当前使用 `SessionStore` 进程内字典：

- 不写 PostgreSQL；
- 不写 Redis；
- 不写宿主机文件；
- `docker-compose.yml` 不挂载数据卷；
- 后端容器重启即丢失全部游戏 Session。

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
  "input": "我先扫描所有 TCP 端口"
}
```

## 当前边界与下一步

这一版的目标是验证核心玩法闭环，不是一次性完成 40 套主题。下一阶段优先级：

1. 把 Action Classifier 从规则路由升级为结构化 Agent Intent Parser；
2. 增加目录枚举、HTTP 请求变体、文件/日志调查、模拟凭据与权限状态；
3. 增加 Story Graph、Branch/Consequence、Hint、评分与复盘；
4. 将 3 个 CSS Theme 扩展为可注册的 Theme Pack，并逐步增加到 40 套；
5. 加入 SSE/WebSocket 事件流；
6. 增加 E2E 测试与 Docker smoke test；
7. 把 Paper Range 注册到 AI-Agent Skill/Project Orchestrator，形成可发现能力。
