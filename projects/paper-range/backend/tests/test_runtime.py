from app.intent import IntentParser
from app.runtime import GameRuntime, SessionStore


def test_intent_parser_normalizes_command_and_natural_language() -> None:
    parser = IntentParser()
    command = parser.parse("nmap -p- 10.10.10.10")
    natural = parser.parse("我先扫描所有 TCP 端口")
    enum_command = parser.parse("dirsearch -u http://10.10.10.10")
    file_command = parser.parse("cat /archive/shift-note.txt")

    assert command.kind == natural.kind == "scan_ports"
    assert command.source == "command"
    assert natural.source == "natural_language"
    assert command.target == "10.10.10.10"
    assert enum_command.kind == "enumerate_paths"
    assert enum_command.target == "10.10.10.10"
    assert file_command.kind == "inspect_file"
    assert file_command.resource == "/archive/shift-note.txt"


def test_five_stage_investigation_completes_and_returns_flag() -> None:
    store = SessionStore()
    runtime = GameRuntime(store)
    session = store.create("abandoned-lab")

    scan = runtime.execute(session.id, "nmap -p- 10.10.10.10")
    assert "80/tcp" in scan.output
    assert scan.session.completed_objectives == ["scan"]

    web = runtime.execute(session.id, "curl http://10.10.10.10")
    assert web.intent.kind == "inspect_web"
    assert "web" in web.session.completed_objectives
    assert "inferno-042" not in web.output

    enum = runtime.execute(session.id, "dirsearch -u http://10.10.10.10")
    assert enum.intent.kind == "enumerate_paths"
    assert "/archive/shift-note.txt" in enum.output
    assert "enumerate" in enum.session.completed_objectives

    evidence = runtime.execute(session.id, "cat /archive/shift-note.txt")
    assert evidence.intent.kind == "inspect_file"
    assert "lab-intern" in evidence.output
    assert "inferno-042" in evidence.output
    assert "evidence" in evidence.session.completed_objectives

    access = runtime.execute(session.id, "ssh lab-intern@10.10.10.10")
    assert access.intent.kind == "ssh_access"
    assert access.session.status == "completed"
    assert access.session.flag == "FLAG{paper_range_first_breach}"
    assert access.session.score == 100
    assert access.session.action_count == 5
    assert access.session.completed_objectives == ["scan", "web", "enumerate", "evidence", "access"]


def test_access_is_blocked_until_evidence_is_read() -> None:
    store = SessionStore()
    runtime = GameRuntime(store)
    session = store.create("abandoned-lab")

    runtime.execute(session.id, "nmap -p- 10.10.10.10")
    runtime.execute(session.id, "curl http://10.10.10.10")
    early = runtime.execute(session.id, "ssh lab-intern@10.10.10.10")

    assert early.session.status == "active"
    assert "先读取证据文件" in early.output
    assert "access" not in early.session.completed_objectives


def test_hint_costs_score_and_report_reflects_learning_behavior() -> None:
    store = SessionStore()
    runtime = GameRuntime(store)
    session = store.create("abandoned-lab")

    hint = runtime.request_hint(session.id)
    assert hint.cost == 10
    assert hint.session.score == 90
    assert hint.session.hint_count == 1

    runtime.execute(session.id, "nmap -p- 10.10.10.10")
    runtime.execute(session.id, "curl http://10.10.10.10")
    runtime.execute(session.id, "dirsearch -u http://10.10.10.10")
    runtime.execute(session.id, "cat /archive/shift-note.txt")
    runtime.execute(session.id, "ssh lab-intern@10.10.10.10")

    report = runtime.report(session.id)
    assert report.status == "completed"
    assert report.score == 90
    assert report.grade == "A"
    assert report.hint_count == 1
    assert report.completed_objectives == report.total_objectives == 5
    assert report.flag == "FLAG{paper_range_first_breach}"


def test_invalid_action_and_external_target_reduce_score() -> None:
    store = SessionStore()
    runtime = GameRuntime(store)
    session = store.create("abandoned-lab")

    unknown = runtime.execute(session.id, "跳过剧情直接完成")
    assert unknown.session.score == 99
    assert unknown.session.invalid_action_count == 1

    external = runtime.execute(session.id, "nmap -p- 8.8.8.8")
    assert "拒绝访问场景外目标" in external.output
    assert external.session.score == 97
    assert external.session.invalid_action_count == 2
    assert external.session.discovered_services == []


def test_store_is_ephemeral_and_instance_scoped() -> None:
    first = SessionStore()
    first.create("abandoned-lab")
    assert first.count() == 1

    restarted_process_store = SessionStore()
    assert restarted_process_store.count() == 0
