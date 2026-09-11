from __future__ import annotations

import random
import shlex
from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4

from .intent import IntentParser
from .models import (
    ActionIntent,
    ActionResponse,
    GameEvent,
    GameSessionView,
    HintResponse,
    LearningReport,
    PortService,
    Scenario,
)
from .scenarios import SCENARIOS
from .themes import choose_theme


HINT_COST = 10
BROAD_RECON_COST = 3
CORRELATION_CHECKS = {"log-query", "asset-map"}


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
    story_node: str = "recon"
    story_branch: str | None = None
    evidence_strategy: str | None = None
    investigation_checks: list[str] = field(default_factory=list)
    world_tags: list[str] = field(default_factory=lambda: ["ephemeral-world", "simulation-only"])
    consequences: list[str] = field(default_factory=list)
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
            story_node=self.story_node,
            story_branch=self.story_branch,
            evidence_strategy=self.evidence_strategy,
            investigation_checks=list(self.investigation_checks),
            world_tags=list(self.world_tags),
            consequences=list(self.consequences),
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
            "select_approach": lambda: self._select_approach(session, intent.option),
            "enumerate_paths": lambda: self._enumerate_paths(session, intent.target),
            "select_evidence_strategy": lambda: self._select_evidence_strategy(session, intent.option),
            "query_logs": lambda: self._query_logs(session),
            "trace_asset": lambda: self._trace_asset(session),
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

        if session.story_node == "evidence-strategy":
            hint = "你可以直接验证证据，也可以选择 correlate：先完成模拟日志查询和资产关系映射，再读取证据。"
        elif session.story_node == "correlation-work":
            missing = CORRELATION_CHECKS.difference(session.investigation_checks)
            labels = {"log-query": "日志查询", "asset-map": "资产关系映射"}
            hint = "关联证据路线还缺少：" + "、".join(labels[item] for item in sorted(missing)) + "。"
        else:
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
        if session.story_branch == "focused":
            strengths.append("选择了定向调查分支，用较小的模拟暴露面推进证据链。")
        elif session.story_branch == "broad":
            next_steps.append("下一局尝试 focused/定向调查，对比低噪声调查与广覆盖枚举的收益差异。")

        if session.evidence_strategy == "correlate" and CORRELATION_CHECKS.issubset(session.investigation_checks):
            strengths.append("完成日志与资产关系的双重关联后再读取证据，建立了更强的模拟证据置信度。")
        elif session.evidence_strategy == "direct":
            next_steps.append("下一局尝试 evidence correlate，体验日志查询 + 资产关系映射的条件调查路线。")

        if session.status == "completed":
            strengths.append("完成了侦察 → Web 初查 → 分支调查 → 证据验证 → 模拟访问的完整证据链。")
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
            story_branch=session.story_branch,
            evidence_strategy=session.evidence_strategy,
            investigation_checks=list(session.investigation_checks),
            world_tags=list(session.world_tags),
            consequences=list(session.consequences),
            strengths=strengths,
            next_steps=next_steps,
            flag=session.flag,
        )

    def _scan_ports(self, session: GameSession, target: str | None) -> str:
        resolved_target = target or session.scenario.target_ip
        if resolved_target != session.scenario.target_ip:
            return self._reject_external_target(session, resolved_target)

        session.discovered_services = list(session.scenario.services)
        session.story_node = "web-investigation"
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
        session.story_node = "approach-decision"
        self._complete_objective(session, "web", 2, "目标完成：调查 Web 服务。")
        session.emit("narrative", "站点没有把答案直接摆在首页，但页面细节留下了下一段调查路径。")
        session.emit(
            "agent",
            "Story Graph 已进入调查方式节点：可选 focused（定向、低噪声）或 broad（覆盖更广、-3 分）。直接枚举时默认 focused。",
        )
        return f"HTTP/1.1 200 OK\nserver: paper-range-sim\n\n{session.scenario.web_observation}"

    def _select_approach(self, session: GameSession, option: str | None) -> str:
        if "web" not in session.completed_objectives:
            return self._blocked(session, "调查方式分支尚未解锁。先完成端口侦察和 Web 初查。")
        if "enumerate" in session.completed_objectives:
            return self._blocked(session, "隐藏路径已经枚举完成，当前调查方式分支已经固化，不能回滚选择。")
        if option not in {"focused", "broad"}:
            return self._invalid(session, "请选择 approach focused 或 approach broad。")
        if session.story_branch is not None:
            return self._blocked(session, f"本局已经选择 {session.story_branch} 分支，分支一旦写入 WorldState 就不再改写。")
        return self._apply_story_branch(session, option, explicit=True)

    def _apply_story_branch(self, session: GameSession, option: str, *, explicit: bool) -> str:
        session.story_branch = option
        session.story_node = "path-enumeration"

        if option == "focused":
            self._append_unique(session.world_tags, "low-noise-recon")
            consequence = (
                "你沿 Web 线索做定向调查，模拟暴露面保持较低。"
                if explicit
                else "你没有显式选择调查方式，Agent 默认采用 focused 定向调查，保持较低模拟暴露面。"
            )
            self._append_unique(session.consequences, consequence)
            session.emit("narrative", consequence)
            session.emit("agent", "focused 分支只会优先暴露高置信度证据路径。")
            return f"STORY BRANCH LOCKED: focused\n{consequence}"

        self._append_unique(session.world_tags, "noisy-enumeration")
        consequence = "你选择广覆盖枚举，得到更多路径情报，但制造了更高的模拟噪声。"
        self._append_unique(session.consequences, consequence)
        session.score = max(0, session.score - BROAD_RECON_COST)
        session.emit("narrative", consequence)
        session.emit("agent", f"broad 分支已写入 WorldState（-{BROAD_RECON_COST} 分），后续会显示全部发现路径。")
        return f"STORY BRANCH LOCKED: broad\n{consequence}\nscore -{BROAD_RECON_COST}"

    def _enumerate_paths(self, session: GameSession, target: str | None) -> str:
        resolved_target = target or session.scenario.target_ip
        if resolved_target != session.scenario.target_ip:
            return self._reject_external_target(session, resolved_target)
        if "web" not in session.completed_objectives:
            return self._blocked(session, "先完成 Web 初查，再做路径枚举。这样线索链会更清晰。")

        if session.story_branch is None:
            self._apply_story_branch(session, "focused", explicit=False)

        clue = f"发现证据文件候选：{session.scenario.evidence_path}"
        if clue not in session.clues:
            session.clues.append(clue)
        session.story_node = "evidence-strategy"
        self._complete_objective(session, "enumerate", 3, "目标完成：枚举隐藏路径。")

        if session.story_branch == "focused":
            visible_paths = [session.scenario.evidence_path]
            header = "SIMULATED FOCUSED PATH ENUM"
        else:
            visible_paths = list(session.scenario.hidden_paths)
            header = "SIMULATED BROAD PATH ENUM"

        lines = [f"{header} {resolved_target}", "STATUS  PATH"]
        for path in visible_paths:
            lines.append(f"200     {path}")
        session.emit(
            "agent",
            "路径枚举完成。Story Graph v2 已进入证据策略节点：direct 可直接读取候选证据；correlate 需要先完成日志查询与资产关系映射。",
        )
        return "\n".join(lines)

    def _select_evidence_strategy(self, session: GameSession, option: str | None) -> str:
        if "enumerate" not in session.completed_objectives:
            return self._blocked(session, "证据策略节点尚未解锁。先完成路径枚举。")
        if "evidence" in session.completed_objectives:
            return self._blocked(session, "证据已经读取，本局证据策略已经固化，不能回滚。")
        if option not in {"direct", "correlate"}:
            return self._invalid(session, "请选择 evidence direct 或 evidence correlate。")
        if session.evidence_strategy is not None:
            return self._blocked(session, f"本局证据策略已经锁定为 {session.evidence_strategy}。")
        return self._apply_evidence_strategy(session, option, explicit=True)

    def _apply_evidence_strategy(self, session: GameSession, option: str, *, explicit: bool) -> str:
        session.evidence_strategy = option
        if option == "direct":
            session.story_node = "evidence-review"
            self._append_unique(session.world_tags, "direct-evidence-route")
            consequence = (
                "你选择直接验证候选证据，推进速度更快，但没有额外建立日志与资产关系的交叉置信度。"
                if explicit
                else "你没有显式选择证据策略，Agent 默认采用 direct 路线以保持旧版流程兼容。"
            )
            self._append_unique(session.consequences, consequence)
            session.emit("narrative", consequence)
            return f"EVIDENCE STRATEGY LOCKED: direct\n{consequence}"

        session.story_node = "correlation-work"
        self._append_unique(session.world_tags, "correlation-route")
        consequence = "你选择关联证据路线；只有日志查询和资产关系映射都完成后，候选证据才会被放行。"
        self._append_unique(session.consequences, consequence)
        session.emit("narrative", consequence)
        session.emit("agent", "需要完成两个 simulation-only 检查：log-query + asset-map。")
        self._refresh_correlation_state(session)
        return f"EVIDENCE STRATEGY LOCKED: correlate\n{consequence}"

    def _query_logs(self, session: GameSession) -> str:
        if "enumerate" not in session.completed_objectives:
            return self._blocked(session, "当前还没有可关联的路径上下文。先完成路径枚举。")
        if session.evidence_strategy == "direct":
            return self._blocked(session, "本局已经锁定 direct 证据路线；日志关联不再作为当前路线的必要检查。")
        if session.evidence_strategy is None:
            self._apply_evidence_strategy(session, "correlate", explicit=False)

        self._append_unique(session.investigation_checks, "log-query")
        self._append_unique(session.world_tags, "logs-correlated")
        clue = f"模拟日志关联确认：请求轨迹与候选证据 {session.scenario.evidence_path} 属于同一训练事件链。"
        self._append_unique(session.clues, clue)
        session.emit("agent", "日志查询完成：已把 Web/路径事件和候选证据关联到同一模拟时间线。")
        self._refresh_correlation_state(session)
        return (
            "SIMULATED LOG QUERY\n"
            f"host={session.scenario.target_ip}\n"
            "source=/var/log/paper-range/events.log\n"
            f"match=evidence-candidate {session.scenario.evidence_path}\n"
            "network_io=none"
        )

    def _trace_asset(self, session: GameSession) -> str:
        if "scan" not in session.completed_objectives:
            return self._blocked(session, "还没有服务画像，无法建立资产关系。先扫描当前虚构目标。")

        self._append_unique(session.investigation_checks, "asset-map")
        self._append_unique(session.world_tags, "asset-context-mapped")
        services = ", ".join(f"{item.port}/{item.service}" for item in session.discovered_services)
        clue = f"资产关系图确认：{session.scenario.target_ip} 的当前模拟服务链为 {services}。"
        self._append_unique(session.clues, clue)
        session.emit("agent", "资产关系映射完成：服务画像已经被整理成当前场景的 simulation-only 关系图。")
        self._refresh_correlation_state(session)
        return (
            "SIMULATED ASSET MAP\n"
            f"asset={session.scenario.target_ip}\n"
            f"services={services}\n"
            "scope=current-fictional-scenario-only\n"
            "network_io=none"
        )

    def _refresh_correlation_state(self, session: GameSession) -> None:
        if session.evidence_strategy != "correlate":
            return
        if CORRELATION_CHECKS.issubset(session.investigation_checks):
            session.story_node = "evidence-review"
            self._append_unique(session.world_tags, "correlated-evidence")
            consequence = "日志轨迹与资产关系已经交叉吻合，候选证据的模拟置信度提升，可以继续读取。"
            if consequence not in session.consequences:
                session.consequences.append(consequence)
                session.emit("reward", consequence)
        else:
            session.story_node = "correlation-work"

    def _inspect_file(self, session: GameSession, resource: str | None) -> str:
        if "enumerate" not in session.completed_objectives:
            return self._blocked(session, "当前还没有可靠的文件路径。先枚举隐藏路径。")

        if session.evidence_strategy is None:
            self._apply_evidence_strategy(session, "direct", explicit=False)
        if session.evidence_strategy == "correlate" and not CORRELATION_CHECKS.issubset(session.investigation_checks):
            missing = CORRELATION_CHECKS.difference(session.investigation_checks)
            labels = {"log-query": "日志查询", "asset-map": "资产关系映射"}
            return self._blocked(
                session,
                "关联证据路线尚未满足条件，还缺少：" + "、".join(labels[item] for item in sorted(missing)) + "。",
            )

        resolved_resource = resource or session.scenario.evidence_path
        if resolved_resource != session.scenario.evidence_path:
            session.invalid_action_count += 1
            session.score = max(0, session.score - 1)
            text = f"SIMULATED FILE NOT FOUND: {resolved_resource}。证据栏里已经记录了更可信的候选路径。"
            session.emit("agent", text)
            return text

        if session.scenario.evidence_text not in session.clues:
            session.clues.append(session.scenario.evidence_text)
        session.story_node = "access-validation"
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
        session.story_node = "complete"
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
        tags = ",".join(session.world_tags) if session.world_tags else "-"
        checks = ",".join(session.investigation_checks) if session.investigation_checks else "-"
        return (
            f"scenario={session.scenario.name}\n"
            f"status={session.status}\n"
            f"story_node={session.story_node}\n"
            f"story_branch={session.story_branch or 'unselected'}\n"
            f"evidence_strategy={session.evidence_strategy or 'unselected'}\n"
            f"investigation_checks={checks}\n"
            f"world_tags={tags}\n"
            f"consequences={len(session.consequences)}\n"
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
            "approach focused  # 定向、低噪声\n"
            "approach broad    # 广覆盖、-3 分\n"
            f"dirsearch -u http://{session.scenario.target_ip}\n"
            "evidence direct   # 直接验证候选证据\n"
            "evidence correlate # 先完成双重关联检查\n"
            "grep incident /var/log/paper-range/events.log\n"
            "asset-map\n"
            "cat /你从枚举结果中发现的证据文件\n"
            "ssh <你从证据中发现的用户>@<目标>\n"
            "status\n"
            "所有命令都只是 Typed Intent，不会交给系统 shell，也不会访问真实网络。"
        )

    def _unknown(self, session: GameSession, command: str) -> str:
        return self._invalid(
            session,
            f"我理解你想执行“{command}”，但当前模拟器只实现服务侦察、Web 调查、路径枚举、证据策略、模拟日志查询、资产关系映射、证据读取和模拟 SSH 访问。输入 help 查看动作。",
        )

    @staticmethod
    def _complete_objective(session: GameSession, objective_id: str, next_index: int, event: str) -> None:
        if objective_id not in session.completed_objectives:
            session.completed_objectives.append(objective_id)
            session.emit("reward", event)
        session.objective_index = max(session.objective_index, next_index)

    @staticmethod
    def _append_unique(items: list[str], value: str) -> None:
        if value not in items:
            items.append(value)

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
