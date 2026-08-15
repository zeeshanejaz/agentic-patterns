"""Reflection: LangGraph draft → critic → revise until PASS or max rounds."""

from __future__ import annotations

from typing import Literal, TypedDict

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langfuse import get_client, observe, propagate_attributes
from langfuse.langchain import CallbackHandler
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel

from sd_agentic_shared.env import load_env, openai_model
from sd_agentic_shared.prompts import CRITIC_SYSTEM, DRAFT_SYSTEM, REVISE_SYSTEM, SUMMARIZE_SYSTEM
from sd_agentic_shared.tasks.support_email import SUPPORT_EMAIL

load_env()

MAX_ROUNDS = 3


class ReflectionRound(BaseModel):
    draft: str
    critique: str


class ReflectionResult(BaseModel):
    summary: str
    rounds: list[ReflectionRound]
    final: str
    passed: bool


class ReflectionState(TypedDict):
    email: str
    summary: str
    draft: str
    critique: str
    rounds: list[dict[str, str]]
    round_index: int
    passed: bool
    final: str


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


def _passed(critique_text: str) -> bool:
    return critique_text.strip().upper().startswith("PASS")


def summarize_node(state: ReflectionState) -> dict[str, str]:
    chain = _text_chain(SUMMARIZE_SYSTEM, "{email}")
    return {"summary": chain.invoke({"email": state["email"]})}


def draft_node(state: ReflectionState) -> dict[str, str]:
    chain = _text_chain(
        DRAFT_SYSTEM,
        "Original email:\n{email}\n\nFact summary:\n{summary}",
    )
    draft = chain.invoke({"email": state["email"], "summary": state["summary"]})
    return {"draft": draft, "final": draft}


def critic_node(state: ReflectionState) -> dict[str, object]:
    chain = _text_chain(
        CRITIC_SYSTEM,
        "Original email:\n{email}\n\nDraft:\n{draft}",
    )
    critique_text = chain.invoke({"email": state["email"], "draft": state["draft"]})
    rounds = list(state["rounds"]) + [{"draft": state["draft"], "critique": critique_text}]
    passed = _passed(critique_text)
    return {
        "critique": critique_text,
        "rounds": rounds,
        "passed": passed,
        "round_index": state["round_index"] + 1,
        "final": state["draft"],
    }


def revise_node(state: ReflectionState) -> dict[str, str]:
    chain = _text_chain(
        REVISE_SYSTEM,
        "Original email:\n{email}\n\nCurrent draft:\n{draft}\n\nCritic:\n{critique}",
    )
    draft = chain.invoke(
        {
            "email": state["email"],
            "draft": state["draft"],
            "critique": state["critique"],
        }
    )
    return {"draft": draft, "final": draft}


def should_continue(state: ReflectionState) -> Literal["revise", "end"]:
    if state["passed"] or state["round_index"] >= MAX_ROUNDS:
        return "end"
    return "revise"


def build_graph():
    graph = StateGraph(ReflectionState)
    graph.add_node("summarize", summarize_node)
    graph.add_node("draft", draft_node)
    graph.add_node("critic", critic_node)
    graph.add_node("revise", revise_node)
    graph.add_edge(START, "summarize")
    graph.add_edge("summarize", "draft")
    graph.add_edge("draft", "critic")
    graph.add_conditional_edges(
        "critic",
        should_continue,
        {"revise": "revise", "end": END},
    )
    graph.add_edge("revise", "critic")
    return graph.compile()


@observe(name="pattern.reflection")
def run(email: str) -> ReflectionResult:
    with propagate_attributes(
        tags=["backend:langchain", "pattern:reflection"],
        metadata={"pattern": "reflection", "backend": "langchain"},
    ):
        handler = CallbackHandler()
        result = build_graph().invoke(
            {
                "email": email,
                "summary": "",
                "draft": "",
                "critique": "",
                "rounds": [],
                "round_index": 0,
                "passed": False,
                "final": "",
            },
            config={"callbacks": [handler]},
        )
        return ReflectionResult(
            summary=result["summary"],
            rounds=[ReflectionRound.model_validate(item) for item in result["rounds"]],
            final=result["final"],
            passed=bool(result["passed"]),
        )


def main() -> None:
    print(run(SUPPORT_EMAIL).model_dump_json(indent=2))
    get_client().flush()


if __name__ == "__main__":
    main()
