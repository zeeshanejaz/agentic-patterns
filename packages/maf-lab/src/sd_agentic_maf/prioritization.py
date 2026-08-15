"""Prioritization with MAF Agents: score an inbox, draft the top tickets, re-rank leftover."""

from __future__ import annotations

import asyncio
import json
import re
from typing import Any

from agent_framework import Agent
from agent_framework.observability import get_tracer
from agent_framework.openai import OpenAIChatClient
from opentelemetry import trace
from pydantic import BaseModel

from sd_agentic_maf.otel import configure_maf_otel
from sd_agentic_shared.env import load_env, openai_model, workspace_root
from sd_agentic_shared.prompts import DRAFT_SYSTEM, PRIORITY_SCORE_SYSTEM, SUMMARIZE_SYSTEM
from sd_agentic_shared.tasks.support_email import SAMPLE_EMAILS

load_env()
_OTEL_READY = False

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


def _age_bump(item: TicketScore) -> TicketScore:
    return item.model_copy(update={"score": min(10, item.score + AGE_BUMP)})


async def run(inbox: dict[str, str] | None = None) -> PriorityResult:
    queue = dict(inbox if inbox is not None else SAMPLE_EMAILS)
    _ensure_otel()
    client = _client()
    agents = {
        "score": Agent(client=client, name="score", instructions=PRIORITY_SCORE_SYSTEM),
        "summarize": Agent(client=client, name="summarize", instructions=SUMMARIZE_SYSTEM),
        "draft": Agent(client=client, name="draft", instructions=DRAFT_SYSTEM),
    }
    with get_tracer().start_as_current_span("pattern.prioritization") as span:
        span.set_attribute("pattern", "prioritization")
        span.set_attribute("backend", "maf")
        ranked = []
        for label, email in queue.items():
            raw = (await agents["score"].run(email)).text or ""
            ranked.append(_parse_score(label, raw, email))
        ranked.sort(key=lambda item: item.score, reverse=True)
        initial = list(ranked)
        leftover = list(ranked)
        executed: list[ExecutedTicket] = []
        while leftover and len(executed) < MAX_EXECUTE:
            top = leftover.pop(0)
            email = queue[top.id]
            summary = (await agents["summarize"].run(email)).text or ""
            reply = (
                await agents["draft"].run(
                    f"Original email:\n{email}\n\nFact summary:\n{summary}"
                )
            ).text or ""
            executed.append(ExecutedTicket(id=top.id, score=top.score, reply=reply))
            leftover = sorted(
                [_age_bump(item) for item in leftover],
                key=lambda item: item.score,
                reverse=True,
            )
        return PriorityResult(initial=initial, executed=executed, leftover=leftover)


def main() -> None:
    print(asyncio.run(run()).model_dump_json(indent=2))
    provider = trace.get_tracer_provider()
    flush = getattr(provider, "force_flush", None)
    if callable(flush):
        flush()


if __name__ == "__main__":
    main()
