"""Prompt chaining with a sequential LangGraph and Langfuse CallbackHandler."""

from __future__ import annotations

from typing import TypedDict

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langfuse import get_client, observe, propagate_attributes
from langfuse.langchain import CallbackHandler
from langgraph.graph import END, START, StateGraph

from sd_agentic_shared.env import load_env, openai_model
from sd_agentic_shared.prompts import CHECK_SYSTEM, DRAFT_SYSTEM, SUMMARIZE_SYSTEM
from sd_agentic_shared.tasks.support_email import SUPPORT_EMAIL, TicketDraft

load_env()


class ChainState(TypedDict):
    email: str
    summary: str
    reply: str
    policy_ok: str


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


def summarize_node(state: ChainState) -> dict[str, str]:
    chain = _text_chain(SUMMARIZE_SYSTEM, "{email}")
    return {"summary": chain.invoke({"email": state["email"]})}


def draft_node(state: ChainState) -> dict[str, str]:
    chain = _text_chain(
        DRAFT_SYSTEM,
        "Original email:\n{email}\n\nFact summary:\n{summary}",
    )
    return {"reply": chain.invoke({"email": state["email"], "summary": state["summary"]})}


def check_node(state: ChainState) -> dict[str, str]:
    chain = _text_chain(
        CHECK_SYSTEM,
        "Original email:\n{email}\n\nSummary:\n{summary}\n\nDraft reply:\n{reply}",
    )
    return {
        "policy_ok": chain.invoke(
            {
                "email": state["email"],
                "summary": state["summary"],
                "reply": state["reply"],
            }
        )
    }


def build_graph():
    graph = StateGraph(ChainState)
    graph.add_node("summarize", summarize_node)
    graph.add_node("draft", draft_node)
    graph.add_node("check", check_node)
    graph.add_edge(START, "summarize")
    graph.add_edge("summarize", "draft")
    graph.add_edge("draft", "check")
    graph.add_edge("check", END)
    return graph.compile()


@observe(name="pattern.prompt_chaining")
def run(email: str) -> TicketDraft:
    with propagate_attributes(
        tags=["backend:langchain", "pattern:chaining"],
        metadata={"pattern": "prompt_chaining", "backend": "langchain"},
    ):
        handler = CallbackHandler()
        result = build_graph().invoke(
            {"email": email, "summary": "", "reply": "", "policy_ok": ""},
            config={"callbacks": [handler]},
        )
        return TicketDraft(
            summary=result["summary"],
            reply=result["reply"],
            policy_ok=result["policy_ok"],
        )


def main() -> None:
    result = run(SUPPORT_EMAIL)
    print(result.model_dump_json(indent=2))
    get_client().flush()


if __name__ == "__main__":
    main()
