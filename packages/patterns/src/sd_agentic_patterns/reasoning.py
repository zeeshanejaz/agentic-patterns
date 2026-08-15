"""Reasoning techniques: chain-of-thought samples, then a self-consistency pick."""

from __future__ import annotations

import json
from typing import Any

from langfuse import get_client, observe, propagate_attributes
from pydantic import BaseModel

from sd_agentic_patterns.llm import complete
from sd_agentic_shared.env import load_env
from sd_agentic_shared.prompts import REASONING_SYSTEM
from sd_agentic_shared.tasks.support_email import SUPPORT_EMAIL

load_env()

N_SAMPLES = 2


class ReasoningSample(BaseModel):
    steps: list[str]
    reply: str


class ReasoningResult(BaseModel):
    samples: list[ReasoningSample]
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


def _parse_sample(raw: str) -> ReasoningSample:
    try:
        payload = _extract_json(raw)
        steps = [str(item).strip() for item in (payload.get("steps") or []) if str(item).strip()]
        reply = str(payload.get("reply") or "").strip()
        if not steps:
            steps = ["parse produced no steps"]
        if not reply:
            reply = raw.strip()
        return ReasoningSample(steps=steps, reply=reply)
    except (ValueError, json.JSONDecodeError, TypeError):
        return ReasoningSample(steps=["fallback: unparseable CoT"], reply=raw.strip())


@observe(name="step.sample")
def one_sample(email: str) -> ReasoningSample:
    return _parse_sample(complete(REASONING_SYSTEM, email, temperature=0.7))


@observe(name="pattern.reasoning")
def run(email: str | None = None) -> ReasoningResult:
    ticket = email if email is not None else SUPPORT_EMAIL
    with propagate_attributes(
        tags=["backend:scratch", "pattern:reasoning"],
        metadata={"pattern": "reasoning", "backend": "scratch"},
    ):
        samples = [one_sample(ticket) for _ in range(N_SAMPLES)]
        chosen = samples[0].reply
        return ReasoningResult(samples=samples, reply=chosen)


def main() -> None:
    print(run().model_dump_json(indent=2))
    get_client().flush()


if __name__ == "__main__":
    main()
