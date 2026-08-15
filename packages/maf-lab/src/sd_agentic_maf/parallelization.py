"""Parallelization with MAF ConcurrentBuilder, then a merge Agent. Traces via OTEL."""

from __future__ import annotations

import asyncio

from agent_framework import Agent
from agent_framework.observability import get_tracer
from agent_framework.openai import OpenAIChatClient
from agent_framework.orchestrations import ConcurrentBuilder
from opentelemetry import trace
from pydantic import BaseModel

from sd_agentic_maf.otel import configure_maf_otel
from sd_agentic_shared.env import load_env, openai_model, workspace_root
from sd_agentic_shared.prompts import (
    MERGE_SECTIONS_SYSTEM,
    SECTION_ASK_SYSTEM,
    SECTION_ORDER_SYSTEM,
    SECTION_PAYMENT_SYSTEM,
    VOTE_MERGE_SYSTEM,
)
from sd_agentic_shared.tasks.support_email import SUPPORT_EMAIL

load_env()
_OTEL_READY = False

VOTE_WORKER_SYSTEM = (
    "Write a short support reply to the email. Do not invent tracking, "
    "order status, or refund amounts. Worker {index}."
)


class SectionResult(BaseModel):
    order: str
    payment: str
    ask: str
    summary: str


class VoteResult(BaseModel):
    drafts: list[str]
    merged: str


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


def _texts_by_name(results: list, names: tuple[str, ...]) -> dict[str, str]:
    by_id = {r.executor_id: (r.agent_response.text or "") for r in results}
    out: dict[str, str] = {}
    unused = dict(by_id)
    for name in names:
        match_id = next((eid for eid in unused if name == eid or eid.endswith(name)), None)
        if match_id is None:
            match_id = next(iter(unused), None)
        out[name] = unused.pop(match_id, "") if match_id else ""
    return out


def _first_output(events) -> object:
    outputs = events.get_outputs()
    return outputs[0] if outputs else {}


async def run_sectioning(email: str) -> SectionResult:
    _ensure_otel()
    client = _client()
    names = ("order", "payment", "ask")
    agents = [
        Agent(client=client, name="order", instructions=SECTION_ORDER_SYSTEM),
        Agent(client=client, name="payment", instructions=SECTION_PAYMENT_SYSTEM),
        Agent(client=client, name="ask", instructions=SECTION_ASK_SYSTEM),
    ]
    merger = Agent(client=client, name="merge_sections", instructions=MERGE_SECTIONS_SYSTEM)
    workflow = ConcurrentBuilder(participants=agents).with_aggregator(
        lambda results: _texts_by_name(results, names)
    ).build()
    with get_tracer().start_as_current_span("pattern.parallelization.sectioning") as span:
        span.set_attribute("pattern", "parallelization")
        span.set_attribute("backend", "maf")
        events = await workflow.run(email)
        parts = _first_output(events)
        if not isinstance(parts, dict):
            parts = {}
        order = str(parts.get("order", ""))
        payment = str(parts.get("payment", ""))
        ask = str(parts.get("ask", ""))
        user = f"Order facts:\n{order}\n\nPayment facts:\n{payment}\n\nCustomer ask:\n{ask}"
        merged = await merger.run(user)
        return SectionResult(order=order, payment=payment, ask=ask, summary=merged.text or "")


async def run_voting(email: str, n: int = 3) -> VoteResult:
    _ensure_otel()
    client = _client()
    names = tuple(f"draft_{i}" for i in range(1, n + 1))
    agents = [
        Agent(
            client=client,
            name=name,
            instructions=VOTE_WORKER_SYSTEM.format(index=i),
        )
        for i, name in enumerate(names, start=1)
    ]
    merger = Agent(client=client, name="vote_merge", instructions=VOTE_MERGE_SYSTEM)
    workflow = ConcurrentBuilder(participants=agents).with_aggregator(
        lambda results: _texts_by_name(results, names)
    ).build()
    with get_tracer().start_as_current_span("pattern.parallelization.voting") as span:
        span.set_attribute("pattern", "parallelization")
        span.set_attribute("backend", "maf")
        events = await workflow.run(email)
        parts = _first_output(events)
        if not isinstance(parts, dict):
            parts = {}
        drafts = [str(parts.get(name, "")) for name in names]
        numbered = "\n\n".join(f"Draft {i}:\n{d}" for i, d in enumerate(drafts, start=1))
        merged = await merger.run(f"Original email:\n{email}\n\n{numbered}")
        return VoteResult(drafts=drafts, merged=merged.text or "")


def main() -> None:
    print("=== sectioning ===")
    print(asyncio.run(run_sectioning(SUPPORT_EMAIL)).model_dump_json(indent=2))
    print("\n=== voting ===")
    print(asyncio.run(run_voting(SUPPORT_EMAIL)).model_dump_json(indent=2))
    provider = trace.get_tracer_provider()
    flush = getattr(provider, "force_flush", None)
    if callable(flush):
        flush()


if __name__ == "__main__":
    main()
