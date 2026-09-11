from __future__ import annotations

import random
import shlex
from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4

from .intent import IntentParser
from .models import ActionIntent, ActionResponse, GameEvent, GameSessionView, HintResponse, LearningReport, PortService, Scenario
from .scenarios import SCENARIOS
from .themes import choose_theme


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
    """Process-local game memory; a restarted backend starts with an empty world."""

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
            theme_id=choose_theme(),
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

        handlers = {
            "scan_ports": lambda: self._scan_ports(session, intent.target),
            "inspect_web": lambda: self._inspect_web(session, intent.target),
            "enumerate_paths": lambda: self._enumerate_paths(session, intent.target),
            "inspect_file": lambda: self._inspect_file(session, intent.resource),
            "ssh_access": lambda: self._ssh_access(session, intent),
            "status": lambda: self._status(session),
            "help": lambda: self._help(session),
        }
        handler = handlers.get(intent.kind)
        output = handler() if handler else self._unknown(session, intent.raw_input)
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

        strengths.append(
            "没有使用 Hint，能够自主推进当前任务链。"
            if session.hint_count == 0
            else "能够利用 Hint 恢复任务方向并继续完成推演。"
        )
        if session.invalid_action_count <= 1:
            strengths.append("行动路径较集中，较少出现与当前目标无关的尝试。")
        if session.status == "completed":
            strengths.append("完成了侦察 → Web 初查 → 路径枚举 → 证据读取 → 模拟访问的完整证据链。")
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
        self._complete_objective(session, "scan", 1, "目标完成：扫描开放端口。")
        lines = [f"SIMULATED NMAP {resolved_target}", "PORT      STATE  SERVICE       VERSION"]
        for service in session.scenario.services:
            lines.append(f"{service.port}/tcp   open   {service.service:<13} {service.version}")
        lines.append(f"扫描完成：发现 {len(session.scenario.services)} 个开放 TCP 端口。")
        session.emit("agent", "服务画像已经建立。下一步先检查 Web 服务，不要直接猜凭据。")
        return "\n".join(lines)

    def _inspect_web(self, session: GameSession, target: str | None) -> str:
        resolved_target = target or session.scenario.target_ip
        if resolved_target != session.scenario.target_ip:
            return self._reject_external_target(session, resolved_target)
        if "scan" not in session.completed_objectives:
            return self._blocked(session, "你还没有建立服务画像。先扫描目标，再决定是否调查 Web。")

        if session.scenario.web_observation not in session.clues:
            session.clues.append(session.scenario.web_observation)
        self._complete_objective(session, "web", 2, "目标完成：调查 Web 服务。")
        session.emit("narrative", "站点没有把答案直接摆在首页，但页面细节留下了下一段调查路径。")
        session.emit("agent", "初步 Web 观察已加入证据栏。下一步可以枚举隐藏目录或路径。")
        return f"HTTP/1.1 200 OK\nserver: paper-range-sim\n\n{session.scenario.web_observation}"

    def _enumerate_paths(self, session: GameSession, target: str | None) -> str:
        resolved_target = target or session.scenario.target_ip
        if resolved_target != session.scenario.target_ip:
            return self._reject_external_target(session, resolved_target)
        if "web" not in session.completed_objectives:
            return self._blocked(session, "先完成 Web 初查，再做路径枚举。这样线索链会更清晰。")

        clue = f"发现证据文件候选：{session.scenario.evidence_path}"
        if clue not in session.clues:
            session.clues.append(clue)
        self._complete_objective(session, "enumerate", 3, "目标完成：枚举隐藏路径。")
        lines = [f"SIMULATED PATH ENUM {resolved_target}", "STATUS  PATH"]
        for path in session.scenario.hidden_paths:
            lines.append(f"200     {path}")
        session.emit("agent", f"路径枚举完成。最值得读取的证据候选是 {session.scenario.evidence_path}。")
        return "\n".join(lines)

    def _inspect_file(self, session: GameSession, resource: str | None) -> str:
        if "enumerate" not in session.completed_objectives:
            return self._blocked(session, "当前还没有可靠的文件路径。先枚举隐藏路径。")

        resolved_resource = resource or session.scenario.evidence_path
        if resolved_resource != session.scenario.evidence_path:
            session.invalid_action_count += 1
            session.score = max(0, session.score - 1)
            text = f"SIMULATED FILE NOT FOUND: {resolved_resource}。证据栏里已经记录了更可信的候选路径。"
            session.emit("agent", text)
            return text

        if session.scenario.evidence_text not in session.clues:
            session.clues.append(session.scenario.evidence_text)
        self._complete_objective(session, "evidence", 4, "目标完成：读取证据文件。")
        session.emit("narrative", "文件内容被解析后，一条只属于当前模拟世界的训练身份浮出水面。")
        session.emit("agent", "凭据证据已加入线索栏。现在可以验证模拟 SSH 访问。")
        return f"SIMULATED FILE READ {resolved_resource}\n\n{session.scenario.evidence_text}"

    def _ssh_access(self, session: GameSession, intent: ActionIntent) -> str:
        if intent.target and intent.target != session.scenario.target_ip:
            return self._reject_external_target(session, intent.target)
        if "evidence" not in session.completed_objectives:
            return self._blocked(session, "还没有经过验证的训练身份。先读取证据文件，再尝试模拟登录。")

        try:
            args = shlex.split(intent.raw_input)
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

        if intent.source == "command" and supplied_user is None:
            return self._invalid(session, "模拟 SSH 需要明确用户，例如 ssh <证据中的用户>@<目标>。")
        if supplied_user and supplied_user != session.scenario.ssh_user:
            return self._invalid(session, f"模拟 SSH 拒绝用户 {supplied_user}。请对照证据栏中的训练身份。")
        if supplied_password and supplied_password != session.scenario.ssh_password:
            return self._invalid(session, "模拟 SSH 认证失败。当前训练口令与证据不匹配。")

        self._complete_objective(session, "access", len(session.scenario.objectives), "目标完成：建立模拟访问。")
        session.status = "completed"
        session.flag = session.scenario.flag
        session.completed_at = datetime.now(UTC)
        session.emit("narrative", "主机欢迎语闪过，封存事故的证据目录出现在屏幕上。战役结束。")
        session.emit("reward", f"MISSION COMPLETE — {session.flag}")
        return (
            "SIMULATED SSH ACCESS GRANTED\n"
            f"user={session.scenario.ssh_user}\n"
            f"host={session.scenario.target_ip}\n"
            f"{session.flag}"
        )

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
            "可以直接用自然语言，也可以输入以下模拟命令：\n"
            f"nmap -p- {session.scenario.target_ip}\n"
            f"curl http://{session.scenario.target_ip}\n"
            f"dirsearch -u http://{session.scenario.target_ip}\n"
            "cat /你从枚举结果中发现的证据文件\n"
            "ssh <你从证据中发现的用户>@<目标>\n"
            "status\n"
            "也可以在任务面板请求 Hint（每次 -10 分）。"
        )

    def _unknown(self, session: GameSession, command: str) -> str:
        return self._invalid(
            session,
            f"我理解你想执行“{command}”，但当前模拟器只实现端口扫描、Web 初查、路径枚举、证据读取和模拟 SSH 访问。输入 help 查看动作。",
        )

    @staticmethod
    def _complete_objective(session: GameSession, objective_id: str, next_index: int, event: str) -> None:
        if objective_id not in session.completed_objectives:
            session.completed_objectives.append(objective_id)
            session.emit("reward", event)
        session.objective_index = max(session.objective_index, next_index)

    @staticmethod
    def _blocked(session: GameSession, text: str) -> str:
        session.emit("agent", text)
        return text

    @staticmethod
    def _invalid(session: GameSession, text: str) -> str:
        session.invalid_action_count += 1
        session.score = max(0, session.score - 1)
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
