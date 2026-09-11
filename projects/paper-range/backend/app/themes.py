from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass(frozen=True)
class ThemePack:
    id: str
    label: str
    family: str
    intensity: int


THEME_PACKS: dict[str, ThemePack] = {
    "inferno": ThemePack("inferno", "Inferno Core", "crimson", 5),
    "blood-moon": ThemePack("blood-moon", "Blood Moon", "crimson", 5),
    "black-site": ThemePack("black-site", "Black Site", "ember", 4),
    "ash-cathedral": ThemePack("ash-cathedral", "Ash Cathedral", "ash", 4),
    "neon-crypt": ThemePack("neon-crypt", "Neon Crypt", "magenta", 4),
    "reactor-amber": ThemePack("reactor-amber", "Reactor Amber", "amber", 4),
    "plague-green": ThemePack("plague-green", "Plague Green", "toxic", 4),
    "ice-vault": ThemePack("ice-vault", "Ice Vault", "cyan", 3),
    "violet-null": ThemePack("violet-null", "Violet Null", "violet", 4),
    "rust-foundry": ThemePack("rust-foundry", "Rust Foundry", "rust", 4),
    "signal-blue": ThemePack("signal-blue", "Signal Blue", "blue", 3),
    "obsidian-gold": ThemePack("obsidian-gold", "Obsidian Gold", "gold", 4),
}

THEME_IDS: tuple[str, ...] = tuple(THEME_PACKS)


def choose_theme(rng: random.Random | None = None) -> str:
    """Choose one registered theme for a new ephemeral session."""

    chooser = rng or random
    return chooser.choice(THEME_IDS)
