from __future__ import annotations

from .models import ActionIntent


class IntentParser:
    """Deterministic parser for the typed simulation Action Contract.

    The parser only classifies user intent. It never executes operating-system commands
    or reaches the network, which keeps interpretation separate from world mutation.
    """

    def parse(self, raw_input: str) -> ActionIntent:
        command = raw_input.strip()
        lower = command.lower()
        target = self._extract_target(command)
        resource = self._extract_resource(command)
        option = self._extract_option(command)
        source = "command" if self._looks_like_command(lower) else "natural_language"

        if lower in {"help", "?", "帮助"}:
            kind = "help"
        elif lower in {"status", "状态", "任务"}:
            kind = "status"
        elif option is not None and (
            lower.startswith(("approach ", "mode ", "route ", "strategy "))
            or any(
                phrase in command
                for phrase in ["定向调查", "低噪声调查", "聚焦调查", "全面调查", "广泛调查", "高覆盖调查", "全量枚举"]
            )
        ):
            kind = "select_approach"
        elif lower.startswith("nmap ") or any(word in command for word in ["扫描", "端口", "探测服务"]):
            kind = "scan_ports"
        elif lower.startswith("curl ") or any(word in command for word in ["访问网站", "调查 web", "查看网页", "检查 web", "打开网站"]):
            kind = "inspect_web"
        elif lower.startswith(("dirsearch ", "gobuster ")) or any(
            word in command for word in ["目录枚举", "枚举目录", "枚举路径", "扫描目录", "找隐藏路径"]
        ):
            kind = "enumerate_paths"
        elif lower.startswith(("cat ", "less ", "type ")) or any(
            word in command for word in ["读取文件", "查看日志", "读取日志", "读取证据", "打开证据", "查看文件"]
        ):
            kind = "inspect_file"
        elif lower.startswith("ssh ") or any(word in command for word in ["ssh 登录", "登录主机", "远程登录"]):
            kind = "ssh_access"
        else:
            kind = "unknown"

        return ActionIntent(
            kind=kind,
            raw_input=command,
            source=source,
            target=target,
            resource=resource,
            option=option,
        )

    @staticmethod
    def _looks_like_command(lower: str) -> bool:
        return lower.startswith(
            (
                "nmap ",
                "curl ",
                "dirsearch ",
                "gobuster ",
                "cat ",
                "less ",
                "type ",
                "ssh ",
                "approach ",
                "mode ",
                "route ",
                "strategy ",
                "help",
                "status",
            )
        ) or lower in {"?"}

    @staticmethod
    def _extract_target(command: str) -> str | None:
        normalized = command.replace("http://", " ").replace("https://", " ").replace("@", " ")
        for token in normalized.split():
            stripped = token.strip("/: ,[]()")
            parts = stripped.split(".")
            if len(parts) == 4 and all(part.isdigit() for part in parts):
                return stripped
        return None

    @staticmethod
    def _extract_resource(command: str) -> str | None:
        for token in command.split():
            stripped = token.strip("\"'[]()")
            if stripped.startswith("/") and len(stripped) > 1:
                return stripped.rstrip(";,.")
        return None

    @staticmethod
    def _extract_option(command: str) -> str | None:
        lower = command.lower()
        if any(token in lower for token in ["focused", "focus", "quiet"]) or any(
            phrase in command for phrase in ["定向调查", "低噪声调查", "聚焦调查"]
        ):
            return "focused"
        if any(token in lower for token in ["broad", "wide", "noisy"]) or any(
            phrase in command for phrase in ["全面调查", "广泛调查", "高覆盖调查", "全量枚举"]
        ):
            return "broad"
        return None
