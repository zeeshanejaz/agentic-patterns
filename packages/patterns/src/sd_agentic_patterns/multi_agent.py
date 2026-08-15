"""Multi-agent: coordinator assigns specialists, they share notes, a writer replies."""

from __future__ import annotations

import json
from typing import Any

from langfuse import get_client, observe, propagate_attributes
from pydantic import BaseModel

from sd_agentic_patterns.llm import complete
from sd_agentic_shared.env import load_env
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

MAX_ROUNDS = 2
ROSTER = ("billing", "shipping", "policy")
AGENT_SYSTEMS: dict[str, str] = {
    "billing": BILLING_AGENT_SYSTEM,
    "shipping": SHIPPING_AGENT_SYSTEM,
    "policy": POLICY_AGENT_SYSTEM,
}


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


@observe(name="step.coordinate")
def coordinate(email: str) -> list[Assignment]:
    raw = complete(COORDINATOR_SYSTEM, email)
    try:
        return _assignments_from_payload(_extract_json(raw))
    except (ValueError, json.JSONDecodeError, TypeError):
        return _fallback_assignments()


@observe(name="step.review")
def review(email: str, notes: list[Note]) -> list[Assignment]:
    user = f"Original email:\n{email}\n\nTeam notes:\n{_notes_blob(notes)}"
    raw = complete(COORDINATOR_REVIEW_SYSTEM, user)
    if raw.strip().upper().startswith("DONE"):
        return []
    try:
        return _assignments_from_payload(_extract_json(raw))
    except (ValueError, json.JSONDecodeError, TypeError):
        return []


@observe(name="step.specialist")
def run_specialist(agent: str, email: str, instruction: str, notes: list[Note]) -> Note:
    user = (
        f"Original email:\n{email}\n\n"
        f"Your instruction:\n{instruction}\n\n"
        f"Notes so far:\n{_notes_blob(notes)}"
    )
    text = complete(AGENT_SYSTEMS[agent], user)
    return Note(agent=agent, text=text)


@observe(name="step.write")
def write_reply(email: str, notes: list[Note]) -> str:
    user = f"Original email:\n{email}\n\nTeam notes:\n{_notes_blob(notes)}"
    return complete(WRITER_AGENT_SYSTEM, user)


@observe(name="pattern.multi_agent")
def run(email: str) -> MultiAgentResult:
    with propagate_attributes(
        tags=["backend:scratch", "pattern:multi_agent"],
        metadata={"pattern": "multi_agent", "backend": "scratch"},
    ):
        all_assignments: list[Assignment] = []
        notes: list[Note] = []
        rounds = 0
        pending = coordinate(email)
        while pending and rounds < MAX_ROUNDS:
            all_assignments.extend(pending)
            rounds += 1
            for item in pending:
                notes.append(run_specialist(item.agent, email, item.instruction, notes))
            pending = review(email, notes) if rounds < MAX_ROUNDS else []
        reply = write_reply(email, notes)
        return MultiAgentResult(
            assignments=all_assignments,
            notes=notes,
            rounds=rounds,
            reply=reply,
        )


def main() -> None:
    print(run(SUPPORT_EMAIL).model_dump_json(indent=2))
    get_client().flush()


if __name__ == "__main__":
    main()
