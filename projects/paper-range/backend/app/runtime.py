from __future__ import annotations

import random
import shlex
from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4

from .intent import IntentParser
from .models import ActionResponse, GameEvent, GameSessionView, HintResponse, LearningReport, PortService, Scenario
from .scenarios import SCENARIOS


THEMES = ["inferno", "blood-moon", "black-site"]
HINT_COST = 10


@dataclass
class GameSession:
    id: str
    scenario: Scenario
    theme_id: str
    created_at: datetime
    status: str = "active"
    objective_index: int = 0
    completed_objectives: list[str] = field(default_factory=list)
    clues: list[str] = field(default_factory=list)
    discovered_services: list[PortService] = field(default_factory=list)
    events: list[GameEvent] = field(default_factory=list)
    score: int = 100
    action_count: int = 0
    hint_count: int = 0
    invalid_action_count: int = 0
    flag: str | None = None
    completed_at: datetime | None = None

    def emit(self, kind: str, text: str) -> None:
        self.events.append(GameEvent(seq=len(self.events) + 1, kind=kind, text=text))

    def view(self) -> GameSessionView:
        return GameSessionView(
            id=self.id,
            scenario_id=self.scenario.id,
            scenario_name=self.scenario.name,
            theme_id=self.theme_id,
            target_ip=self.scenario.target_ip,
            created_at=self.created_at.isoformat(),
            status=self.status,
            objective_index=self.objective_index,
            completed_objectives=list(self.completed_objectives),
            clues=list(self.clues),
            discovered_services=list(self.discovered_services),
            events=list(self.events),
            score=self.score,
            action_count=self.action_count,
            hint_count=self.hint_count,
            invalid_action_count=self.invalid_action_count,
            flag=self.flag,
        )


class SessionStore:
    """Process-local game memory.

    No session is written to disk or an external database. Destroying/restarting the
    backend container creates a completely new store and therefore a new memory.
    """

    def __init__(self) -> None:
        self._sessions: dict[str, GameSession] = {}

    def create(self, scenario_id: str | None = None) -> GameSession:
        if scenario_id is None:
            scenario = random.choice(list(SCENARIOS.values()))
        else:
            try:
                scenario = SCENARIOS[scenario_id]
            except KeyError as exc:
                raise ValueError(f"unknown scenario: {scenario_id}") from exc

        session = GameSession(
            id=str(uuid4()),
            scenario=scenario,
            theme_id=random.choice(THEMES),
            created_at=datetime.now(UTC),
        )
        session.emit("system", f"新会话已创建：{scenario.name}。本局记忆仅存在于当前运行中的容器进程。")
        session.emit("narrative", scenario.intro)
        session.emit("agent", f"任务：{scenario.briefing}")
        self._sessions[session.id] = session
        return session

    def get(self, session_id: str) -> GameSession:
        try:
            return self._sessions[session_id]
        except KeyError as exc:
            raise KeyError("session not found") from exc

    def delete(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)

    def count(self) -> int:
        return len(self._sessions)


class GameRuntime:
    def __init__(self, store: SessionStore | None = None, intent_parser: IntentParser | None = None) -> None:
        self.store = store or SessionStore()
        self.intent_parser = intent_parser or IntentParser()

    def execute(self, session_id: str, raw_input: str) -> ActionResponse:
        session = self.store.get(session_id)
        intent = self.intent_parser.parse(raw_input)
        session.action_count += 1
        session.emit("tool", f"> {intent.raw_input}")

        if session.status == "completed":
            return ActionResponse(
                intent=intent,
                output="本战役已经完成。可以查看学习报告，或创建一个新会话开始新的世界。",
                session=session.view(),
            )

        if intent.kind == "scan_ports":
            output = self._scan_ports(session, intent.target)
        elif intent.kind == "inspect_web":
            output = self._inspect_web(session, intent.target)
        elif intent.kind == "ssh_access":
            output = self._ssh_access(session, intent.raw_input)
        elif intent.kind == "status":
            output = self._status(session)
        elif intent.kind == "help":
            output = self._help(session)
        else:
            output = self._unknown(session, intent.raw_input)

        return ActionResponse(intent=intent, output=output, session=session.view())

    def request_hint(self, session_id: str) -> HintResponse:
        session = self.store.get(session_id)
        if session.status == "completed":
            return HintResponse(hint="战役已经完成。现在更适合查看学习报告。", cost=0, session=session.view())

        hint_index = min(session.objective_index, len(session.scenario.hints) - 1)
        hint = session.scenario.hints[hint_index]
        session.hint_count += 1
        session.score = max(0, session.score - HINT_COST)
        session.emit("agent", f"Hint (-{HINT_COST}): {hint}")
        return HintResponse(hint=hint, cost=HINT_COST, session=session.view())

    def report(self, session_id: str) -> LearningReport:
        session = self.store.get(session_id)
        grade = self._grade(session.score)
        strengths: list[str] = []
        next_steps: list[str] = []

        if session.hint_count == 0:
            strengths.append("没有使用 Hint，能够自主推进当前任务链。")
        else:
            strengths.append("能够利用 Hint 恢复任务方向并继续完成推演。")
        if session.invalid_action_count <= 1:
            strengths.append("行动路径较集中，较少出现与当前目标无关的尝试。")
        if session.status == "completed":
            strengths.append("完成了侦察 → Web 调查 → 模拟访问的完整证据链。")
        else:
            next_steps.append("完成剩余目标后再生成最终学习结论。")

        if session.hint_count > 0:
            next_steps.append("重玩同一场景一次，尝试不使用 Hint 完成相同步骤。")
        if session.invalid_action_count > 1:
            next_steps.append("执行动作前先对照当前 Objective，减少无效尝试。")
        next_steps.append("分别用自然语言和命令表达同一意图，观察它们如何映射到统一 Action Contract。")

        return LearningReport(
            session_id=session.id,
            scenario_name=session.scenario.name,
            status=session.status,
            score=session.score,
            grade=grade,
            action_count=session.action_count,
            hint_count=session.hint_count,
            invalid_action_count=session.invalid_action_count,
            completed_objectives=len(session.completed_objectives),
            total_objectives=len(session.scenario.objectives),
            strengths=strengths,
            next_steps=next_steps,
            flag=session.flag,
        )

    def _scan_ports(self, session: GameSession, target: str | None) -> str:
        resolved_target = target or session.scenario.target_ip
        if resolved_target != session.scenario.target_ip:
            return self._reject_external_target(session, resolved_target)

        session.discovered_services = list(session.scenario.services)
        if "scan" not in session.completed_objectives:
            session.completed_objectives.append("scan")
            session.objective_index = max(session.objective_index, 1)
            session.emit("reward", "目标完成：扫描开放端口。")

        lines = [f"SIMULATED NMAP {resolved_target}", "PORT      STATE  SERVICE       VERSION"]
        for service in session.scenario.services:
            lines.append(f"{service.port}/tcp   open   {service.service:<13} {service.version}")
        lines.append(f"扫描完成：发现 {len(session.scenario.services)} 个开放 TCP 端口。")
        output = "\n".join(lines)
        session.emit("agent", f"我记录了 {len(session.scenario.services)} 个服务。下一步可以检查 Web 服务，寻找剧情线索。")
        return output

    def _inspect_web(self, session: GameSession, target: str | None) -> str:
        resolved_target = target or session.scenario.target_ip
        if resolved_target != session.scenario.target_ip:
            return self._reject_external_target(session, resolved_target)
        if "scan" not in session.completed_objectives:
            text = "你还没有建立服务画像。先扫描目标会让调查更符合任务流程。"
            session.emit("agent", text)
            return text

        clue = session.scenario.web_clue
        if clue not in session.clues:
            session.clues.append(clue)
        if "web" not in session.completed_objectives:
            session.completed_objectives.append("web")
            session.objective_index = max(session.objective_index, 2)
            session.emit("reward", "目标完成：调查 Web 服务。")
        session.emit("narrative", "页面加载后，终端荧光映出一份没有被清理的值班记录。")
        session.emit("agent", "线索已加入证据栏。它包含一个只对本模拟世界有效的训练账户。")
        return f"HTTP/1.1 200 OK\nserver: paper-range-sim\n\n{clue}"

    def _ssh_access(self, session: GameSession, command: str) -> str:
        if "web" not in session.completed_objectives:
            text = "当前没有可验证的访问身份。先调查 Web 服务寻找剧情凭据。"
            session.emit("agent", text)
            return text

        try:
            args = shlex.split(command)
        except ValueError:
            args = []

        supplied_user = None
        supplied_password = None
        if args and args[0].lower() == "ssh":
            if len(args) > 1 and "@" in args[1]:
                supplied_user = args[1].split("@", 1)[0]
            if "--password" in args:
                index = args.index("--password")
                if index + 1 < len(args):
                    supplied_password = args[index + 1]

        if supplied_user and supplied_user != session.scenario.ssh_user:
            text = f"模拟 SSH 拒绝用户 {supplied_user}。证据栏里的训练账户可能更有用。"
            session.emit("agent", text)
            session.invalid_action_count += 1
            session.score = max(0, session.score - 1)
            return text
        if supplied_password and supplied_password != session.scenario.ssh_password:
            text = "模拟 SSH 认证失败。当前输入的训练口令与已发现线索不匹配。"
            session.emit("agent", text)
            session.invalid_action_count += 1
            session.score = max(0, session.score - 1)
            return text

        if "access" not in session.completed_objectives:
            session.completed_objectives.append("access")
        session.objective_index = len(session.scenario.objectives)
        session.status = "completed"
        session.flag = session.scenario.flag
        session.completed_at = datetime.now(UTC)
        session.emit("reward", "目标完成：建立模拟访问。")
        session.emit("narrative", "主机欢迎语闪过，封存事故的证据目录出现在屏幕上。战役结束。")
        session.emit("reward", f"MISSION COMPLETE — {session.flag}")
        return f"SIMULATED SSH ACCESS GRANTED\nuser={session.scenario.ssh_user}\nhost={session.scenario.target_ip}\n{session.flag}"

    @staticmethod
    def _status(session: GameSession) -> str:
        return (
            f"scenario={session.scenario.name}\n"
            f"status={session.status}\n"
            f"objectives={len(session.completed_objectives)}/{len(session.scenario.objectives)}\n"
            f"score={session.score}\n"
            f"actions={session.action_count}\n"
            f"hints={session.hint_count}\n"
            f"clues={len(session.clues)}"
        )

    @staticmethod
    def _help(session: GameSession) -> str:
        return (
            "可以直接用自然语言，也可以输入模拟命令：\n"
            f"nmap -p- {session.scenario.target_ip}\n"
            f"curl http://{session.scenario.target_ip}\n"
            f"ssh {session.scenario.ssh_user}@{session.scenario.target_ip}\n"
            "status\n"
            "也可以在任务面板请求 Hint（每次 -10 分）。"
        )

    def _unknown(self, session: GameSession, command: str) -> str:
        session.invalid_action_count += 1
        session.score = max(0, session.score - 1)
        text = (
            f"我理解你想执行“{command}”，但当前 MVP 只实现侦察、Web 调查和模拟 SSH 访问。"
            "输入 help 查看当前动作。无效动作会轻微影响学习评分。"
        )
        session.emit("agent", text)
        return text

    @staticmethod
    def _reject_external_target(session: GameSession, target: str) -> str:
        session.invalid_action_count += 1
        session.score = max(0, session.score - 2)
        text = f"纸上靶场拒绝访问场景外目标 {target}。当前允许的虚构目标只有 {session.scenario.target_ip}。"
        session.emit("system", text)
        return text

    @staticmethod
    def _grade(score: int) -> str:
        if score >= 95:
            return "S"
        if score >= 85:
            return "A"
        if score >= 70:
            return "B"
        return "C"
