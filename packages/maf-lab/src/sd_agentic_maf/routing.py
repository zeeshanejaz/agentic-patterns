"""Routing with a MAF classifier Agent then one specialist Agent. Traces export via OTEL."""

from __future__ import annotations

import asyncio

from agent_framework import Agent
from agent_framework.observability import get_tracer
from agent_framework.openai import OpenAIChatClient
from opentelemetry import trace
from pydantic import BaseModel

from sd_agentic_maf.otel import configure_maf_otel
from sd_agentic_shared.env import load_env, openai_model, workspace_root
from sd_agentic_shared.prompts import (
    BILLING_HANDLER_SYSTEM,
    CANCEL_HANDLER_SYSTEM,
    OTHER_HANDLER_SYSTEM,
    ROUTE_SYSTEM,
    SHIPPING_HANDLER_SYSTEM,
)
from sd_agentic_shared.tasks.support_email import SAMPLE_EMAILS

load_env()
_OTEL_READY = False

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


def _ensure_otel() -> None:
    global _OTEL_READY
    if not _OTEL_READY:
        configure_maf_otel()
        _OTEL_READY = True


def _parse_intent(raw: str) -> str:
    token = raw.strip().lower().split()[0].strip(".,:;!?") if raw.strip() else "other"
    return token if token in INTENTS else "other"


def _client() -> OpenAIChatClient:
    return OpenAIChatClient(
        model=openai_model(),
        env_file_path=str(workspace_root() / ".env"),
    )


def build_agents() -> tuple[Agent, dict[str, Agent]]:
    client = _client()
    router = Agent(client=client, name="router", instructions=ROUTE_SYSTEM)
    specialists = {
        intent: Agent(client=client, name=intent, instructions=system)
        for intent, system in HANDLERS.items()
    }
    return router, specialists


async def run(email: str) -> RouteResult:
    _ensure_otel()
    router, specialists = build_agents()
    with get_tracer().start_as_current_span("pattern.routing") as span:
        span.set_attribute("pattern", "routing")
        span.set_attribute("backend", "maf")
        classified = await router.run(email)
        intent = _parse_intent(classified.text or "")
        handled = await specialists[intent].run(email)
        return RouteResult(intent=intent, reply=handled.text or "")


def main() -> None:
    for label, email in SAMPLE_EMAILS.items():
        print(f"\n=== {label} ===")
        print(asyncio.run(run(email)).model_dump_json(indent=2))
    provider = trace.get_tracer_provider()
    flush = getattr(provider, "force_flush", None)
    if callable(flush):
        flush()


if __name__ == "__main__":
    main()
