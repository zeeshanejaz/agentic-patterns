"""Reflection with MAF Agents in a draft → critic → revise loop. Traces via OTEL."""

from __future__ import annotations

import asyncio

from agent_framework import Agent
from agent_framework.observability import get_tracer
from agent_framework.openai import OpenAIChatClient
from opentelemetry import trace
from pydantic import BaseModel

from sd_agentic_maf.otel import configure_maf_otel
from sd_agentic_shared.env import load_env, openai_model, workspace_root
from sd_agentic_shared.prompts import CRITIC_SYSTEM, DRAFT_SYSTEM, REVISE_SYSTEM, SUMMARIZE_SYSTEM
from sd_agentic_shared.tasks.support_email import SUPPORT_EMAIL

load_env()
_OTEL_READY = False

MAX_ROUNDS = 3


class ReflectionRound(BaseModel):
    draft: str
    critique: str


class ReflectionResult(BaseModel):
    summary: str
    rounds: list[ReflectionRound]
    final: str
    passed: bool


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


def _passed(critique_text: str) -> bool:
    return critique_text.strip().upper().startswith("PASS")


def build_agents() -> dict[str, Agent]:
    client = _client()
    return {
        "summarize": Agent(client=client, name="summarize", instructions=SUMMARIZE_SYSTEM),
        "draft": Agent(client=client, name="draft", instructions=DRAFT_SYSTEM),
        "critic": Agent(client=client, name="critic", instructions=CRITIC_SYSTEM),
        "revise": Agent(client=client, name="revise", instructions=REVISE_SYSTEM),
    }


async def run(email: str, max_rounds: int = MAX_ROUNDS) -> ReflectionResult:
    _ensure_otel()
    agents = build_agents()
    with get_tracer().start_as_current_span("pattern.reflection") as span:
        span.set_attribute("pattern", "reflection")
        span.set_attribute("backend", "maf")
        summary = (await agents["summarize"].run(email)).text or ""
        draft = (
            await agents["draft"].run(
                f"Original email:\n{email}\n\nFact summary:\n{summary}"
            )
        ).text or ""
        rounds: list[ReflectionRound] = []
        passed = False
        for _ in range(max_rounds):
            critique_text = (
                await agents["critic"].run(
                    f"Original email:\n{email}\n\nDraft:\n{draft}"
                )
            ).text or ""
            rounds.append(ReflectionRound(draft=draft, critique=critique_text))
            if _passed(critique_text):
                passed = True
                break
            draft = (
                await agents["revise"].run(
                    f"Original email:\n{email}\n\n"
                    f"Current draft:\n{draft}\n\n"
                    f"Critic:\n{critique_text}"
                )
            ).text or ""
        return ReflectionResult(
            summary=summary,
            rounds=rounds,
            final=draft,
            passed=passed,
        )


def main() -> None:
    print(asyncio.run(run(SUPPORT_EMAIL)).model_dump_json(indent=2))
    provider = trace.get_tracer_provider()
    flush = getattr(provider, "force_flush", None)
    if callable(flush):
        flush()


if __name__ == "__main__":
    main()
