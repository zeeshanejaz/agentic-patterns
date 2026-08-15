"""Reasoning with MAF Agents: two CoT samples. Traces via OTEL."""

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
from sd_agentic_shared.prompts import REASONING_SYSTEM
from sd_agentic_shared.tasks.support_email import SUPPORT_EMAIL

load_env()
_OTEL_READY = False

N_SAMPLES = 2


class ReasoningSample(BaseModel):
    steps: list[str]
    reply: str


class ReasoningResult(BaseModel):
    samples: list[ReasoningSample]
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


async def run(email: str | None = None) -> ReasoningResult:
    ticket = email if email is not None else SUPPORT_EMAIL
    _ensure_otel()
    agent = Agent(client=_client(), name="reason", instructions=REASONING_SYSTEM)
    with get_tracer().start_as_current_span("pattern.reasoning") as span:
        span.set_attribute("pattern", "reasoning")
        span.set_attribute("backend", "maf")
        samples = [
            _parse_sample((await agent.run(ticket)).text or "")
            for _ in range(N_SAMPLES)
        ]
        return ReasoningResult(samples=samples, reply=samples[0].reply)


def main() -> None:
    print(asyncio.run(run()).model_dump_json(indent=2))
    provider = trace.get_tracer_provider()
    flush = getattr(provider, "force_flush", None)
    if callable(flush):
        flush()


if __name__ == "__main__":
    main()
