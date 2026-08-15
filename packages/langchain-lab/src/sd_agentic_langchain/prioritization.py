"""Prioritization: LangGraph scores an inbox, drafts the top tickets, re-ranks leftover."""

from __future__ import annotations

import json
import re
from typing import Any, Literal, TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langfuse import get_client, observe, propagate_attributes
from langfuse.langchain import CallbackHandler
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel

from sd_agentic_shared.env import load_env, openai_model
from sd_agentic_shared.prompts import DRAFT_SYSTEM, PRIORITY_SCORE_SYSTEM, SUMMARIZE_SYSTEM
from sd_agentic_shared.tasks.support_email import SAMPLE_EMAILS

load_env()

MAX_EXECUTE = 2
AGE_BUMP = 1


class TicketScore(BaseModel):
    id: str
    score: int
    reason: str
    sla_hours: int


class ExecutedTicket(BaseModel):
    id: str
    score: int
    reply: str


class PriorityResult(BaseModel):
    initial: list[TicketScore]
    executed: list[ExecutedTicket]
    leftover: list[TicketScore]


class PriorityState(TypedDict):
    inbox: dict[str, str]
    initial: list[dict[str, Any]]
    leftover: list[dict[str, Any]]
    executed: list[dict[str, Any]]


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


def _urgent_floor(email: str) -> int:
    blob = email.lower()
    floor = 0
    if "chargeback" in blob:
        floor = max(floor, 9)
    if "refund" in blob:
        for match in re.findall(r"\$(\d+(?:\.\d+)?)", blob):
            if float(match) > 50:
                floor = max(floor, 8)
    if "today" in blob or "right now" in blob or "fix this now" in blob:
        floor = max(floor, 7)
    return floor


def _parse_score(ticket_id: str, raw: str, email: str) -> TicketScore:
    try:
        payload = _extract_json(raw)
        score = int(payload.get("score") or 1)
        sla = int(payload.get("sla_hours") or 24)
        reason = str(payload.get("reason") or "").strip() or "no reason"
    except (ValueError, json.JSONDecodeError, TypeError):
        score, sla, reason = 1, 24, "score parse failed"
    score = max(1, min(10, max(score, _urgent_floor(email))))
    if sla not in {1, 4, 8, 24}:
        sla = 8 if score >= 7 else 24
    return TicketScore(id=ticket_id, score=score, reason=reason, sla_hours=sla)


def score_all_node(state: PriorityState) -> dict[str, Any]:
    ranked = sorted(
        [
            _parse_score(label, _complete(PRIORITY_SCORE_SYSTEM, email), email)
            for label, email in state["inbox"].items()
        ],
        key=lambda item: item.score,
        reverse=True,
    )
    dumped = [item.model_dump() for item in ranked]
    return {"initial": dumped, "leftover": dumped, "executed": []}


def execute_node(state: PriorityState) -> dict[str, Any]:
    leftover = list(state["leftover"])
    top = leftover.pop(0)
    email = state["inbox"][top["id"]]
    summary = _complete(SUMMARIZE_SYSTEM, email)
    reply = _complete(
        DRAFT_SYSTEM,
        f"Original email:\n{email}\n\nFact summary:\n{summary}",
    )
    executed = list(state["executed"]) + [
        ExecutedTicket(id=top["id"], score=int(top["score"]), reply=reply).model_dump()
    ]
    return {"leftover": leftover, "executed": executed}


def age_node(state: PriorityState) -> dict[str, Any]:
    bumped = [
        TicketScore.model_validate(item).model_copy(
            update={"score": min(10, int(item["score"]) + AGE_BUMP)}
        )
        for item in state["leftover"]
    ]
    bumped.sort(key=lambda item: item.score, reverse=True)
    return {"leftover": [item.model_dump() for item in bumped]}


def after_turn(state: PriorityState) -> Literal["execute", "end"]:
    if state["leftover"] and len(state["executed"]) < MAX_EXECUTE:
        return "execute"
    return "end"


def build_graph():
    graph = StateGraph(PriorityState)
    graph.add_node("score_all", score_all_node)
    graph.add_node("execute", execute_node)
    graph.add_node("age", age_node)
    graph.add_edge(START, "score_all")
    graph.add_conditional_edges(
        "score_all",
        after_turn,
        {"execute": "execute", "end": END},
    )
    graph.add_edge("execute", "age")
    graph.add_conditional_edges(
        "age",
        after_turn,
        {"execute": "execute", "end": END},
    )
    return graph.compile()


@observe(name="pattern.prioritization")
def run(inbox: dict[str, str] | None = None) -> PriorityResult:
    queue = dict(inbox if inbox is not None else SAMPLE_EMAILS)
    with propagate_attributes(
        tags=["backend:langchain", "pattern:prioritization"],
        metadata={"pattern": "prioritization", "backend": "langchain"},
    ):
        handler = CallbackHandler()
        result = build_graph().invoke(
            {"inbox": queue, "initial": [], "leftover": [], "executed": []},
            config={"callbacks": [handler]},
        )
        return PriorityResult(
            initial=[TicketScore.model_validate(item) for item in result["initial"]],
            executed=[ExecutedTicket.model_validate(item) for item in result["executed"]],
            leftover=[TicketScore.model_validate(item) for item in result["leftover"]],
        )


def main() -> None:
    print(run().model_dump_json(indent=2))
    get_client().flush()


if __name__ == "__main__":
    main()
