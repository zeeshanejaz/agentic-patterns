"""Resource-aware cheap vs expensive paths with MAF Agents. Traces via OTEL."""

from __future__ import annotations

import asyncio
import math
import re

from agent_framework import Agent
from agent_framework.observability import get_tracer
from agent_framework.openai import OpenAIChatClient
from opentelemetry import trace
from pydantic import BaseModel

from sd_agentic_maf.otel import configure_maf_otel
from sd_agentic_shared.env import load_env, openai_model, workspace_root
from sd_agentic_shared.prompts import (
    RESOURCE_CHEAP_SYSTEM,
    RESOURCE_CLASSIFY_SYSTEM,
    RESOURCE_EXPENSIVE_SYSTEM,
)
from sd_agentic_shared.tasks.support_email import SAMPLE_EMAILS

load_env()
_OTEL_READY = False

CHEAP_FEE = 1
EXPENSIVE_FEE = 4


class ResourceResult(BaseModel):
    label: str
    route: str
    cost_units: int
    reply: str


def _ensure_otel() -> None:
    global _OTEL_READY
    if not _OTEL_READY:
        configure_maf_otel()
        _OTEL_READY = True


def _client() -> OpenAIChatClient:
    return OpenAIChatClient(
        model=openai_model(),
        env_file_path=str(workspace_root() / ".env"),
    )


def _refund_over_50(text: str) -> bool:
    blob = text.lower()
    if "refund" not in blob and "chargeback" not in blob:
        return False
    for match in re.findall(r"\$(\d+(?:\.\d+)?)", blob):
        if float(match) > 50:
            return True
    return "full refund" in blob


def _parse_route(email: str, raw: str) -> str:
    if _refund_over_50(email):
        return "complex"
    token = raw.strip().lower().split()[0].strip(".,:;!?") if raw.strip() else "complex"
    return token if token in {"simple", "complex"} else "complex"


def _cost(route: str, reply: str) -> int:
    fee = CHEAP_FEE if route == "simple" else EXPENSIVE_FEE
    return fee + math.ceil(max(len(reply), 1) / 100)


async def run(email: str, label: str = "ticket") -> ResourceResult:
    _ensure_otel()
    client = _client()
    agents = {
        "classify": Agent(client=client, name="classify", instructions=RESOURCE_CLASSIFY_SYSTEM),
        "cheap": Agent(client=client, name="cheap", instructions=RESOURCE_CHEAP_SYSTEM),
        "expensive": Agent(client=client, name="expensive", instructions=RESOURCE_EXPENSIVE_SYSTEM),
    }
    with get_tracer().start_as_current_span("pattern.resource_aware") as span:
        span.set_attribute("pattern", "resource_aware")
        span.set_attribute("backend", "maf")
        span.set_attribute("label", label)
        raw = (await agents["classify"].run(email)).text or ""
        route = _parse_route(email, raw)
        agent = agents["cheap"] if route == "simple" else agents["expensive"]
        reply = (await agent.run(email)).text or ""
        return ResourceResult(
            label=label,
            route=route,
            cost_units=_cost(route, reply),
            reply=reply,
        )


def main() -> None:
    async def _all() -> None:
        for label, email in SAMPLE_EMAILS.items():
            print(f"\n=== {label} ===")
            print((await run(email, label)).model_dump_json(indent=2))

    asyncio.run(_all())
    provider = trace.get_tracer_provider()
    flush = getattr(provider, "force_flush", None)
    if callable(flush):
        flush()


if __name__ == "__main__":
    main()
