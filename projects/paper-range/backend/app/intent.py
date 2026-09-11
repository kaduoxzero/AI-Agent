from __future__ import annotations

from .models import ActionIntent


class IntentParser:
    """Deterministic parser for the MVP action contract.

    The parser produces a typed intent and never executes operating-system commands.
    It is intentionally replaceable by a structured LLM parser later, while keeping
    GameRuntime independent from the interpretation strategy.
    """

    def parse(self, raw_input: str) -> ActionIntent:
        command = raw_input.strip()
        lower = command.lower()
        target = self._extract_target(command)
        source = "command" if self._looks_like_command(lower) else "natural_language"

        if lower in {"help", "?", "帮助"}:
            kind = "help"
        elif lower in {"status", "状态", "任务"}:
            kind = "status"
        elif lower.startswith("nmap ") or any(word in command for word in ["扫描", "端口", "探测服务"]):
            kind = "scan_ports"
        elif lower.startswith("curl ") or any(word in command for word in ["访问网站", "调查 web", "查看网页", "检查 web"]):
            kind = "inspect_web"
        elif lower.startswith("ssh ") or any(word in command for word in ["ssh 登录", "登录主机", "远程登录"]):
            kind = "ssh_access"
        else:
            kind = "unknown"

        return ActionIntent(kind=kind, raw_input=command, source=source, target=target)

    @staticmethod
    def _looks_like_command(lower: str) -> bool:
        return lower.startswith(("nmap ", "curl ", "ssh ", "help", "status")) or lower in {"?"}

    @staticmethod
    def _extract_target(command: str) -> str | None:
        normalized = command.replace("http://", " ").replace("https://", " ").replace("@", " ")
        for token in normalized.split():
            stripped = token.strip("/:,[]()")
            parts = stripped.split(".")
            if len(parts) == 4 and all(part.isdigit() for part in parts):
                return stripped
        return None
