from app.runtime import GameRuntime, SessionStore


def test_vertical_slice_completes_and_returns_flag() -> None:
    store = SessionStore()
    runtime = GameRuntime(store)
    session = store.create("abandoned-lab")

    scan = runtime.execute(session.id, "nmap -p- 10.10.10.10")
    assert scan.action == "scan_ports"
    assert "80/tcp" in scan.output
    assert "scan" in scan.session.completed_objectives

    web = runtime.execute(session.id, "curl http://10.10.10.10")
    assert web.action == "inspect_web"
    assert "lab-intern" in web.output
    assert "web" in web.session.completed_objectives

    access = runtime.execute(session.id, "ssh lab-intern@10.10.10.10")
    assert access.action == "ssh_access"
    assert access.session.status == "completed"
    assert access.session.flag == "FLAG{paper_range_first_breach}"


def test_runtime_refuses_targets_outside_current_scenario() -> None:
    store = SessionStore()
    runtime = GameRuntime(store)
    session = store.create("abandoned-lab")

    response = runtime.execute(session.id, "nmap -p- 8.8.8.8")

    assert "拒绝访问场景外目标" in response.output
    assert response.session.discovered_services == []


def test_store_is_ephemeral_and_instance_scoped() -> None:
    first = SessionStore()
    first.create("abandoned-lab")
    assert first.count() == 1

    restarted_process_store = SessionStore()
    assert restarted_process_store.count() == 0
