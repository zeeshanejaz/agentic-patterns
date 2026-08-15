"""Goal setting and monitoring: set KPIs, score progress, adjust within a budget."""

from __future__ import annotations

import json
from typing import Any

from langfuse import get_client, observe, propagate_attributes
from pydantic import BaseModel

from sd_agentic_patterns.llm import complete
from sd_agentic_shared.env import load_env
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


@observe(name="step.set_goals")
def set_goals(email: str) -> list[Goal]:
    user = f"Support SLA:\n{SUPPORT_SLA}\n\nEmail:\n{email}"
    try:
        return _parse_goals(complete(GOAL_SET_SYSTEM, user))
    except (ValueError, json.JSONDecodeError, TypeError):
        return [Goal.model_validate(item) for item in FALLBACK_GOALS]


@observe(name="step.adjust")
def adjust(email: str, goals: list[Goal], prior_reply: str, failed: list[GoalScore]) -> str:
    user = (
        f"Goals:\n{_goals_blob(goals)}\n\n"
        f"Failed goals:\n{_scores_blob(failed)}\n\n"
        f"Prior draft:\n{prior_reply or '(none — write the first reply)'}\n\n"
        f"Email:\n{email}"
    )
    return complete(GOAL_ADJUST_SYSTEM, user)


@observe(name="step.monitor")
def monitor(email: str, reply: str, goals: list[Goal]) -> list[GoalScore]:
    user = f"Goals:\n{_goals_blob(goals)}\n\nEmail:\n{email}\n\nReply:\n{reply}"
    try:
        return _parse_scores(complete(GOAL_MONITOR_SYSTEM, user), goals)
    except (ValueError, json.JSONDecodeError, TypeError):
        return [
            GoalScore(id=goal.id, status="FAIL", reason="monitor parse failed")
            for goal in goals
        ]


@observe(name="pattern.goal_setting")
def run(email: str | None = None) -> GoalSettingResult:
    ticket = email if email is not None else SUPPORT_EMAIL
    with propagate_attributes(
        tags=["backend:scratch", "pattern:goal_setting"],
        metadata={"pattern": "goal_setting", "backend": "scratch"},
    ):
        goals = set_goals(ticket)
        reply = ""
        failed: list[GoalScore] = []
        attempts: list[Attempt] = []
        met = False
        for index in range(1, MAX_ATTEMPTS + 1):
            reply = adjust(ticket, goals, reply, failed)
            scores = monitor(ticket, reply, goals)
            attempts.append(Attempt(attempt=index, reply=reply, scores=scores))
            failed = [item for item in scores if item.status != "PASS"]
            if not failed:
                met = True
                break
        return GoalSettingResult(
            goals=goals,
            attempts=attempts,
            attempts_used=len(attempts),
            reply=reply,
            met=met,
        )


def main() -> None:
    print(run().model_dump_json(indent=2))
    get_client().flush()


if __name__ == "__main__":
    main()
