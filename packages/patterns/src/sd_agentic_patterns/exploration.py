"""Exploration: expand reply angles, score, prune weak branches, pick a survivor."""

from __future__ import annotations

import json
import re
from typing import Any

from langfuse import get_client, observe, propagate_attributes
from pydantic import BaseModel

from sd_agentic_patterns.llm import complete
from sd_agentic_shared.env import load_env
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


@observe(name="step.explore_branch")
def expand(email: str, angle: str) -> str:
    return complete(
        EXPLORE_BRANCH_SYSTEM,
        f"Angle:\n{angle}\n\nEmail:\n{email}",
    )


@observe(name="step.score_branch")
def score_branch(email: str, angle: str, reply: str) -> tuple[int, bool, str]:
    return _parse_score(
        complete(
            EXPLORE_SCORE_SYSTEM,
            f"Angle:\n{angle}\n\nEmail:\n{email}\n\nDraft:\n{reply}",
        )
    )


def _prune(score: int, keep: bool, reply: str) -> tuple[bool, str]:
    if _promises_over_50(reply):
        return False, "heuristic: promised refund over $50"
    if score < KEEP_THRESHOLD:
        return False, f"below threshold ({score} < {KEEP_THRESHOLD})"
    return keep, ""


@observe(name="pattern.exploration")
def run(email: str | None = None) -> ExploreResult:
    ticket = email if email is not None else SUPPORT_EMAIL
    with propagate_attributes(
        tags=["backend:scratch", "pattern:exploration"],
        metadata={"pattern": "exploration", "backend": "scratch"},
    ):
        branches: list[Branch] = []
        for angle in EXPLORE_ANGLES:
            reply = expand(ticket, angle)
            score, keep, reason = score_branch(ticket, angle, reply)
            kept, prune_reason = _prune(score, keep, reply)
            if prune_reason:
                reason = prune_reason
                keep = kept
            else:
                keep = kept and keep
            branches.append(
                Branch(angle=angle, reply=reply, score=score, kept=keep, reason=reason)
            )
        kept = [item for item in branches if item.kept]
        pool = kept or branches
        winner = max(pool, key=lambda item: item.score)
        return ExploreResult(branches=branches, reply=winner.reply)


def main() -> None:
    print(run().model_dump_json(indent=2))
    get_client().flush()


if __name__ == "__main__":
    main()
