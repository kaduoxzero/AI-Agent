from __future__ import annotations

from .models import Objective, PortService, Scenario


SCENARIOS: dict[str, Scenario] = {
    "abandoned-lab": Scenario(
        id="abandoned-lab",
        name="废弃研究所",
        subtitle="一座被紧急封存的生物研究设施仍在回应网络探测。",
        difficulty="入门",
        category="Web / Linux",
        target_ip="10.10.10.10",
        intro="雨水敲击着封锁区的金属外墙。研究所已经断电三年，但内部网络刚刚出现了心跳。",
        briefing="确认目标暴露面，找到遗留的研究日志，并进入模拟主机取得证据。所有动作都发生在纸上靶场的虚构世界中。",
        services=[
            PortService(port=22, service="ssh", version="OpenSSH 8.2p1"),
            PortService(port=80, service="http", version="nginx 1.18"),
            PortService(port=443, service="https", version="nginx 1.18"),
            PortService(port=3306, service="mysql", version="MySQL 8.0"),
        ],
        objectives=[
            Objective(id="scan", title="扫描开放端口", description="识别研究所主机暴露的 TCP 服务。"),
            Objective(id="web", title="调查 Web 服务", description="读取遗留页面并找到值班记录。"),
            Objective(id="access", title="建立模拟访问", description="使用剧情中发现的凭据进入虚构 SSH 主机。"),
        ],
        hints=[
            "先建立服务画像。你可以说“扫描所有 TCP 端口”，也可以输入 nmap -p- 10.10.10.10。",
            "开放端口里有 Web 服务。尝试访问目标主页，寻找遗留日志。",
            "你已经拿到训练账户。模拟 SSH 会接受剧情中发现的身份。",
        ],
        web_clue="/archive/shift-note.txt: 夜班账号 lab-intern；应急口令写在旧工牌背面：inferno-042",
        ssh_user="lab-intern",
        ssh_password="inferno-042",
        flag="FLAG{paper_range_first_breach}",
    ),
    "corp-intranet": Scenario(
        id="corp-intranet",
        name="企业内网残影",
        subtitle="一次演练结束后，隔离办公网里仍残留异常服务。",
        difficulty="进阶",
        category="Intranet / Service Discovery",
        target_ip="10.20.30.15",
        intro="凌晨两点，演练平台本应完全关闭，但一台资产仍持续广播心跳。你的任务是解释它为什么还活着。",
        briefing="枚举虚构办公网主机、检查内部站点、获取用于演练的临时访问身份。",
        services=[
            PortService(port=22, service="ssh", version="OpenSSH 9.0"),
            PortService(port=8080, service="http-proxy", version="Caddy 2.7"),
            PortService(port=8443, service="https-alt", version="Caddy 2.7"),
        ],
        objectives=[
            Objective(id="scan", title="确认残留服务", description="扫描目标主机并记录暴露服务。"),
            Objective(id="web", title="读取内部告警页", description="检查内部 Web 服务中的演练线索。"),
            Objective(id="access", title="进入演练主机", description="使用剧情凭据完成模拟 SSH 登录。"),
        ],
        hints=[
            "先确认主机还暴露了哪些服务。服务发现是解释异常资产的第一步。",
            "注意 8080/8443 这样的替代 Web 端口；当前模拟器会把 Web 调查动作映射到剧情页面。",
            "内部告警页已经给出一次性训练身份。使用它完成模拟登录。",
        ],
        web_clue="/ops/drill.txt: 演练账户 range-ops；一次性训练口令 ember-731，仅适用于本模拟世界。",
        ssh_user="range-ops",
        ssh_password="ember-731",
        flag="FLAG{ghost_in_the_intranet}",
    ),
    "underground-market": Scenario(
        id="underground-market",
        name="地下交易市场",
        subtitle="匿名交易节点在封闭网络里重新上线，等待调查。",
        difficulty="困难",
        category="Web / Narrative Recon",
        target_ip="172.16.66.6",
        intro="红色霓虹从排水隧道尽头闪烁。一个只存在于模拟网络的交易节点重新出现。",
        briefing="建立服务画像、追踪留言板线索并获取用于剧情推进的模拟访问凭据。",
        services=[
            PortService(port=22, service="ssh", version="Dropbear 2022.83"),
            PortService(port=8000, service="http-alt", version="uvicorn"),
            PortService(port=9001, service="tor-orport", version="simulated relay"),
        ],
        objectives=[
            Objective(id="scan", title="勘察交易节点", description="记录虚构节点对外暴露的服务。"),
            Objective(id="web", title="读取留言板", description="寻找与节点运维有关的剧情线索。"),
            Objective(id="access", title="取得节点证据", description="使用模拟凭据进入 SSH 服务。"),
        ],
        hints=[
            "不要先猜剧情。先做侦察，确认节点真正暴露了什么。",
            "交易节点的 Web 服务不在标准 80 端口，但 Web 调查动作仍会解析到当前场景。",
            "留言板维护信息里藏着训练账户。最后一步是验证这条线索。",
        ],
        web_clue="/board/maintenance: 用户 broker-watch；训练密码 crimson-909。留言注明：仅用于纸上靶场。",
        ssh_user="broker-watch",
        ssh_password="crimson-909",
        flag="FLAG{market_after_midnight}",
    ),
}


def list_scenarios() -> list[Scenario]:
    return list(SCENARIOS.values())
