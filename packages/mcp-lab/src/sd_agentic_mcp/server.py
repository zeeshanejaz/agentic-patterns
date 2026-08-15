"""Support MCP server: tools, a policy resource, and a reusable prompt."""

from __future__ import annotations

from fastmcp import FastMCP

from sd_agentic_shared.prompts import POLICY
from sd_agentic_shared.tools import create_refund as _create_refund
from sd_agentic_shared.tools import lookup_order as _lookup_order
from sd_agentic_shared.tools import search_docs as _search_docs

SUPPORT_AGENT_PROMPT = f"""You are a support agent with MCP tools. Use tools before claiming facts.
{POLICY}
If lookup_order fails, say you could not find the order. Never invent tracking.
If create_refund is refused, tell the customer a human must approve it."""


def create_server() -> FastMCP:
    mcp = FastMCP(
        name="sd-agentic-support",
        instructions=(
            "In-memory support tools for the sd-agentic lab. "
            "Discover lookup_order, create_refund, and search_docs; "
            "read policy://support before promising refunds."
        ),
    )

    @mcp.tool
    def lookup_order(order_id: str) -> str:
        """Look up an order by id such as A-18422."""
        return _lookup_order(order_id)

    @mcp.tool
    def create_refund(order_id: str, amount: float) -> str:
        """Issue a refund. Amounts over $50 are refused and need human approval."""
        return _create_refund(order_id, amount)

    @mcp.tool
    def search_docs(query: str) -> str:
        """Search support policy docs (refund, shipping, cancel)."""
        return _search_docs(query)

    @mcp.resource("policy://support")
    def support_policy() -> str:
        """Current support policy text."""
        return POLICY

    @mcp.prompt
    def support_agent() -> str:
        """System prompt for a support agent that uses these tools."""
        return SUPPORT_AGENT_PROMPT

    return mcp


mcp = create_server()


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
