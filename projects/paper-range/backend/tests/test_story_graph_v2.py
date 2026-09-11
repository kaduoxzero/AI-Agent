from app.intent import IntentParser
from app.runtime import GameRuntime, SessionStore


def _ready_for_evidence_strategy(runtime: GameRuntime, session_id: str) -> None:
    runtime.execute(session_id, "nmap -p- 10.10.10.10")
    runtime.execute(session_id, "curl http://10.10.10.10")
    runtime.execute(session_id, "approach focused")
    runtime.execute(session_id, "dirsearch -u http://10.10.10.10")


def test_parser_recognizes_investigation_v2_actions() -> None:
    parser = IntentParser()

    correlate = parser.parse("evidence correlate")
    direct = parser.parse("我选择直接验证")
    logs = parser.parse("grep incident /var/log/paper-range/events.log")
    assets = parser.parse("追踪资产关系")

    assert correlate.kind == "select_evidence_strategy"
    assert correlate.option == "correlate"
    assert direct.kind == "select_evidence_strategy"
    assert direct.option == "direct"
    assert logs.kind == "query_logs"
    assert assets.kind == "trace_asset"


def test_correlate_route_requires_both_simulated_checks() -> None:
    store = SessionStore()
    runtime = GameRuntime(store)
    session = store.create("abandoned-lab")
    _ready_for_evidence_strategy(runtime, session.id)

    selected = runtime.execute(session.id, "evidence correlate")
    assert selected.session.evidence_strategy == "correlate"
    assert selected.session.story_node == "correlation-work"

    blocked = runtime.execute(session.id, "cat /archive/shift-note.txt")
    assert "还缺少" in blocked.output
    assert "evidence" not in blocked.session.completed_objectives

    assets = runtime.execute(session.id, "asset-map")
    assert "network_io=none" in assets.output
    assert assets.session.story_node == "correlation-work"
    assert "asset-map" in assets.session.investigation_checks

    logs = runtime.execute(session.id, "grep incident /var/log/paper-range/events.log")
    assert "network_io=none" in logs.output
    assert logs.session.story_node == "evidence-review"
    assert set(logs.session.investigation_checks) == {"asset-map", "log-query"}
    assert "correlated-evidence" in logs.session.world_tags

    evidence = runtime.execute(session.id, "cat /archive/shift-note.txt")
    assert "inferno-042" in evidence.output
    assert "evidence" in evidence.session.completed_objectives

    report = runtime.report(session.id)
    assert report.evidence_strategy == "correlate"
    assert any("双重关联" in strength for strength in report.strengths)


def test_direct_route_keeps_backward_compatible_fast_path() -> None:
    store = SessionStore()
    runtime = GameRuntime(store)
    session = store.create("abandoned-lab")
    _ready_for_evidence_strategy(runtime, session.id)

    selected = runtime.execute(session.id, "evidence direct")
    assert selected.session.evidence_strategy == "direct"
    assert selected.session.story_node == "evidence-review"

    evidence = runtime.execute(session.id, "cat /archive/shift-note.txt")
    assert "evidence" in evidence.session.completed_objectives
    assert evidence.session.score == 100

    logs = runtime.execute(session.id, "查询日志")
    assert "锁定 direct" in logs.output


def test_asset_map_is_simulation_only_and_can_be_precomputed() -> None:
    store = SessionStore()
    runtime = GameRuntime(store)
    session = store.create("abandoned-lab")

    runtime.execute(session.id, "nmap -p- 10.10.10.10")
    mapped = runtime.execute(session.id, "asset-map")

    assert mapped.intent.kind == "trace_asset"
    assert "scope=current-fictional-scenario-only" in mapped.output
    assert "network_io=none" in mapped.output
    assert "asset-map" in mapped.session.investigation_checks
