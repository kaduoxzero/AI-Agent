from __future__ import annotations

from mcp.server import MCPServer


mcp = MCPServer(
    "Supplier Risk MCP",
    instructions="Read supplier context before producing supplier-risk conclusions.",
)


SUPPLIERS = {
    "s-001": {
        "name": "Acme Components",
        "country": "CN",
        "late_deliveries_30d": 3,
        "incidents_90d": 1,
    },
    "s-002": {
        "name": "North Star Parts",
        "country": "US",
        "late_deliveries_30d": 0,
        "incidents_90d": 0,
    },
}


@mcp.tool()
def calculate_risk_score(delays: int, incidents: int) -> dict[str, int | str]:
    """Calculate a deterministic supplier risk score from delivery delays and incidents."""
    delays = max(delays, 0)
    incidents = max(incidents, 0)
    score = min(100, delays * 12 + incidents * 25)
    level = "high" if score >= 60 else "medium" if score >= 30 else "low"
    return {"score": score, "level": level}


@mcp.tool()
def get_supplier_risk(supplier_id: str) -> dict[str, object]:
    """Return supplier facts plus a deterministic risk score."""
    supplier = SUPPLIERS.get(supplier_id)
    if supplier is None:
        return {"found": False, "supplier_id": supplier_id}

    risk = calculate_risk_score(
        delays=int(supplier["late_deliveries_30d"]),
        incidents=int(supplier["incidents_90d"]),
    )
    return {
        "found": True,
        "supplier_id": supplier_id,
        "supplier": supplier,
        "risk": risk,
    }


@mcp.resource("supplier://{supplier_id}")
def supplier_resource(supplier_id: str) -> str:
    """Read the canonical supplier record as text context."""
    supplier = SUPPLIERS.get(supplier_id)
    if supplier is None:
        return f"supplier {supplier_id} not found"
    return (
        f"name={supplier['name']}; country={supplier['country']}; "
        f"late_deliveries_30d={supplier['late_deliveries_30d']}; "
        f"incidents_90d={supplier['incidents_90d']}"
    )


if __name__ == "__main__":
    # 开发环境可直接运行；生产环境建议挂载到受认证和治理的 ASGI 服务。
    mcp.run(transport="streamable-http")
