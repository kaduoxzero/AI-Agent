from __future__ import annotations

import pytest
from mcp import Client

from server import mcp


@pytest.mark.anyio
async def test_get_supplier_risk() -> None:
    async with Client(mcp) as client:
        result = await client.call_tool("get_supplier_risk", {"supplier_id": "s-001"})

    assert result.is_error is False
    assert result.structured_content is not None

    # MCP SDK 可能将非对象返回值包装进 result；对象返回通常可以直接读取。
    payload = result.structured_content.get("result", result.structured_content)
    assert payload["found"] is True
    assert payload["supplier_id"] == "s-001"
    assert payload["risk"]["level"] in {"low", "medium", "high"}


@pytest.mark.anyio
async def test_unknown_supplier_is_explicit() -> None:
    async with Client(mcp) as client:
        result = await client.call_tool("get_supplier_risk", {"supplier_id": "missing"})

    assert result.is_error is False
    assert result.structured_content is not None
    payload = result.structured_content.get("result", result.structured_content)
    assert payload["found"] is False
