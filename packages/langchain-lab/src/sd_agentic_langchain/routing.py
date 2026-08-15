"""Routing with a LangGraph classify node and conditional handler edges."""

from __future__ import annotations

from typing import TypedDict

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langfuse import get_client, observe, propagate_attributes
from langfuse.langchain import CallbackHandler
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel

from sd_agentic_shared.env import load_env, openai_model
from sd_agentic_shared.prompts import (
    BILLING_HANDLER_SYSTEM,
    CANCEL_HANDLER_SYSTEM,
    OTHER_HANDLER_SYSTEM,
    ROUTE_SYSTEM,
    SHIPPING_HANDLER_SYSTEM,
)
from sd_agentic_shared.tasks.support_email import SAMPLE_EMAILS

load_env()

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


class RouteState(TypedDict):
    email: str
    intent: str
    reply: str


def _llm() -> ChatOpenAI:
    return ChatOpenAI(model=openai_model())


def _text_chain(system: str, user_template: str):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", user_template),
        ]
    )
    return prompt | _llm() | StrOutputParser()


def _parse_intent(raw: str) -> str:
    token = raw.strip().lower().split()[0].strip(".,:;!?") if raw.strip() else "other"
    return token if token in INTENTS else "other"


def classify_node(state: RouteState) -> dict[str, str]:
    chain = _text_chain(ROUTE_SYSTEM, "{email}")
    raw = chain.invoke({"email": state["email"]})
    return {"intent": _parse_intent(raw)}


def _handler_node(system: str):
    def node(state: RouteState) -> dict[str, str]:
        chain = _text_chain(system, "{email}")
        return {"reply": chain.invoke({"email": state["email"]})}

    return node


def route_intent(state: RouteState) -> str:
    return state["intent"] if state["intent"] in INTENTS else "other"


def build_graph():
    graph = StateGraph(RouteState)
    graph.add_node("classify", classify_node)
    for intent, system in HANDLERS.items():
        graph.add_node(intent, _handler_node(system))
    graph.add_edge(START, "classify")
    graph.add_conditional_edges("classify", route_intent, {intent: intent for intent in INTENTS})
    for intent in INTENTS:
        graph.add_edge(intent, END)
    return graph.compile()


@observe(name="pattern.routing")
def run(email: str) -> RouteResult:
    with propagate_attributes(
        tags=["backend:langchain", "pattern:routing"],
        metadata={"pattern": "routing", "backend": "langchain"},
    ):
        handler = CallbackHandler()
        result = build_graph().invoke(
            {"email": email, "intent": "", "reply": ""},
            config={"callbacks": [handler]},
        )
        return RouteResult(intent=result["intent"], reply=result["reply"])


def main() -> None:
    for label, email in SAMPLE_EMAILS.items():
        print(f"\n=== {label} ===")
        print(run(email).model_dump_json(indent=2))
    get_client().flush()


if __name__ == "__main__":
    main()
