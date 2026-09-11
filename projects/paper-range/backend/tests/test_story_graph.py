from app.intent import IntentParser
from app.runtime import BROAD_RECON_COST, GameRuntime, SessionStore


def _reach_web(runtime: GameRuntime, session_id: str) -> None:
    runtime.execute(session_id, "nmap -p- 10.10.10.10")
    runtime.execute(session_id, "curl http://10.10.10.10")


def test_parser_understands_story_approach_commands_and_natural_language() -> None:
    parser = IntentParser()

    focused = parser.parse("approach focused")
    broad = parser.parse("strategy broad")
    natural = parser.parse("我选择低噪声调查")

    assert focused.kind == "select_approach"
    assert focused.option == "focused"
    assert focused.source == "command"
    assert broad.kind == "select_approach"
    assert broad.option == "broad"
    assert natural.kind == "select_approach"
    assert natural.option == "focused"
    assert natural.source == "natural_language"


def test_focused_branch_changes_world_state_and_limits_visible_paths() -> None:
    store = SessionStore()
    runtime = GameRuntime(store)
    session = store.create("abandoned-lab")
    _reach_web(runtime, session.id)

    choice = runtime.execute(session.id, "approach focused")
    assert choice.session.story_node == "path-enumeration"
    assert choice.session.story_branch == "focused"
    assert "low-noise-recon" in choice.session.world_tags
    assert choice.session.score == 100

    enum = runtime.execute(session.id, "dirsearch -u http://10.10.10.10")
    assert enum.session.story_node == "evidence-review"
    assert "/archive/shift-note.txt" in enum.output
    assert "/assets/" not in enum.output
    assert enum.session.score == 100


def test_broad_branch_exposes_more_paths_and_records_consequence() -> None:
    store = SessionStore()
    runtime = GameRuntime(store)
    session = store.create("abandoned-lab")
    _reach_web(runtime, session.id)

    choice = runtime.execute(session.id, "approach broad")
    assert choice.session.story_branch == "broad"
    assert "noisy-enumeration" in choice.session.world_tags
    assert choice.session.score == 100 - BROAD_RECON_COST
    assert any("广覆盖枚举" in item for item in choice.session.consequences)

    enum = runtime.execute(session.id, "dirsearch -u http://10.10.10.10")
    assert "/archive/" in enum.output
    assert "/assets/" in enum.output
    assert "/archive/shift-note.txt" in enum.output

    report = runtime.report(session.id)
    assert report.story_branch == "broad"
    assert "noisy-enumeration" in report.world_tags
    assert any("focused" in item for item in report.next_steps)


def test_enumeration_without_explicit_choice_defaults_to_focused_for_backward_compatibility() -> None:
    store = SessionStore()
    runtime = GameRuntime(store)
    session = store.create("abandoned-lab")
    _reach_web(runtime, session.id)

    enum = runtime.execute(session.id, "dirsearch -u http://10.10.10.10")

    assert enum.session.story_branch == "focused"
    assert enum.session.score == 100
    assert "low-noise-recon" in enum.session.world_tags
    assert any("默认采用 focused" in item for item in enum.session.consequences)


def test_story_branch_cannot_be_rewritten_after_it_is_selected() -> None:
    store = SessionStore()
    runtime = GameRuntime(store)
    session = store.create("abandoned-lab")
    _reach_web(runtime, session.id)

    runtime.execute(session.id, "approach focused")
    second = runtime.execute(session.id, "approach broad")

    assert second.session.story_branch == "focused"
    assert second.session.score == 100
    assert "已经选择 focused" in second.output
