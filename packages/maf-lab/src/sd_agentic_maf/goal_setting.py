"""Goal setting with MAF Agents. Traces via OTEL."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from agent_framework import Agent
from agent_framework.observability import get_tracer
from agent_framework.openai import OpenAIChatClient
from opentelemetry import trace
from pydantic import BaseModel

from sd_agentic_maf.otel import configure_maf_otel
from sd_agentic_shared.env import load_env, openai_model, workspace_root
from sd_agentic_shared.prompts import (
    GOAL_ADJUST_SYSTEM,
    GOAL_MONITOR_SYSTEM,
    GOAL_SET_SYSTEM,
    SUPPORT_SLA,
)
from sd_agentic_shared.tasks.support_email import SUPPORT_EMAIL

load_env()
_OTEL_READY = False

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


def _ensure_otel() -> None:
    global _OTEL_READY
    if not _OTEL_READY:
        configure_maf_otel()
        _OTEL_READY = True


def _client() -> OpenAIChatClient:
    return OpenAIChatClient(
        model=openai_model(),
        env_file_path=str(workspace_root() / ".env"),
    )


def build_agents() -> dict[str, Agent]:
    client = _client()
    return {
        "set_goals": Agent(client=client, name="set_goals", instructions=GOAL_SET_SYSTEM),
        "adjust": Agent(client=client, name="adjust", instructions=GOAL_ADJUST_SYSTEM),
        "monitor": Agent(client=client, name="monitor", instructions=GOAL_MONITOR_SYSTEM),
    }


async def _complete(agent: Agent, user: str) -> str:
    return (await agent.run(user)).text or ""


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


async def run(email: str | None = None) -> GoalSettingResult:
    ticket = email if email is not None else SUPPORT_EMAIL
    _ensure_otel()
    agents = build_agents()
    with get_tracer().start_as_current_span("pattern.goal_setting") as span:
        span.set_attribute("pattern", "goal_setting")
        span.set_attribute("backend", "maf")
        try:
            goals = _parse_goals(
                await _complete(
                    agents["set_goals"],
                    f"Support SLA:\n{SUPPORT_SLA}\n\nEmail:\n{ticket}",
                )
            )
        except (ValueError, json.JSONDecodeError, TypeError):
            goals = [Goal.model_validate(item) for item in FALLBACK_GOALS]
        reply = ""
        failed: list[GoalScore] = []
        attempts: list[Attempt] = []
        met = False
        for index in range(1, MAX_ATTEMPTS + 1):
            reply = await _complete(
                agents["adjust"],
                (
                    f"Goals:\n{_goals_blob(goals)}\n\n"
                    f"Failed goals:\n{_scores_blob(failed)}\n\n"
                    f"Prior draft:\n{reply or '(none — write the first reply)'}\n\n"
                    f"Email:\n{ticket}"
                ),
            )
            try:
                scores = _parse_scores(
                    await _complete(
                        agents["monitor"],
                        f"Goals:\n{_goals_blob(goals)}\n\nEmail:\n{ticket}\n\nReply:\n{reply}",
                    ),
                    goals,
                )
            except (ValueError, json.JSONDecodeError, TypeError):
                scores = [
                    GoalScore(id=goal.id, status="FAIL", reason="monitor parse failed")
                    for goal in goals
                ]
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
    print(asyncio.run(run()).model_dump_json(indent=2))
    provider = trace.get_tracer_provider()
    flush = getattr(provider, "force_flush", None)
    if callable(flush):
        flush()


if __name__ == "__main__":
    main()
