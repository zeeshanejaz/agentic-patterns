"""Tool use via OO-Agents CodeAct: methods on self instead of a tool schema."""

from __future__ import annotations

import asyncio
from typing import Any

from opentelemetry import trace
from pydantic import BaseModel

from sd_agentic_nooa.agent import make_support_agent
from sd_agentic_nooa.tracing import configure_nooa_tracing, flush_nooa_traces
from sd_agentic_shared.tasks.support_email import SUPPORT_EMAIL


class ToolCallRecord(BaseModel):
    name: str
    arguments: dict[str, Any]
    result: str


class ToolUseResult(BaseModel):
    calls: list[ToolCallRecord]
    reply: str


async def run(email: str) -> ToolUseResult:
    configure_nooa_tracing()
    agent = make_support_agent()
    tracer = trace.get_tracer("sd_agentic_nooa")
    with tracer.start_as_current_span("pattern.tool_use") as span:
        span.set_attribute("pattern", "tool_use")
        span.set_attribute("backend", "nooa")
        span.set_attribute("langfuse.trace.tags", ["pattern:tool_use", "backend:nooa"])
        reply = await agent.handle(email)
        return ToolUseResult(
            calls=[ToolCallRecord.model_validate(call) for call in agent.calls],
            reply=reply or "",
        )


def main() -> None:
    print(asyncio.run(run(SUPPORT_EMAIL)).model_dump_json(indent=2))
    flush_nooa_traces()


if __name__ == "__main__":
    main()
