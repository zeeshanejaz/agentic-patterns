"""Exception handling wrapping MAF tool use. Traces via OTEL."""

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
from sd_agentic_shared.prompts import EXCEPTION_FALLBACK_SYSTEM, POLICY
from sd_agentic_shared.tasks.support_email import SUPPORT_EMAIL
from sd_agentic_shared.tools import TOOL_IMPLS, call_tool

load_env()
_OTEL_READY = False

MAX_RETRIES = 2
MAX_EVENTS = 12
LOOKUP_TIMEOUTS = 2
BACKOFF_SECONDS = 0

SYSTEM = f"""You are a support agent with tools. Use tools before claiming facts.
{POLICY}
If lookup_order fails, say you could not find the order. Never invent tracking.
If create_refund is refused, tell the customer a human must approve it."""


class TransientError(Exception):
    def __init__(self, kind: str) -> None:
        super().__init__(kind)
        self.kind = kind


class PermanentError(Exception):
    def __init__(self, kind: str) -> None:
        super().__init__(kind)
        self.kind = kind


class CriticalError(Exception):
    def __init__(self, kind: str) -> None:
        super().__init__(kind)
        self.kind = kind


class RecoveryEvent(BaseModel):
    tool: str
    error: str | None
    classification: str
    action: str
    attempt: int


class ToolCallRecord(BaseModel):
    name: str
    arguments: dict[str, Any]
    result: str


class ExceptionHandlingResult(BaseModel):
    events: list[RecoveryEvent]
    calls: list[ToolCallRecord]
    reply: str
    stopped: bool


class Recovery:
    def __init__(self) -> None:
        self.lookup_timeouts_left = LOOKUP_TIMEOUTS
        self.events: list[RecoveryEvent] = []

    def _record(
        self,
        tool: str,
        error: str | None,
        classification: str,
        action: str,
        attempt: int,
    ) -> None:
        self.events.append(
            RecoveryEvent(
                tool=tool,
                error=error,
                classification=classification,
                action=action,
                attempt=attempt,
            )
        )

    def _guard(self) -> None:
        if len(self.events) >= MAX_EVENTS:
            self._record("*", "max_events", "critical", "emergency_stop", 0)
            raise CriticalError("max_events")

    def _raw_call(self, name: str, arguments: dict[str, Any]) -> str:
        if name == "lookup_order" and self.lookup_timeouts_left > 0:
            self.lookup_timeouts_left -= 1
            raise TransientError("timeout")
        if name not in TOOL_IMPLS:
            raise PermanentError("unknown_tool")
        return call_tool(name, arguments)

    def _fallback(self, failed_name: str) -> str:
        _ = failed_name
        try:
            return call_tool("search_docs", {"query": "shipping"})
        except (TypeError, ValueError):
            return "FALLBACK: could not complete the tool call."

    def execute(self, name: str, arguments: dict[str, Any]) -> str:
        last_kind = "timeout"
        for attempt in range(1, MAX_RETRIES + 2):
            self._guard()
            try:
                result = self._raw_call(name, arguments)
                if attempt > 1:
                    self._record(name, None, "ok", "success", attempt)
                return result
            except TransientError as exc:
                last_kind = exc.kind
                self._record(name, exc.kind, "transient", "retry", attempt)
                _ = BACKOFF_SECONDS
                continue
            except PermanentError as exc:
                self._record(name, exc.kind, "permanent", "fallback", attempt)
                return self._fallback(name)
        self._record(name, last_kind, "transient", "fallback", MAX_RETRIES + 1)
        return self._fallback(name)


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


def _wrap_tools(recovery: Recovery) -> list:
    def lookup_order(order_id: str) -> str:
        """Look up an order by id such as A-18422."""
        return recovery.execute("lookup_order", {"order_id": order_id})

    def create_refund(order_id: str, amount: float) -> str:
        """Issue a refund. Amounts over $50 are refused."""
        return recovery.execute("create_refund", {"order_id": order_id, "amount": amount})

    def search_docs(query: str) -> str:
        """Search support policy docs (refund, shipping, cancel)."""
        return recovery.execute("search_docs", {"query": query})

    return [lookup_order, create_refund, search_docs]


async def run(email: str | None = None) -> ExceptionHandlingResult:
    ticket = email if email is not None else SUPPORT_EMAIL
    _ensure_otel()
    recovery = Recovery()
    recorder = RecordTools()
    agent = Agent(
        client=_client(),
        name="support",
        instructions=SYSTEM,
        tools=_wrap_tools(recovery),
        middleware=[recorder],
    )
    fallback = Agent(
        client=_client(),
        name="fallback",
        instructions=EXCEPTION_FALLBACK_SYSTEM,
    )
    with get_tracer().start_as_current_span("pattern.exception_handling") as span:
        span.set_attribute("pattern", "exception_handling")
        span.set_attribute("backend", "maf")
        try:
            response = await agent.run(ticket)
            return ExceptionHandlingResult(
                events=recovery.events,
                calls=recorder.calls,
                reply=response.text or "",
                stopped=False,
            )
        except CriticalError:
            reply = (
                await fallback.run(
                    f"Email:\n{ticket}\n\nRecovery events:\n{recovery.events}"
                )
            ).text or ""
            return ExceptionHandlingResult(
                events=recovery.events,
                calls=recorder.calls,
                reply=reply,
                stopped=True,
            )


def main() -> None:
    print(asyncio.run(run()).model_dump_json(indent=2))
    provider = trace.get_tracer_provider()
    flush = getattr(provider, "force_flush", None)
    if callable(flush):
        flush()


if __name__ == "__main__":
    main()
