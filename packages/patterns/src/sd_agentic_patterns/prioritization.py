"""Prioritization: score a support inbox, draft the top tickets, re-score leftover."""

from __future__ import annotations

import json
import re
from typing import Any

from langfuse import get_client, observe, propagate_attributes
from pydantic import BaseModel

from sd_agentic_patterns.llm import complete
from sd_agentic_shared.env import load_env
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


@observe(name="step.score_ticket")
def score_ticket(ticket_id: str, email: str) -> TicketScore:
    return _parse_score(ticket_id, complete(PRIORITY_SCORE_SYSTEM, email), email)


@observe(name="step.execute_ticket")
def execute_ticket(ticket_id: str, email: str, score: int) -> ExecutedTicket:
    summary = complete(SUMMARIZE_SYSTEM, email)
    reply = complete(
        DRAFT_SYSTEM,
        f"Original email:\n{email}\n\nFact summary:\n{summary}",
    )
    return ExecutedTicket(id=ticket_id, score=score, reply=reply)


def _age_bump(item: TicketScore) -> TicketScore:
    return item.model_copy(update={"score": min(10, item.score + AGE_BUMP)})


@observe(name="pattern.prioritization")
def run(inbox: dict[str, str] | None = None) -> PriorityResult:
    queue = dict(inbox if inbox is not None else SAMPLE_EMAILS)
    with propagate_attributes(
        tags=["backend:scratch", "pattern:prioritization"],
        metadata={"pattern": "prioritization", "backend": "scratch"},
    ):
        ranked = sorted(
            [score_ticket(label, email) for label, email in queue.items()],
            key=lambda item: item.score,
            reverse=True,
        )
        initial = list(ranked)
        executed: list[ExecutedTicket] = []
        leftover = list(ranked)
        while leftover and len(executed) < MAX_EXECUTE:
            top = leftover.pop(0)
            executed.append(execute_ticket(top.id, queue[top.id], top.score))
            leftover = sorted(
                [_age_bump(item) for item in leftover],
                key=lambda item: item.score,
                reverse=True,
            )
        return PriorityResult(initial=initial, executed=executed, leftover=leftover)


def main() -> None:
    print(run().model_dump_json(indent=2))
    get_client().flush()


if __name__ == "__main__":
    main()
