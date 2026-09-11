from __future__ import annotations

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from .models import (
    ActionRequest,
    ActionResponse,
    GameSessionView,
    HintResponse,
    LearningReport,
    ScenarioPublic,
    SessionCreateRequest,
)
from .runtime import GameRuntime, SessionStore
from .scenarios import list_scenarios


store = SessionStore()
runtime = GameRuntime(store)

app = FastAPI(
    title="Paper Range API",
    version="0.3.0",
    description="Ephemeral narrative cyber-range simulator for AI-Agent.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:8080", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, object]:
    return {"status": "ok", "sessions": store.count(), "persistence": "process-memory-only"}


@app.get("/api/scenarios", response_model=list[ScenarioPublic])
def scenarios() -> list[ScenarioPublic]:
    # FastAPI/Pydantic response filtering intentionally strips server-only evidence,
    # hidden paths, passwords and flags from pre-game scenario metadata.
    return list_scenarios()


@app.post("/api/sessions", response_model=GameSessionView, status_code=status.HTTP_201_CREATED)
def create_session(payload: SessionCreateRequest) -> GameSessionView:
    try:
        session = store.create(payload.scenario_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return session.view()


@app.get("/api/sessions/{session_id}", response_model=GameSessionView)
def get_session(session_id: str) -> GameSessionView:
    try:
        return store.get(session_id).view()
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="session not found") from exc


@app.post("/api/sessions/{session_id}/actions", response_model=ActionResponse)
def action(session_id: str, payload: ActionRequest) -> ActionResponse:
    try:
        return runtime.execute(session_id, payload.input)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="session not found") from exc


@app.post("/api/sessions/{session_id}/hint", response_model=HintResponse)
def hint(session_id: str) -> HintResponse:
    try:
        return runtime.request_hint(session_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="session not found") from exc


@app.get("/api/sessions/{session_id}/report", response_model=LearningReport)
def report(session_id: str) -> LearningReport:
    try:
        return runtime.report(session_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="session not found") from exc


@app.delete("/api/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(session_id: str) -> None:
    store.delete(session_id)
