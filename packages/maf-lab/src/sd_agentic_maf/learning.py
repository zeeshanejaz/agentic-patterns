"""Learning and adaptation with MAF Agents. Traces via OTEL."""

from __future__ import annotations

import asyncio
import re

from agent_framework import Agent
from agent_framework.observability import get_tracer
from agent_framework.openai import OpenAIChatClient
from opentelemetry import trace
from pydantic import BaseModel

from sd_agentic_maf.otel import configure_maf_otel
from sd_agentic_shared.env import load_env, openai_model, workspace_root
from sd_agentic_shared.prompts import LEARNING_DISTILL_SYSTEM, LEARNING_REPLY_SYSTEM
from sd_agentic_shared.tasks.support_email import LEARNING_CASES, LEARNING_HELD_OUT, LearningCase

load_env()
_OTEL_READY = False

MIN_RATING = 2
POISON_MARKERS = (
    "invent tracking",
    "invent order",
    "blame",
    "their fault",
    "your fault",
    "stupid",
)


class LearningResult(BaseModel):
    kept: list[dict[str, object]]
    dropped: list[dict[str, object]]
    lessons: str
    held_out: str
    baseline: str
    adapted: str


def _is_poison(correction: str) -> bool:
    blob = correction.lower()
    if any(marker in blob for marker in POISON_MARKERS):
        return True
    for match in re.findall(r"\$(\d+(?:\.\d+)?)", blob):
        if float(match) > 50:
            return True
    return False


def _case_blob(case: LearningCase) -> dict[str, object]:
    return {"email": case.email, "rating": case.rating, "correction": case.correction}


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
        "distill": Agent(client=client, name="distill", instructions=LEARNING_DISTILL_SYSTEM),
        "reply": Agent(client=client, name="reply", instructions=LEARNING_REPLY_SYSTEM),
    }


async def _complete(agent: Agent, user: str) -> str:
    return (await agent.run(user)).text or ""


def clean_feedback(cases: list[LearningCase]) -> tuple[list[LearningCase], list[LearningCase]]:
    kept: list[LearningCase] = []
    dropped: list[LearningCase] = []
    for case in cases:
        if not case.correction.strip() or case.rating < MIN_RATING or _is_poison(case.correction):
            dropped.append(case)
        else:
            kept.append(case)
    return kept, dropped


async def distill(agent: Agent, kept: list[LearningCase]) -> str:
    if not kept:
        return ""
    parts = [
        f"Rating {case.rating}/5\nEmail:\n{case.email}\nCorrection:\n{case.correction}"
        for case in kept
    ]
    return (await _complete(agent, "\n\n".join(parts))).strip()


async def write_reply(agent: Agent, email: str, lessons: str = "") -> str:
    if lessons.strip():
        user = f"Learned lessons:\n{lessons.strip()}\n\nEmail:\n{email}"
    else:
        user = f"Learned lessons: (none)\n\nEmail:\n{email}"
    return await _complete(agent, user)


async def run(
    cases: list[LearningCase] | None = None,
    held_out: str | None = None,
) -> LearningResult:
    batch = cases if cases is not None else LEARNING_CASES
    probe = held_out if held_out is not None else LEARNING_HELD_OUT
    _ensure_otel()
    agents = build_agents()
    with get_tracer().start_as_current_span("pattern.learning") as span:
        span.set_attribute("pattern", "learning")
        span.set_attribute("backend", "maf")
        kept, dropped = clean_feedback(batch)
        lessons = await distill(agents["distill"], kept)
        baseline = await write_reply(agents["reply"], probe, lessons="")
        adapted = await write_reply(agents["reply"], probe, lessons=lessons)
        return LearningResult(
            kept=[_case_blob(case) for case in kept],
            dropped=[_case_blob(case) for case in dropped],
            lessons=lessons,
            held_out=probe,
            baseline=baseline,
            adapted=adapted,
        )


def main() -> None:
    print(asyncio.run(run()).model_dump_json(indent=2))
    provider = trace.get_tracer_provider()
    flush = getattr(provider, "force_flush", None)
    if callable(flush):
        flush()


if __name__ == "__main__":
    main()
