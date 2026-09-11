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
        elif option in {"focused", "broad"} and (
            lower.startswith(("approach ", "mode ", "route ", "strategy "))
            or any(
                phrase in command
                for phrase in ["定向调查", "低噪声调查", "聚焦调查", "全面调查", "广泛调查", "高覆盖调查", "全量枚举"]
            )
        ):
            kind = "select_approach"
        elif option in {"direct", "correlate"} and (
            lower.startswith(("evidence ", "verify ", "analysis "))
            or any(phrase in command for phrase in ["直接验证", "直接取证", "关联证据", "交叉验证", "证据关联"])
        ):
            kind = "select_evidence_strategy"
        elif lower.startswith("nmap ") or any(word in command for word in ["扫描", "端口", "探测服务"]):
            kind = "scan_ports"
        elif lower.startswith("curl ") or any(word in command for word in ["访问网站", "调查 web", "查看网页", "检查 web", "打开网站"]):
            kind = "inspect_web"
        elif lower.startswith(("dirsearch ", "gobuster ")) or any(
            word in command for word in ["目录枚举", "枚举目录", "枚举路径", "扫描目录", "找隐藏路径"]
        ):
            kind = "enumerate_paths"
        elif lower.startswith(("grep ", "journalctl ", "log-query ")) or any(
            word in command for word in ["查询日志", "搜索日志", "检索日志", "关联日志", "分析日志"]
        ):
            kind = "query_logs"
        elif lower.startswith(("asset-map", "asset map", "trace asset")) or any(
            word in command for word in ["追踪资产关系", "映射资产", "资产关联", "关联服务", "服务关系"]
        ):
            kind = "trace_asset"
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
                "grep ",
                "journalctl ",
                "log-query ",
                "asset-map",
                "asset map",
                "trace asset",
                "cat ",
                "less ",
                "type ",
                "ssh ",
                "approach ",
                "mode ",
                "route ",
                "strategy ",
                "evidence ",
                "verify ",
                "analysis ",
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
        if any(token in lower for token in ["correlate", "correlation", "cross-check"]) or any(
            phrase in command for phrase in ["关联证据", "交叉验证", "证据关联"]
        ):
            return "correlate"
        if any(token in lower for token in ["direct", "straight"]) or any(
            phrase in command for phrase in ["直接验证", "直接取证"]
        ):
            return "direct"
        return None
