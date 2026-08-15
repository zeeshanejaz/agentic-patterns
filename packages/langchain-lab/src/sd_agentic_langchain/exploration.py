"""Exploration: LangGraph expands reply angles, scores, prunes, and picks a survivor."""

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
from sd_agentic_shared.prompts import EXPLORE_BRANCH_SYSTEM, EXPLORE_SCORE_SYSTEM
from sd_agentic_shared.tasks.support_email import EXPLORE_ANGLES, SUPPORT_EMAIL

load_env()

KEEP_THRESHOLD = 6


class Branch(BaseModel):
    angle: str
    reply: str
    score: int
    kept: bool
    reason: str


class ExploreResult(BaseModel):
    branches: list[Branch]
    reply: str


class ExploreState(TypedDict):
    email: str
    branches: list[dict[str, Any]]
    scored: int
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


def _promises_over_50(text: str) -> bool:
    blob = text.lower()
    if "refund" not in blob:
        return False
    for match in re.findall(r"\$(\d+(?:\.\d+)?)", blob):
        if float(match) > 50:
            return True
    return False


def _parse_score(raw: str) -> tuple[int, bool, str]:
    try:
        payload = _extract_json(raw)
        score = max(1, min(10, int(payload.get("score") or 1)))
        keep = bool(payload.get("keep"))
        reason = str(payload.get("reason") or "").strip() or "no reason"
        return score, keep, reason
    except (ValueError, json.JSONDecodeError, TypeError):
        return 1, False, "score parse failed"


def expand_node(state: ExploreState) -> dict[str, Any]:
    angle = EXPLORE_ANGLES[len(state["branches"])]
    reply = _complete(
        EXPLORE_BRANCH_SYSTEM,
        f"Angle:\n{angle}\n\nEmail:\n{state['email']}",
    )
    branch = Branch(angle=angle, reply=reply, score=0, kept=False, reason="unscored")
    return {"branches": state["branches"] + [branch.model_dump()]}


def after_expand(state: ExploreState) -> Literal["expand", "score"]:
    if len(state["branches"]) < len(EXPLORE_ANGLES):
        return "expand"
    return "score"


def score_node(state: ExploreState) -> dict[str, Any]:
    idx = state["scored"]
    item = Branch.model_validate(state["branches"][idx])
    score, keep, reason = _parse_score(
        _complete(
            EXPLORE_SCORE_SYSTEM,
            f"Angle:\n{item.angle}\n\nEmail:\n{state['email']}\n\nDraft:\n{item.reply}",
        )
    )
    updated = list(state["branches"])
    updated[idx] = item.model_copy(
        update={"score": score, "kept": keep, "reason": reason}
    ).model_dump()
    return {"branches": updated, "scored": idx + 1}


def after_score(state: ExploreState) -> Literal["score", "prune"]:
    if state["scored"] < len(state["branches"]):
        return "score"
    return "prune"


def prune_node(state: ExploreState) -> dict[str, Any]:
    branches: list[Branch] = []
    for raw in state["branches"]:
        item = Branch.model_validate(raw)
        if _promises_over_50(item.reply):
            item = item.model_copy(
                update={"kept": False, "reason": "heuristic: promised refund over $50"}
            )
        elif item.score < KEEP_THRESHOLD:
            item = item.model_copy(
                update={
                    "kept": False,
                    "reason": f"below threshold ({item.score} < {KEEP_THRESHOLD})",
                }
            )
        branches.append(item)
    kept = [item for item in branches if item.kept]
    pool = kept or branches
    winner = max(pool, key=lambda item: item.score)
    return {
        "branches": [item.model_dump() for item in branches],
        "reply": winner.reply,
    }


def build_graph():
    graph = StateGraph(ExploreState)
    graph.add_node("expand", expand_node)
    graph.add_node("score", score_node)
    graph.add_node("prune", prune_node)
    graph.add_edge(START, "expand")
    graph.add_conditional_edges(
        "expand",
        after_expand,
        {"expand": "expand", "score": "score"},
    )
    graph.add_conditional_edges(
        "score",
        after_score,
        {"score": "score", "prune": "prune"},
    )
    graph.add_edge("prune", END)
    return graph.compile()


@observe(name="pattern.exploration")
def run(email: str | None = None) -> ExploreResult:
    ticket = email if email is not None else SUPPORT_EMAIL
    with propagate_attributes(
        tags=["backend:langchain", "pattern:exploration"],
        metadata={"pattern": "exploration", "backend": "langchain"},
    ):
        handler = CallbackHandler()
        result = build_graph().invoke(
            {"email": ticket, "branches": [], "scored": 0, "reply": ""},
            config={"callbacks": [handler]},
        )
        return ExploreResult(
            branches=[Branch.model_validate(item) for item in result["branches"]],
            reply=result["reply"],
        )


def main() -> None:
    print(run().model_dump_json(indent=2))
    get_client().flush()


if __name__ == "__main__":
    main()
