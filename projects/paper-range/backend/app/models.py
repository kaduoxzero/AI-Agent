from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


ActionKind = Literal[
    "scan_ports",
    "inspect_web",
    "select_approach",
    "enumerate_paths",
    "inspect_file",
    "ssh_access",
    "status",
    "help",
    "unknown",
]


class PortService(BaseModel):
    port: int
    protocol: Literal["tcp"] = "tcp"
    service: str
    version: str


class Objective(BaseModel):
    id: str
    title: str
    description: str


class ScenarioPublic(BaseModel):
    """Scenario metadata safe to expose before the player discovers evidence.

    `ssh_user` remains public for the current UI's command helper, but passwords,
    evidence bodies, hidden paths and flags stay server-side.
    """

    id: str
    name: str
    subtitle: str
    difficulty: Literal["入门", "进阶", "困难"]
    category: str
    target_ip: str
    intro: str
    briefing: str
    objectives: list[Objective]
    ssh_user: str


class Scenario(ScenarioPublic):
    """Server-side scenario definition with undiscovered evidence and rewards."""

    services: list[PortService]
    hints: list[str]
    web_observation: str
    hidden_paths: list[str]
    evidence_path: str
    evidence_text: str
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
    resource: str | None = None
    option: Literal["focused", "broad"] | None = None


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
    story_node: str
    story_branch: Literal["focused", "broad"] | None = None
    world_tags: list[str]
    consequences: list[str]
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
    story_branch: Literal["focused", "broad"] | None = None
    world_tags: list[str]
    consequences: list[str]
    strengths: list[str]
    next_steps: list[str]
    flag: str | None = None
