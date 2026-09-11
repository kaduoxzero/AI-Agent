import random

from app.runtime import SessionStore
from app.themes import THEME_IDS, THEME_PACKS, choose_theme


def test_theme_registry_has_twelve_unique_packs() -> None:
    assert len(THEME_IDS) == 12
    assert len(set(THEME_IDS)) == 12
    assert set(THEME_IDS) == set(THEME_PACKS)


def test_choose_theme_returns_only_registered_themes_and_has_variety() -> None:
    rng = random.Random(42)
    seen = {choose_theme(rng) for _ in range(120)}

    assert seen <= set(THEME_IDS)
    assert len(seen) > 3


def test_new_sessions_use_registered_theme_pack() -> None:
    store = SessionStore()
    themes = {store.create("abandoned-lab").theme_id for _ in range(48)}

    assert themes <= set(THEME_IDS)
    assert len(themes) > 1
