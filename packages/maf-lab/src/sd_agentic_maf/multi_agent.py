"""Multi-agent with MAF Agents in a coordinator → specialists → writer loop. Traces via OTEL."""

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
    BILLING_AGENT_SYSTEM,
    COORDINATOR_REVIEW_SYSTEM,
    COORDINATOR_SYSTEM,
    POLICY_AGENT_SYSTEM,
    SHIPPING_AGENT_SYSTEM,
    WRITER_AGENT_SYSTEM,
)
from sd_agentic_shared.tasks.support_email import SUPPORT_EMAIL

load_env()
_OTEL_READY = False

MAX_ROUNDS = 2
ROSTER = ("billing", "shipping", "policy")


class Assignment(BaseModel):
    agent: str
    instruction: str


class Note(BaseModel):
    agent: str
    text: str


class MultiAgentResult(BaseModel):
    assignments: list[Assignment]
    notes: list[Note]
    rounds: int
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


def build_agents() -> dict[str, Agent]:
    client = _client()
    return {
        "coordinator": Agent(client=client, name="coordinator", instructions=COORDINATOR_SYSTEM),
        "review": Agent(client=client, name="review", instructions=COORDINATOR_REVIEW_SYSTEM),
        "billing": Agent(client=client, name="billing", instructions=BILLING_AGENT_SYSTEM),
        "shipping": Agent(client=client, name="shipping", instructions=SHIPPING_AGENT_SYSTEM),
        "policy": Agent(client=client, name="policy", instructions=POLICY_AGENT_SYSTEM),
        "writer": Agent(client=client, name="writer", instructions=WRITER_AGENT_SYSTEM),
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


def _fallback_assignments() -> list[Assignment]:
    return [
        Assignment(agent=name, instruction="Write a short team note about your domain for this email.")
        for name in ROSTER
    ]


def _assignments_from_payload(payload: dict[str, Any]) -> list[Assignment]:
    items = payload.get("assignments") or []
    assignments: list[Assignment] = []
    seen: set[str] = set()
    for item in items:
        if not isinstance(item, dict):
            continue
        agent = str(item.get("agent") or "").strip().lower()
        if agent not in ROSTER or agent in seen:
            continue
        seen.add(agent)
        assignments.append(
            Assignment(
                agent=agent,
                instruction=str(item.get("instruction") or "Write a short team note."),
            )
        )
    if not assignments:
        raise ValueError("no valid assignments")
    return assignments


def _notes_blob(notes: list[Note]) -> str:
    if not notes:
        return "(none)"
    return "\n\n".join(f"[{item.agent}]\n{item.text}" for item in notes)


async def coordinate(agents: dict[str, Agent], email: str) -> list[Assignment]:
    raw = await _complete(agents["coordinator"], email)
    try:
        return _assignments_from_payload(_extract_json(raw))
    except (ValueError, json.JSONDecodeError, TypeError):
        return _fallback_assignments()


async def review(agents: dict[str, Agent], email: str, notes: list[Note]) -> list[Assignment]:
    user = f"Original email:\n{email}\n\nTeam notes:\n{_notes_blob(notes)}"
    raw = await _complete(agents["review"], user)
    if raw.strip().upper().startswith("DONE"):
        return []
    try:
        return _assignments_from_payload(_extract_json(raw))
    except (ValueError, json.JSONDecodeError, TypeError):
        return []


async def run_specialist(
    agents: dict[str, Agent],
    agent: str,
    email: str,
    instruction: str,
    notes: list[Note],
) -> Note:
    user = (
        f"Original email:\n{email}\n\n"
        f"Your instruction:\n{instruction}\n\n"
        f"Notes so far:\n{_notes_blob(notes)}"
    )
    text = await _complete(agents[agent], user)
    return Note(agent=agent, text=text)


async def write_reply(agents: dict[str, Agent], email: str, notes: list[Note]) -> str:
    user = f"Original email:\n{email}\n\nTeam notes:\n{_notes_blob(notes)}"
    return await _complete(agents["writer"], user)


async def run(email: str) -> MultiAgentResult:
    _ensure_otel()
    agents = build_agents()
    with get_tracer().start_as_current_span("pattern.multi_agent") as span:
        span.set_attribute("pattern", "multi_agent")
        span.set_attribute("backend", "maf")
        all_assignments: list[Assignment] = []
        notes: list[Note] = []
        rounds = 0
        pending = await coordinate(agents, email)
        while pending and rounds < MAX_ROUNDS:
            all_assignments.extend(pending)
            rounds += 1
            for item in pending:
                notes.append(
                    await run_specialist(agents, item.agent, email, item.instruction, notes)
                )
            pending = await review(agents, email, notes) if rounds < MAX_ROUNDS else []
        reply = await write_reply(agents, email, notes)
        return MultiAgentResult(
            assignments=all_assignments,
            notes=notes,
            rounds=rounds,
            reply=reply,
        )


def main() -> None:
    print(asyncio.run(run(SUPPORT_EMAIL)).model_dump_json(indent=2))
    provider = trace.get_tracer_provider()
    flush = getattr(provider, "force_flush", None)
    if callable(flush):
        flush()


if __name__ == "__main__":
    main()
