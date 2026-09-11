from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


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
    web_clue: str
    ssh_user: str
    ssh_password: str
    flag: str


class SessionCreateRequest(BaseModel):
    scenario_id: str | None = None


class ActionRequest(BaseModel):
    input: str = Field(min_length=1, max_length=2000)


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
    flag: str | None = None


class ActionResponse(BaseModel):
    action: str
    output: str
    session: GameSessionView
