"""Goal setting: LangGraph set → adjust → monitor until PASS or budget."""

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
    GOAL_ADJUST_SYSTEM,
    GOAL_MONITOR_SYSTEM,
    GOAL_SET_SYSTEM,
    SUPPORT_SLA,
)
from sd_agentic_shared.tasks.support_email import SUPPORT_EMAIL

load_env()

MAX_ATTEMPTS = 3
FALLBACK_GOALS = [
    {"id": "coverage", "target": "Address the shipping delay and the duplicate-charge / refund ask"},
    {"id": "policy", "target": "Do not invent tracking or promise a refund over $50"},
    {"id": "ids", "target": "Acknowledge order ids mentioned in the email; do not invent others"},
]


class Goal(BaseModel):
    id: str
    target: str


class GoalScore(BaseModel):
    id: str
    status: str
    reason: str


class Attempt(BaseModel):
    attempt: int
    reply: str
    scores: list[GoalScore]


class GoalSettingResult(BaseModel):
    goals: list[Goal]
    attempts: list[Attempt]
    attempts_used: int
    reply: str
    met: bool


class GoalState(TypedDict):
    email: str
    goals: list[dict[str, str]]
    reply: str
    failed: list[dict[str, str]]
    attempts: list[dict[str, Any]]
    attempt: int
    met: bool


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


def _goals_blob(goals: list[Goal]) -> str:
    return "\n".join(f"- [{goal.id}] {goal.target}" for goal in goals)


def _scores_blob(scores: list[GoalScore]) -> str:
    if not scores:
        return "(none)"
    return "\n".join(f"- [{item.id}] {item.status}: {item.reason}" for item in scores)


def _parse_goals(raw: str) -> list[Goal]:
    payload = _extract_json(raw)
    items = payload.get("goals") or []
    goals: list[Goal] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        goal_id = str(item.get("id") or "").strip()
        target = str(item.get("target") or "").strip()
        if goal_id and target:
            goals.append(Goal(id=goal_id, target=target))
    if len(goals) < 3:
        raise ValueError("need at least 3 goals")
    return goals[:5]


def _parse_scores(raw: str, goals: list[Goal]) -> list[GoalScore]:
    payload = _extract_json(raw)
    by_id = {
        str(item.get("id") or "").strip(): item
        for item in (payload.get("scores") or [])
        if isinstance(item, dict)
    }
    scores: list[GoalScore] = []
    for goal in goals:
        item = by_id.get(goal.id) or {}
        status = str(item.get("status") or "FAIL").strip().upper()
        if status not in {"PASS", "FAIL"}:
            status = "FAIL"
        reason = str(item.get("reason") or "missing score").strip()
        scores.append(GoalScore(id=goal.id, status=status, reason=reason))
    return scores


def set_goals_node(state: GoalState) -> dict[str, Any]:
    user = f"Support SLA:\n{SUPPORT_SLA}\n\nEmail:\n{state['email']}"
    try:
        goals = _parse_goals(_complete(GOAL_SET_SYSTEM, user))
    except (ValueError, json.JSONDecodeError, TypeError):
        goals = [Goal.model_validate(item) for item in FALLBACK_GOALS]
    return {
        "goals": [goal.model_dump() for goal in goals],
        "reply": "",
        "failed": [],
        "attempts": [],
        "attempt": 0,
        "met": False,
    }


def adjust_node(state: GoalState) -> dict[str, str]:
    goals = [Goal.model_validate(item) for item in state["goals"]]
    failed = [GoalScore.model_validate(item) for item in state["failed"]]
    user = (
        f"Goals:\n{_goals_blob(goals)}\n\n"
        f"Failed goals:\n{_scores_blob(failed)}\n\n"
        f"Prior draft:\n{state['reply'] or '(none — write the first reply)'}\n\n"
        f"Email:\n{state['email']}"
    )
    return {"reply": _complete(GOAL_ADJUST_SYSTEM, user)}


def monitor_node(state: GoalState) -> dict[str, Any]:
    goals = [Goal.model_validate(item) for item in state["goals"]]
    try:
        scores = _parse_scores(
            _complete(
                GOAL_MONITOR_SYSTEM,
                f"Goals:\n{_goals_blob(goals)}\n\nEmail:\n{state['email']}\n\nReply:\n{state['reply']}",
            ),
            goals,
        )
    except (ValueError, json.JSONDecodeError, TypeError):
        scores = [
            GoalScore(id=goal.id, status="FAIL", reason="monitor parse failed")
            for goal in goals
        ]
    failed = [item for item in scores if item.status != "PASS"]
    attempt = Attempt(
        attempt=state["attempt"] + 1,
        reply=state["reply"],
        scores=scores,
    )
    return {
        "failed": [item.model_dump() for item in failed],
        "attempts": state["attempts"] + [attempt.model_dump()],
        "attempt": attempt.attempt,
        "met": not failed,
    }


def after_monitor(state: GoalState) -> Literal["adjust", "end"]:
    if state["met"] or state["attempt"] >= MAX_ATTEMPTS:
        return "end"
    return "adjust"


def build_graph():
    graph = StateGraph(GoalState)
    graph.add_node("set_goals", set_goals_node)
    graph.add_node("adjust", adjust_node)
    graph.add_node("monitor", monitor_node)
    graph.add_edge(START, "set_goals")
    graph.add_edge("set_goals", "adjust")
    graph.add_edge("adjust", "monitor")
    graph.add_conditional_edges(
        "monitor",
        after_monitor,
        {"adjust": "adjust", "end": END},
    )
    return graph.compile()


@observe(name="pattern.goal_setting")
def run(email: str | None = None) -> GoalSettingResult:
    ticket = email if email is not None else SUPPORT_EMAIL
    with propagate_attributes(
        tags=["backend:langchain", "pattern:goal_setting"],
        metadata={"pattern": "goal_setting", "backend": "langchain"},
    ):
        handler = CallbackHandler()
        result = build_graph().invoke(
            {
                "email": ticket,
                "goals": [],
                "reply": "",
                "failed": [],
                "attempts": [],
                "attempt": 0,
                "met": False,
            },
            config={"callbacks": [handler]},
        )
        return GoalSettingResult(
            goals=[Goal.model_validate(item) for item in result["goals"]],
            attempts=[Attempt.model_validate(item) for item in result["attempts"]],
            attempts_used=result["attempt"],
            reply=result["reply"],
            met=result["met"],
        )


def main() -> None:
    print(run().model_dump_json(indent=2))
    get_client().flush()


if __name__ == "__main__":
    main()
