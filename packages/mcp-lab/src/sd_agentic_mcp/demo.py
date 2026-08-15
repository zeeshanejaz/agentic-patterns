"""In-process MCP client: list tools/resources/prompts and call lookup_order."""

from __future__ import annotations

import asyncio
import json

from fastmcp import Client

from sd_agentic_mcp.server import create_server


def _schema(tool) -> dict:
    return getattr(tool, "inputSchema", None) or getattr(tool, "input_schema", {}) or {}


def _text(result) -> str:
    data = getattr(result, "data", None)
    if data is not None:
        return str(data)
    content = getattr(result, "content", None) or []
    parts = [getattr(item, "text", str(item)) for item in content]
    return "\n".join(parts) if parts else str(result)


async def demo() -> dict:
    server = create_server()
    async with Client(server) as client:
        tools = await client.list_tools()
        resources = await client.list_resources()
        prompts = await client.list_prompts()
        order = await client.call_tool("lookup_order", {"order_id": "A-18422"})
        refused = await client.call_tool(
            "create_refund",
            {"order_id": "A-18422", "amount": 89.0},
        )
        policy = await client.read_resource("policy://support")
        policy_text = policy[0].text if policy else ""
        return {
            "tools": [
                {"name": t.name, "description": t.description, "schema": _schema(t)}
                for t in tools
            ],
            "resources": [str(getattr(r, "uri", r)) for r in resources],
            "prompts": [p.name for p in prompts],
            "lookup_order": _text(order),
            "create_refund_over_50": _text(refused),
            "policy": policy_text,
        }


def main() -> None:
    print(json.dumps(asyncio.run(demo()), indent=2))


if __name__ == "__main__":
    main()
