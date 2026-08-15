"""Tool use with a MAF Agent bound to the shared fake support tools. Traces via OTEL."""

from __future__ import annotations

import asyncio
from typing import Any

from agent_framework import Agent, FunctionInvocationContext, FunctionMiddleware
from agent_framework.observability import get_tracer
from agent_framework.openai import OpenAIChatClient
from opentelemetry import trace
from pydantic import BaseModel

from sd_agentic_maf.otel import configure_maf_otel
from sd_agentic_shared.env import load_env, openai_model, workspace_root
from sd_agentic_shared.prompts import POLICY
from sd_agentic_shared.tasks.support_email import SUPPORT_EMAIL
from sd_agentic_shared.tools import create_refund, lookup_order, search_docs

load_env()
_OTEL_READY = False

SYSTEM = f"""You are a support agent with tools. Use tools before claiming facts.
{POLICY}
If lookup_order fails, say you could not find the order. Never invent tracking.
If create_refund is refused, tell the customer a human must approve it."""


class ToolCallRecord(BaseModel):
    name: str
    arguments: dict[str, Any]
    result: str


class ToolUseResult(BaseModel):
    calls: list[ToolCallRecord]
    reply: str


class RecordTools(FunctionMiddleware):
    def __init__(self) -> None:
        self.calls: list[ToolCallRecord] = []

    async def process(self, context: FunctionInvocationContext, call_next) -> None:
        await call_next()
        arguments = context.arguments
        if hasattr(arguments, "model_dump"):
            args = arguments.model_dump()
        elif isinstance(arguments, dict):
            args = dict(arguments)
        else:
            args = dict(getattr(arguments, "__dict__", {}) or {})
        result = context.result
        self.calls.append(
            ToolCallRecord(
                name=context.function.name,
                arguments=args,
                result="" if result is None else str(result),
            )
        )


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


async def run(email: str) -> ToolUseResult:
    _ensure_otel()
    recorder = RecordTools()
    agent = Agent(
        client=_client(),
        name="support",
        instructions=SYSTEM,
        tools=[lookup_order, create_refund, search_docs],
        middleware=[recorder],
    )
    with get_tracer().start_as_current_span("pattern.tool_use") as span:
        span.set_attribute("pattern", "tool_use")
        span.set_attribute("backend", "maf")
        response = await agent.run(email)
        return ToolUseResult(calls=recorder.calls, reply=response.text or "")


def main() -> None:
    print(asyncio.run(run(SUPPORT_EMAIL)).model_dump_json(indent=2))
    provider = trace.get_tracer_provider()
    flush = getattr(provider, "force_flush", None)
    if callable(flush):
        flush()


if __name__ == "__main__":
    main()
