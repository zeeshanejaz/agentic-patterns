"""In-memory fake tools for the tool-use pattern. No real APIs."""

from __future__ import annotations

from typing import Any, Callable

ORDERS: dict[str, dict[str, Any]] = {
    "A-18422": {
        "item": "wireless headphones",
        "status": "processing",
        "paid": 89.0,
        "tracking": None,
        "duplicate_charge": False,
    },
    "A-18423": {
        "item": "wireless headphones",
        "status": "shipped",
        "paid": 89.0,
        "tracking": "1Z999AA10123456784",
        "duplicate_charge": False,
    },
}

DOCS = {
    "refund": "Refunds of $50 or less can be issued by the agent. Over $50 needs human approval.",
    "shipping": "Processing orders have no tracking yet. Shipped orders include a tracking number.",
    "cancel": (
        "Orders in processing can be cancelled. Shipped orders cannot; advise a return instead."
    ),
}


def lookup_order(order_id: str) -> str:
    key = order_id.strip().lstrip("#").upper()
    order = ORDERS.get(key)
    if not order:
        return f"No order found for {key}."
    tracking = order["tracking"] or "none"
    return (
        f"order={key} item={order['item']} status={order['status']} "
        f"paid={order['paid']} tracking={tracking} "
        f"duplicate_charge={order['duplicate_charge']}"
    )


def create_refund(order_id: str, amount: float) -> str:
    key = order_id.strip().lstrip("#").upper()
    if key not in ORDERS:
        return f"No order found for {key}."
    if amount > 50:
        return f"REFUSED: ${amount:.2f} is over $50 and needs human approval."
    return f"Refund of ${amount:.2f} recorded for {key} (fake; not sent to payments)."


def search_docs(query: str) -> str:
    q = query.lower()
    hits = [
        text
        for key, text in DOCS.items()
        if key in q or any(word in q for word in key.split())
    ]
    if not hits:
        hits = list(DOCS.values())
    return " ".join(hits)


TOOL_IMPLS: dict[str, Callable[..., str]] = {
    "lookup_order": lookup_order,
    "create_refund": create_refund,
    "search_docs": search_docs,
}

OPENAI_TOOLS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "lookup_order",
            "description": "Look up an order by id such as A-18422.",
            "parameters": {
                "type": "object",
                "properties": {"order_id": {"type": "string"}},
                "required": ["order_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_refund",
            "description": "Issue a refund. Amounts over $50 are refused.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string"},
                    "amount": {"type": "number"},
                },
                "required": ["order_id", "amount"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_docs",
            "description": "Search support policy docs (refund, shipping, cancel).",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    },
]


def call_tool(name: str, arguments: dict[str, Any]) -> str:
    impl = TOOL_IMPLS.get(name)
    if impl is None:
        return f"Unknown tool: {name}"
    return impl(**arguments)
