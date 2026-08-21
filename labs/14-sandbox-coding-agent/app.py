from __future__ import annotations

import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


class SandboxViolation(RuntimeError):
    pass


@dataclass(frozen=True)
class CommandPolicy:
    allowed_prefixes: tuple[tuple[str, ...], ...]

    def validate(self, argv: Sequence[str]) -> None:
        normalized = tuple(argv)
        if not any(normalized[: len(prefix)] == prefix for prefix in self.allowed_prefixes):
            raise SandboxViolation(f"command not allowed: {normalized}")


class Workspace:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()

    def resolve(self, relative: str) -> Path:
        candidate = (self.root / relative).resolve()
        try:
            candidate.relative_to(self.root)
        except ValueError as exc:
            raise SandboxViolation(f"path escapes workspace: {relative}") from exc
        return candidate

    def write_text(self, relative: str, content: str) -> Path:
        path = self.resolve(relative)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def read_text(self, relative: str) -> str:
        return self.resolve(relative).read_text(encoding="utf-8")


class ProcessRunner:
    def __init__(self, workspace: Workspace, policy: CommandPolicy) -> None:
        self.workspace = workspace
        self.policy = policy

    def run(self, argv: Sequence[str], timeout_seconds: float = 2.0) -> subprocess.CompletedProcess[str]:
        self.policy.validate(argv)
        return subprocess.run(
            list(argv),
            cwd=self.workspace.root,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
            shell=False,
        )


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="agent-sandbox-") as tmp:
        workspace = Workspace(Path(tmp))
        policy = CommandPolicy(
            allowed_prefixes=(
                (sys.executable, "-m", "py_compile"),
                (sys.executable, "-m", "unittest"),
            )
        )
        runner = ProcessRunner(workspace, policy)

        print("=== create workspace file ===")
        workspace.write_text(
            "src/demo.py",
            "def add(a: int, b: int) -> int:\n    return a + b\n",
        )
        print(workspace.read_text("src/demo.py"))

        print("=== compile inside workspace ===")
        result = runner.run(
            [sys.executable, "-m", "py_compile", "src/demo.py"],
            timeout_seconds=2,
        )
        print("returncode=", result.returncode)
        print("stderr=", result.stderr.strip())

        print("\n=== path traversal attempt ===")
        try:
            workspace.read_text("../secret.txt")
        except SandboxViolation as exc:
            print("REJECTED:", exc)

        print("\n=== unauthorized command attempt ===")
        try:
            runner.run([sys.executable, "-c", "print('not allowed')"])
        except SandboxViolation as exc:
            print("REJECTED:", exc)

        print("\nworkspace destroyed automatically after task exits")


if __name__ == "__main__":
    main()
