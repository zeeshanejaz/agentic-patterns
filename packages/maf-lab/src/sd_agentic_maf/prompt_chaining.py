"""Prompt chaining with MAF SequentialBuilder. Traces export via OTEL to Langfuse."""

from __future__ import annotations

import asyncio

from agent_framework import Agent
from agent_framework.observability import get_tracer
from agent_framework.openai import OpenAIChatClient
from agent_framework.orchestrations import SequentialBuilder
from opentelemetry import trace

from sd_agentic_maf.otel import configure_maf_otel
from sd_agentic_shared.env import load_env, openai_model, workspace_root
from sd_agentic_shared.prompts import CHECK_SYSTEM, DRAFT_SYSTEM, SUMMARIZE_SYSTEM
from sd_agentic_shared.tasks.support_email import SUPPORT_EMAIL, TicketDraft

load_env()
_OTEL_READY = False


def _ensure_otel() -> None:
    global _OTEL_READY
    if not _OTEL_READY:
        configure_maf_otel()
        _OTEL_READY = True


def _response_text(item: object) -> str:
    text = getattr(item, "text", None)
    if text:
        return str(text)
    return str(item)


def build_workflow():
    client = OpenAIChatClient(
        model=openai_model(),
        env_file_path=str(workspace_root() / ".env"),
    )
    summarizer = Agent(client=client, name="summarizer", instructions=SUMMARIZE_SYSTEM)
    drafter = Agent(client=client, name="drafter", instructions=DRAFT_SYSTEM)
    checker = Agent(client=client, name="checker", instructions=CHECK_SYSTEM)
    return SequentialBuilder(
        participants=[summarizer, drafter, checker],
        output_from="all",
    ).build()


async def run(email: str) -> TicketDraft:
    _ensure_otel()
    workflow = build_workflow()
    with get_tracer().start_as_current_span("pattern.prompt_chaining"):
        events = await workflow.run(email)
        outputs = events.get_outputs()
        texts = [_response_text(item) for item in outputs]
        summary = texts[0] if len(texts) > 0 else ""
        reply = texts[1] if len(texts) > 1 else ""
        policy_ok = texts[2] if len(texts) > 2 else (texts[-1] if texts else "")
        return TicketDraft(summary=summary, reply=reply, policy_ok=policy_ok)


def main() -> None:
    result = asyncio.run(run(SUPPORT_EMAIL))
    print(result.model_dump_json(indent=2))
    provider = trace.get_tracer_provider()
    flush = getattr(provider, "force_flush", None)
    if callable(flush):
        flush()


if __name__ == "__main__":
    main()
