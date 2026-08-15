"""Routing: classify intent, then send the email to one specialized handler."""

from __future__ import annotations

from langfuse import get_client, observe, propagate_attributes
from pydantic import BaseModel

from sd_agentic_patterns.llm import complete
from sd_agentic_shared.env import load_env
from sd_agentic_shared.prompts import (
    BILLING_HANDLER_SYSTEM,
    CANCEL_HANDLER_SYSTEM,
    OTHER_HANDLER_SYSTEM,
    ROUTE_SYSTEM,
    SHIPPING_HANDLER_SYSTEM,
)
from sd_agentic_shared.tasks.support_email import SAMPLE_EMAILS

load_env()

INTENTS = ("billing", "shipping", "cancel", "other")

HANDLERS: dict[str, str] = {
    "billing": BILLING_HANDLER_SYSTEM,
    "shipping": SHIPPING_HANDLER_SYSTEM,
    "cancel": CANCEL_HANDLER_SYSTEM,
    "other": OTHER_HANDLER_SYSTEM,
}


class RouteResult(BaseModel):
    intent: str
    reply: str


@observe(name="step.classify")
def classify(email: str) -> str:
    raw = complete(ROUTE_SYSTEM, email).strip().lower()
    token = raw.split()[0].strip(".,:;!?") if raw else "other"
    return token if token in INTENTS else "other"


@observe(name="step.handle")
def handle(intent: str, email: str) -> str:
    return complete(HANDLERS[intent], email)


@observe(name="pattern.routing")
def run(email: str) -> RouteResult:
    with propagate_attributes(
        tags=["backend:scratch", "pattern:routing"],
        metadata={"pattern": "routing", "backend": "scratch"},
    ):
        intent = classify(email)
        reply = handle(intent, email)
        return RouteResult(intent=intent, reply=reply)


def main() -> None:
    for label, email in SAMPLE_EMAILS.items():
        print(f"\n=== {label} ===")
        print(run(email).model_dump_json(indent=2))
    get_client().flush()


if __name__ == "__main__":
    main()
