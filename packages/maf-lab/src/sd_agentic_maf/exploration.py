"""Exploration with MAF Agents: expand reply angles, score, prune, pick a survivor."""

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
from sd_agentic_shared.prompts import EXPLORE_BRANCH_SYSTEM, EXPLORE_SCORE_SYSTEM
from sd_agentic_shared.tasks.support_email import EXPLORE_ANGLES, SUPPORT_EMAIL

load_env()
_OTEL_READY = False

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


async def run(email: str | None = None) -> ExploreResult:
    ticket = email if email is not None else SUPPORT_EMAIL
    _ensure_otel()
    client = _client()
    agents = {
        "branch": Agent(client=client, name="branch", instructions=EXPLORE_BRANCH_SYSTEM),
        "score": Agent(client=client, name="score", instructions=EXPLORE_SCORE_SYSTEM),
    }
    with get_tracer().start_as_current_span("pattern.exploration") as span:
        span.set_attribute("pattern", "exploration")
        span.set_attribute("backend", "maf")
        branches: list[Branch] = []
        for angle in EXPLORE_ANGLES:
            reply = (
                await agents["branch"].run(f"Angle:\n{angle}\n\nEmail:\n{ticket}")
            ).text or ""
            score, keep, reason = _parse_score(
                (
                    await agents["score"].run(
                        f"Angle:\n{angle}\n\nEmail:\n{ticket}\n\nDraft:\n{reply}"
                    )
                ).text
                or ""
            )
            if _promises_over_50(reply):
                keep = False
                reason = "heuristic: promised refund over $50"
            elif score < KEEP_THRESHOLD:
                keep = False
                reason = f"below threshold ({score} < {KEEP_THRESHOLD})"
            branches.append(
                Branch(angle=angle, reply=reply, score=score, kept=keep, reason=reason)
            )
        kept = [item for item in branches if item.kept]
        pool = kept or branches
        winner = max(pool, key=lambda item: item.score)
        return ExploreResult(branches=branches, reply=winner.reply)


def main() -> None:
    print(asyncio.run(run()).model_dump_json(indent=2))
    provider = trace.get_tracer_provider()
    flush = getattr(provider, "force_flush", None)
    if callable(flush):
        flush()


if __name__ == "__main__":
    main()
