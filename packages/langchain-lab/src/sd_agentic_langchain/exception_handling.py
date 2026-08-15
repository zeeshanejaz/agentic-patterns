"""Exception handling: wrap LangGraph tool use with retry / fallback / stop."""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_openai import ChatOpenAI
from langfuse import get_client, observe, propagate_attributes
from langfuse.langchain import CallbackHandler
from langgraph.errors import GraphRecursionError
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel

from sd_agentic_shared.env import load_env, openai_model
from sd_agentic_shared.prompts import EXCEPTION_FALLBACK_SYSTEM, POLICY
from sd_agentic_shared.tasks.support_email import SUPPORT_EMAIL
from sd_agentic_shared.tools import TOOL_IMPLS, call_tool

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


class RecoverState(TypedDict):
    messages: list
    stopped: bool
    fallback_reply: str


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


def _llm() -> ChatOpenAI:
    return ChatOpenAI(model=openai_model())


def _llm_with_tools():
    tools = [
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
    return _llm().bind_tools(tools)


def _fallback_reply(email: str, events: list[RecoveryEvent]) -> str:
    user = f"Email:\n{email}\n\nRecovery events:\n{events}"
    message = _llm().invoke(
        [SystemMessage(content=EXCEPTION_FALLBACK_SYSTEM), HumanMessage(content=user)]
    )
    content = message.content
    return content if isinstance(content, str) else str(content or "")


def _records_from_messages(messages: list) -> list[ToolCallRecord]:
    pending: dict[str, tuple[str, dict[str, Any]]] = {}
    calls: list[ToolCallRecord] = []
    for msg in messages:
        for tool_call in getattr(msg, "tool_calls", None) or []:
            call_id = tool_call.get("id") or ""
            pending[call_id] = (
                str(tool_call.get("name") or "unknown"),
                dict(tool_call.get("args") or {}),
            )
        if isinstance(msg, ToolMessage):
            name, arguments = pending.get(msg.tool_call_id, (msg.name or "unknown", {}))
            content = msg.content
            result = content if isinstance(content, str) else str(content)
            calls.append(ToolCallRecord(name=name, arguments=arguments, result=result))
    return calls


def _final_reply(messages: list) -> str:
    for msg in reversed(messages):
        if isinstance(msg, AIMessage) and not getattr(msg, "tool_calls", None):
            content = msg.content
            return content if isinstance(content, str) else str(content or "")
    return ""


def build_graph(recovery: Recovery, email: str):
    def agent_node(state: RecoverState) -> dict[str, list]:
        response = _llm_with_tools().invoke(state["messages"])
        return {"messages": [response]}

    def tools_node(state: RecoverState) -> dict[str, Any]:
        last = state["messages"][-1]
        new_messages: list = []
        for tool_call in getattr(last, "tool_calls", None) or []:
            name = str(tool_call.get("name") or "unknown")
            arguments = dict(tool_call.get("args") or {})
            call_id = str(tool_call.get("id") or "")
            try:
                result = recovery.execute(name, arguments)
            except CriticalError:
                return {
                    "stopped": True,
                    "fallback_reply": _fallback_reply(email, recovery.events),
                    "messages": new_messages,
                }
            new_messages.append(
                ToolMessage(content=result, tool_call_id=call_id, name=name)
            )
        return {"messages": new_messages}

    def route_after_agent(state: RecoverState) -> Literal["tools", "end"]:
        last = state["messages"][-1]
        if getattr(last, "tool_calls", None):
            return "tools"
        return "end"

    def route_after_tools(state: RecoverState) -> Literal["agent", "end"]:
        return "end" if state.get("stopped") else "agent"

    graph = StateGraph(RecoverState)
    graph.add_node("agent", agent_node)
    graph.add_node("tools", tools_node)
    graph.add_edge(START, "agent")
    graph.add_conditional_edges(
        "agent",
        route_after_agent,
        {"tools": "tools", "end": END},
    )
    graph.add_conditional_edges(
        "tools",
        route_after_tools,
        {"agent": "agent", "end": END},
    )
    return graph.compile()


@observe(name="pattern.exception_handling")
def run(email: str | None = None) -> ExceptionHandlingResult:
    ticket = email if email is not None else SUPPORT_EMAIL
    with propagate_attributes(
        tags=["backend:langchain", "pattern:exception_handling"],
        metadata={"pattern": "exception_handling", "backend": "langchain"},
    ):
        handler = CallbackHandler()
        recovery = Recovery()
        try:
            result = build_graph(recovery, ticket).invoke(
                {
                    "messages": [
                        SystemMessage(content=SYSTEM),
                        HumanMessage(content=ticket),
                    ],
                    "stopped": False,
                    "fallback_reply": "",
                },
                config={
                    "callbacks": [handler],
                    "recursion_limit": MAX_STEPS * 2,
                },
            )
            stopped = bool(result.get("stopped"))
            reply = (
                result.get("fallback_reply")
                if stopped and result.get("fallback_reply")
                else _final_reply(result["messages"])
            )
            return ExceptionHandlingResult(
                events=recovery.events,
                calls=_records_from_messages(result["messages"]),
                reply=reply or "",
                stopped=stopped,
            )
        except GraphRecursionError:
            return ExceptionHandlingResult(
                events=recovery.events,
                calls=[],
                reply="Stopped: too many tool steps.",
                stopped=True,
            )


def main() -> None:
    print(run().model_dump_json(indent=2))
    get_client().flush()


if __name__ == "__main__":
    main()
