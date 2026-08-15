"""Multi-agent: LangGraph coordinate → specialists → optional review → writer."""

from __future__ import annotations

import json
from typing import Any, Literal, TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langfuse import get_client, observe, propagate_attributes
from langfuse.langchain import CallbackHandler
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel

from sd_agentic_shared.env import load_env, openai_model
from sd_agentic_shared.prompts import (
    BILLING_AGENT_SYSTEM,
    COORDINATOR_REVIEW_SYSTEM,
    COORDINATOR_SYSTEM,
    POLICY_AGENT_SYSTEM,
    SHIPPING_AGENT_SYSTEM,
    WRITER_AGENT_SYSTEM,
)
from sd_agentic_shared.tasks.support_email import SUPPORT_EMAIL

load_env()

MAX_ROUNDS = 2
ROSTER = ("billing", "shipping", "policy")
AGENT_SYSTEMS: dict[str, str] = {
    "billing": BILLING_AGENT_SYSTEM,
    "shipping": SHIPPING_AGENT_SYSTEM,
    "policy": POLICY_AGENT_SYSTEM,
}


class Assignment(BaseModel):
    agent: str
    instruction: str


class Note(BaseModel):
    agent: str
    text: str


class MultiAgentResult(BaseModel):
    assignments: list[Assignment]
    notes: list[Note]
    rounds: int
    reply: str


class MultiAgentState(TypedDict):
    email: str
    pending: list[dict[str, str]]
    assignments: list[dict[str, str]]
    notes: list[dict[str, str]]
    rounds: int
    reply: str


def _llm() -> ChatOpenAI:
    return ChatOpenAI(model=openai_model())


def _complete(system: str, user: str) -> str:
    message = _llm().invoke(
        [SystemMessage(content=system), HumanMessage(content=user)]
    )
    content = message.content
    return content if isinstance(content, str) else str(content or "")


def _extract_json(text: str) -> dict[str, Any]:
    raw = text.strip()
    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.lower().startswith("json"):
            raw = raw[4:]
        raw = raw.strip()
    start = raw.find("{")
    end = raw.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("no JSON object in model output")
    parsed = json.loads(raw[start : end + 1])
    if not isinstance(parsed, dict):
        raise ValueError("JSON root must be an object")
    return parsed


def _fallback_assignments() -> list[Assignment]:
    return [
        Assignment(agent=name, instruction="Write a short team note about your domain for this email.")
        for name in ROSTER
    ]


def _assignments_from_payload(payload: dict[str, Any]) -> list[Assignment]:
    items = payload.get("assignments") or []
    assignments: list[Assignment] = []
    seen: set[str] = set()
    for item in items:
        if not isinstance(item, dict):
            continue
        agent = str(item.get("agent") or "").strip().lower()
        if agent not in ROSTER or agent in seen:
            continue
        seen.add(agent)
        assignments.append(
            Assignment(
                agent=agent,
                instruction=str(item.get("instruction") or "Write a short team note."),
            )
        )
    if not assignments:
        raise ValueError("no valid assignments")
    return assignments


def _notes_blob(notes: list[Note]) -> str:
    if not notes:
        return "(none)"
    return "\n\n".join(f"[{item.agent}]\n{item.text}" for item in notes)


def coordinate(email: str) -> list[Assignment]:
    raw = _complete(COORDINATOR_SYSTEM, email)
    try:
        return _assignments_from_payload(_extract_json(raw))
    except (ValueError, json.JSONDecodeError, TypeError):
        return _fallback_assignments()


def review(email: str, notes: list[Note]) -> list[Assignment]:
    user = f"Original email:\n{email}\n\nTeam notes:\n{_notes_blob(notes)}"
    raw = _complete(COORDINATOR_REVIEW_SYSTEM, user)
    if raw.strip().upper().startswith("DONE"):
        return []
    try:
        return _assignments_from_payload(_extract_json(raw))
    except (ValueError, json.JSONDecodeError, TypeError):
        return []


def run_specialist(agent: str, email: str, instruction: str, notes: list[Note]) -> Note:
    user = (
        f"Original email:\n{email}\n\n"
        f"Your instruction:\n{instruction}\n\n"
        f"Notes so far:\n{_notes_blob(notes)}"
    )
    text = _complete(AGENT_SYSTEMS[agent], user)
    return Note(agent=agent, text=text)


def write_reply(email: str, notes: list[Note]) -> str:
    user = f"Original email:\n{email}\n\nTeam notes:\n{_notes_blob(notes)}"
    return _complete(WRITER_AGENT_SYSTEM, user)


def coordinate_node(state: MultiAgentState) -> dict[str, Any]:
    pending = [item.model_dump() for item in coordinate(state["email"])]
    return {
        "pending": pending,
        "assignments": pending,
        "notes": [],
        "rounds": 0,
        "reply": "",
    }


def specialists_node(state: MultiAgentState) -> dict[str, Any]:
    notes = [Note.model_validate(item) for item in state["notes"]]
    for item in state["pending"]:
        assignment = Assignment.model_validate(item)
        notes.append(
            run_specialist(
                assignment.agent,
                state["email"],
                assignment.instruction,
                notes,
            )
        )
    return {
        "notes": [item.model_dump() for item in notes],
        "pending": [],
        "rounds": state["rounds"] + 1,
    }


def review_node(state: MultiAgentState) -> dict[str, Any]:
    notes = [Note.model_validate(item) for item in state["notes"]]
    pending = [item.model_dump() for item in review(state["email"], notes)]
    return {
        "pending": pending,
        "assignments": state["assignments"] + pending,
    }


def write_node(state: MultiAgentState) -> dict[str, str]:
    notes = [Note.model_validate(item) for item in state["notes"]]
    return {"reply": write_reply(state["email"], notes)}


def after_specialists(state: MultiAgentState) -> Literal["review", "write"]:
    return "review" if state["rounds"] < MAX_ROUNDS else "write"


def after_review(state: MultiAgentState) -> Literal["specialists", "write"]:
    return "specialists" if state["pending"] else "write"


def build_graph():
    graph = StateGraph(MultiAgentState)
    graph.add_node("coordinate", coordinate_node)
    graph.add_node("specialists", specialists_node)
    graph.add_node("review", review_node)
    graph.add_node("write", write_node)
    graph.add_edge(START, "coordinate")
    graph.add_edge("coordinate", "specialists")
    graph.add_conditional_edges(
        "specialists",
        after_specialists,
        {"review": "review", "write": "write"},
    )
    graph.add_conditional_edges(
        "review",
        after_review,
        {"specialists": "specialists", "write": "write"},
    )
    graph.add_edge("write", END)
    return graph.compile()


@observe(name="pattern.multi_agent")
def run(email: str) -> MultiAgentResult:
    with propagate_attributes(
        tags=["backend:langchain", "pattern:multi_agent"],
        metadata={"pattern": "multi_agent", "backend": "langchain"},
    ):
        handler = CallbackHandler()
        result = build_graph().invoke(
            {
                "email": email,
                "pending": [],
                "assignments": [],
                "notes": [],
                "rounds": 0,
                "reply": "",
            },
            config={"callbacks": [handler]},
        )
        return MultiAgentResult(
            assignments=[Assignment.model_validate(item) for item in result["assignments"]],
            notes=[Note.model_validate(item) for item in result["notes"]],
            rounds=int(result["rounds"]),
            reply=result["reply"],
        )


def main() -> None:
    print(run(SUPPORT_EMAIL).model_dump_json(indent=2))
    get_client().flush()


if __name__ == "__main__":
    main()
