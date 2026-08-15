"""Exception handling: wrap tool use with classify, retry, fallback, and stop."""

from __future__ import annotations

import json
from typing import Any

from langfuse import get_client, observe, propagate_attributes
from langfuse.openai import openai
from pydantic import BaseModel

from sd_agentic_patterns.llm import complete
from sd_agentic_shared.env import load_env, openai_model
from sd_agentic_shared.prompts import EXCEPTION_FALLBACK_SYSTEM, POLICY
from sd_agentic_shared.tasks.support_email import SUPPORT_EMAIL
from sd_agentic_shared.tools import OPENAI_TOOLS, TOOL_IMPLS, call_tool

load_env()

MAX_STEPS = 6
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


@observe(as_type="tool", name="tool.execute")
def execute_tool(recovery: Recovery, name: str, arguments: dict[str, Any]) -> str:
    return recovery.execute(name, arguments)


@observe(name="pattern.exception_handling")
def run(email: str | None = None) -> ExceptionHandlingResult:
    ticket = email if email is not None else SUPPORT_EMAIL
    with propagate_attributes(
        tags=["backend:scratch", "pattern:exception_handling"],
        metadata={"pattern": "exception_handling", "backend": "scratch"},
    ):
        recovery = Recovery()
        messages: list[dict[str, Any]] = [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": ticket},
        ]
        calls: list[ToolCallRecord] = []
        reply = ""
        stopped = False

        for _ in range(MAX_STEPS):
            response = openai.chat.completions.create(
                model=openai_model(),
                messages=messages,
                tools=OPENAI_TOOLS,
            )
            message = response.choices[0].message
            assistant: dict[str, Any] = {"role": "assistant", "content": message.content}
            if message.tool_calls:
                assistant["tool_calls"] = [
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments,
                        },
                    }
                    for tool_call in message.tool_calls
                ]
            messages.append(assistant)

            if not message.tool_calls:
                reply = message.content or ""
                break

            halt = False
            for tool_call in message.tool_calls:
                name = tool_call.function.name
                try:
                    arguments = json.loads(tool_call.function.arguments or "{}")
                except json.JSONDecodeError:
                    arguments = {}
                try:
                    result = execute_tool(recovery, name, arguments)
                except CriticalError:
                    stopped = True
                    halt = True
                    reply = complete(
                        EXCEPTION_FALLBACK_SYSTEM,
                        f"Email:\n{ticket}\n\nRecovery events:\n{recovery.events}",
                    )
                    break
                calls.append(ToolCallRecord(name=name, arguments=arguments, result=result))
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    }
                )
            if halt:
                break
        else:
            reply = "Stopped: too many tool steps."
            stopped = True

        return ExceptionHandlingResult(
            events=recovery.events,
            calls=calls,
            reply=reply,
            stopped=stopped,
        )


def main() -> None:
    print(run().model_dump_json(indent=2))
    get_client().flush()


if __name__ == "__main__":
    main()
