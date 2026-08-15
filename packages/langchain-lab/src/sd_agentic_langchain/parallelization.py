"""Parallelization: LangGraph fan-out sectioning and voting, then merge."""

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
    MERGE_SECTIONS_SYSTEM,
    SECTION_ASK_SYSTEM,
    SECTION_ORDER_SYSTEM,
    SECTION_PAYMENT_SYSTEM,
    VOTE_MERGE_SYSTEM,
)
from sd_agentic_shared.tasks.support_email import SUPPORT_EMAIL

load_env()

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


class SectionState(TypedDict):
    email: str
    order: str
    payment: str
    ask: str
    summary: str


class VoteState(TypedDict):
    email: str
    draft_1: str
    draft_2: str
    draft_3: str
    merged: str


def _llm(*, temperature: float | None = None) -> ChatOpenAI:
    kwargs: dict[str, float] = {}
    if temperature is not None:
        kwargs["temperature"] = temperature
    return ChatOpenAI(model=openai_model(), **kwargs)


def _text_chain(system: str, user_template: str, *, temperature: float | None = None):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", user_template),
        ]
    )
    return prompt | _llm(temperature=temperature) | StrOutputParser()


def _section_node(field: str, system: str):
    def node(state: SectionState) -> dict[str, str]:
        chain = _text_chain(system, "{email}")
        return {field: chain.invoke({"email": state["email"]})}

    return node


def merge_sections_node(state: SectionState) -> dict[str, str]:
    chain = _text_chain(MERGE_SECTIONS_SYSTEM, "{user}")
    user = (
        f"Order facts:\n{state['order']}\n\n"
        f"Payment facts:\n{state['payment']}\n\n"
        f"Customer ask:\n{state['ask']}"
    )
    return {"summary": chain.invoke({"user": user})}


def build_sectioning_graph():
    graph = StateGraph(SectionState)
    graph.add_node("section_order", _section_node("order", SECTION_ORDER_SYSTEM))
    graph.add_node("section_payment", _section_node("payment", SECTION_PAYMENT_SYSTEM))
    graph.add_node("section_ask", _section_node("ask", SECTION_ASK_SYSTEM))
    graph.add_node("merge_sections", merge_sections_node)
    graph.add_edge(START, "section_order")
    graph.add_edge(START, "section_payment")
    graph.add_edge(START, "section_ask")
    graph.add_edge("section_order", "merge_sections")
    graph.add_edge("section_payment", "merge_sections")
    graph.add_edge("section_ask", "merge_sections")
    graph.add_edge("merge_sections", END)
    return graph.compile()


def _vote_draft_node(index: int, field: str):
    def node(state: VoteState) -> dict[str, str]:
        chain = _text_chain(
            VOTE_WORKER_SYSTEM.format(index=index),
            "{email}",
            temperature=0.8,
        )
        return {field: chain.invoke({"email": state["email"]})}

    return node


def vote_merge_node(state: VoteState) -> dict[str, str]:
    drafts = [state["draft_1"], state["draft_2"], state["draft_3"]]
    numbered = "\n\n".join(f"Draft {i}:\n{d}" for i, d in enumerate(drafts, start=1))
    chain = _text_chain(VOTE_MERGE_SYSTEM, "{user}")
    user = f"Original email:\n{state['email']}\n\n{numbered}"
    return {"merged": chain.invoke({"user": user})}


def build_voting_graph():
    graph = StateGraph(VoteState)
    graph.add_node("draft_1", _vote_draft_node(1, "draft_1"))
    graph.add_node("draft_2", _vote_draft_node(2, "draft_2"))
    graph.add_node("draft_3", _vote_draft_node(3, "draft_3"))
    graph.add_node("vote_merge", vote_merge_node)
    graph.add_edge(START, "draft_1")
    graph.add_edge(START, "draft_2")
    graph.add_edge(START, "draft_3")
    graph.add_edge("draft_1", "vote_merge")
    graph.add_edge("draft_2", "vote_merge")
    graph.add_edge("draft_3", "vote_merge")
    graph.add_edge("vote_merge", END)
    return graph.compile()


@observe(name="pattern.parallelization.sectioning")
def run_sectioning(email: str) -> SectionResult:
    with propagate_attributes(
        tags=["backend:langchain", "pattern:parallelization"],
        metadata={"pattern": "parallelization", "mode": "sectioning", "backend": "langchain"},
    ):
        handler = CallbackHandler()
        result = build_sectioning_graph().invoke(
            {"email": email, "order": "", "payment": "", "ask": "", "summary": ""},
            config={"callbacks": [handler]},
        )
        return SectionResult(
            order=result["order"],
            payment=result["payment"],
            ask=result["ask"],
            summary=result["summary"],
        )


@observe(name="pattern.parallelization.voting")
def run_voting(email: str) -> VoteResult:
    with propagate_attributes(
        tags=["backend:langchain", "pattern:parallelization"],
        metadata={"pattern": "parallelization", "mode": "voting", "backend": "langchain"},
    ):
        handler = CallbackHandler()
        result = build_voting_graph().invoke(
            {"email": email, "draft_1": "", "draft_2": "", "draft_3": "", "merged": ""},
            config={"callbacks": [handler]},
        )
        return VoteResult(
            drafts=[result["draft_1"], result["draft_2"], result["draft_3"]],
            merged=result["merged"],
        )


def main() -> None:
    print("=== sectioning ===")
    print(run_sectioning(SUPPORT_EMAIL).model_dump_json(indent=2))
    print("\n=== voting ===")
    print(run_voting(SUPPORT_EMAIL).model_dump_json(indent=2))
    get_client().flush()


if __name__ == "__main__":
    main()
