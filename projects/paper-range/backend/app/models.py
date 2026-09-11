from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


ActionKind = Literal["scan_ports", "inspect_web", "ssh_access", "status", "help", "unknown"]


class PortService(BaseModel):
    port: int
    protocol: Literal["tcp"] = "tcp"
    service: str
    version: str


class Objective(BaseModel):
    id: str
    title: str
    description: str


class Scenario(BaseModel):
    id: str
    name: str
    subtitle: str
    difficulty: Literal["入门", "进阶", "困难"]
    category: str
    target_ip: str
    intro: str
    briefing: str
    services: list[PortService]
    objectives: list[Objective]
    hints: list[str]
    web_clue: str
    ssh_user: str
    ssh_password: str
    flag: str


class SessionCreateRequest(BaseModel):
    scenario_id: str | None = None


class ActionRequest(BaseModel):
    input: str = Field(min_length=1, max_length=2000)


class ActionIntent(BaseModel):
    kind: ActionKind
    raw_input: str
    source: Literal["command", "natural_language", "system"]
    target: str | None = None


class GameEvent(BaseModel):
    seq: int
    kind: Literal["system", "narrative", "tool", "agent", "reward"]
    text: str


class GameSessionView(BaseModel):
    id: str
    scenario_id: str
    scenario_name: str
    theme_id: str
    target_ip: str
    created_at: str
    status: Literal["active", "completed"]
    objective_index: int
    completed_objectives: list[str]
    clues: list[str]
    discovered_services: list[PortService]
    events: list[GameEvent]
    score: int
    action_count: int
    hint_count: int
    invalid_action_count: int
    flag: str | None = None


class ActionResponse(BaseModel):
    intent: ActionIntent
    output: str
    session: GameSessionView


class HintResponse(BaseModel):
    hint: str
    cost: int
    session: GameSessionView


class LearningReport(BaseModel):
    session_id: str
    scenario_name: str
    status: Literal["active", "completed"]
    score: int
    grade: Literal["S", "A", "B", "C"]
    action_count: int
    hint_count: int
    invalid_action_count: int
    completed_objectives: int
    total_objectives: int
    strengths: list[str]
    next_steps: list[str]
    flag: str | None = None
