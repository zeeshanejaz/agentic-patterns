"""Tool use: LangGraph agent ⇄ ToolNode with the shared fake support tools."""

from __future__ import annotations

from typing import Any

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import StructuredTool
from langchain_openai import ChatOpenAI
from langfuse import get_client, observe, propagate_attributes
from langfuse.langchain import CallbackHandler
from langgraph.errors import GraphRecursionError
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from pydantic import BaseModel

from sd_agentic_shared.env import load_env, openai_model
from sd_agentic_shared.prompts import POLICY
from sd_agentic_shared.tasks.support_email import SUPPORT_EMAIL
from sd_agentic_shared.tools import create_refund, lookup_order, search_docs

load_env()

MAX_STEPS = 6

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


TOOLS = [
    StructuredTool.from_function(lookup_order),
    StructuredTool.from_function(create_refund),
    StructuredTool.from_function(search_docs),
]


def _llm_with_tools():
    return ChatOpenAI(model=openai_model()).bind_tools(TOOLS)


def agent_node(state: MessagesState) -> dict[str, list]:
    response = _llm_with_tools().invoke(state["messages"])
    return {"messages": [response]}


def build_graph():
    graph = StateGraph(MessagesState)
    graph.add_node("agent", agent_node)
    graph.add_node("tools", ToolNode(TOOLS))
    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", tools_condition, {"tools": "tools", END: END})
    graph.add_edge("tools", "agent")
    return graph.compile()


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
            name, arguments = pending.get(
                msg.tool_call_id,
                (msg.name or "unknown", {}),
            )
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


@observe(name="pattern.tool_use")
def run(email: str) -> ToolUseResult:
    with propagate_attributes(
        tags=["backend:langchain", "pattern:tool_use"],
        metadata={"pattern": "tool_use", "backend": "langchain"},
    ):
        handler = CallbackHandler()
        graph = build_graph()
        try:
            result = graph.invoke(
                {
                    "messages": [
                        SystemMessage(content=SYSTEM),
                        HumanMessage(content=email),
                    ]
                },
                config={
                    "callbacks": [handler],
                    "recursion_limit": MAX_STEPS * 2,
                },
            )
            messages = result["messages"]
            return ToolUseResult(
                calls=_records_from_messages(messages),
                reply=_final_reply(messages),
            )
        except GraphRecursionError:
            return ToolUseResult(calls=[], reply="Stopped: too many tool steps.")


def main() -> None:
    print(run(SUPPORT_EMAIL).model_dump_json(indent=2))
    get_client().flush()


if __name__ == "__main__":
    main()
