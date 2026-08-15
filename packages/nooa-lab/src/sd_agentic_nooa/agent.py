"""SupportAgent: shared fake tools are methods on self; handle() is CodeAct."""

from __future__ import annotations

from typing import Any

from nooa.agent import Agent
from nooa.unifiedllm.registry import get_llm_client

from sd_agentic_shared.env import load_env, openai_model
from sd_agentic_shared.prompts import POLICY
from sd_agentic_shared.tools import create_refund as _create_refund
from sd_agentic_shared.tools import lookup_order as _lookup_order
from sd_agentic_shared.tools import search_docs as _search_docs

_AGENT_DOC = f"""You are a support agent. Tools are methods on self.
{POLICY}
Use lookup_order, create_refund, and search_docs before claiming facts."""

_HANDLE_DOC = f"""Handle this customer support email. Use tools on self before claiming facts.
{POLICY}
If lookup_order fails, say you could not find the order. Never invent tracking.
If create_refund is refused, tell the customer a human must approve it.
Call self.lookup_order, self.create_refund, and self.search_docs as needed.
Return only the customer-facing email body."""


class SupportAgent(Agent):
    __doc__ = _AGENT_DOC

    def __init__(self, llm, **kwargs: Any) -> None:
        super().__init__(llm=llm, **kwargs)
        self.calls: list[dict[str, Any]] = []

    def lookup_order(self, order_id: str) -> str:
        """Look up an order by id such as A-18422."""
        result = _lookup_order(order_id)
        self.calls.append(
            {"name": "lookup_order", "arguments": {"order_id": order_id}, "result": result}
        )
        return result

    def create_refund(self, order_id: str, amount: float) -> str:
        """Issue a refund. Amounts over $50 are refused and need human approval."""
        result = _create_refund(order_id, amount)
        self.calls.append(
            {
                "name": "create_refund",
                "arguments": {"order_id": order_id, "amount": amount},
                "result": result,
            }
        )
        return result

    def search_docs(self, query: str) -> str:
        """Search support policy docs (refund, shipping, cancel)."""
        result = _search_docs(query)
        self.calls.append({"name": "search_docs", "arguments": {"query": query}, "result": result})
        return result

    async def handle(self, email: str) -> str:
        ...

    handle.__doc__ = _HANDLE_DOC


def make_support_agent() -> SupportAgent:
    load_env()
    return SupportAgent(llm=get_llm_client(openai_model()))
