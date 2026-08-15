"""Human-in-the-loop: gate a support draft, pause for a reviewer, resume."""

from __future__ import annotations

import json
import re
from collections.abc import Callable
from typing import Any

from langfuse import get_client, observe, propagate_attributes
from pydantic import BaseModel

from sd_agentic_patterns.llm import complete
from sd_agentic_shared.env import load_env
from sd_agentic_shared.prompts import (
    DRAFT_SYSTEM,
    HITL_GATE_SYSTEM,
    HITL_RESUME_SYSTEM,
    SUMMARIZE_SYSTEM,
)
from sd_agentic_shared.tasks.support_email import HITL_DECISION, SUPPORT_EMAIL, HITLDecision

load_env()


class GateResult(BaseModel):
    risk: str
    reason: str
    needs_human: bool


class HITLResult(BaseModel):
    summary: str
    draft: str
    gate: GateResult
    decision: HITLDecision | None
    reply: str
    interrupted: bool


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


def _refund_over_50(text: str) -> bool:
    blob = text.lower()
    if "refund" not in blob and "chargeback" not in blob:
        return False
    for match in re.findall(r"\$(\d+(?:\.\d+)?)", blob):
        if float(match) > 50:
            return True
    return "full refund" in blob


@observe(name="step.summarize")
def summarize(email: str) -> str:
    return complete(SUMMARIZE_SYSTEM, email)


@observe(name="step.draft")
def draft_reply(email: str, summary: str) -> str:
    return complete(DRAFT_SYSTEM, f"Original email:\n{email}\n\nFact summary:\n{summary}")


@observe(name="step.gate")
def gate(email: str, draft: str) -> GateResult:
    user = f"Email:\n{email}\n\nDraft:\n{draft}"
    try:
        payload = _extract_json(complete(HITL_GATE_SYSTEM, user))
        risk = str(payload.get("risk") or "high").strip().lower()
        if risk not in {"high", "medium", "low"}:
            risk = "high"
        reason = str(payload.get("reason") or "").strip()
        needs_human = bool(payload.get("needs_human"))
    except (ValueError, json.JSONDecodeError, TypeError):
        risk, reason, needs_human = "high", "gate parse failed", True
    if _refund_over_50(email) or _refund_over_50(draft):
        needs_human = True
        if not reason:
            reason = "refund over $50 requires a human"
        risk = "high"
    return GateResult(risk=risk, reason=reason, needs_human=needs_human)


@observe(name="step.resume")
def resume(email: str, draft: str, decision: HITLDecision) -> str:
    action = decision.action.strip().lower()
    if action == "edit" and decision.edited_reply.strip():
        return decision.edited_reply.strip()
    user = (
        f"Action: {action}\nNote: {decision.note}\n\n"
        f"Edited text:\n{decision.edited_reply or '(none)'}\n\n"
        f"Draft:\n{draft}\n\nEmail:\n{email}"
    )
    return complete(HITL_RESUME_SYSTEM, user)


def default_reviewer(payload: dict[str, Any]) -> HITLDecision:
    _ = payload
    return HITL_DECISION


@observe(name="pattern.human_in_the_loop")
def run(
    email: str | None = None,
    reviewer: Callable[[dict[str, Any]], HITLDecision] | None = None,
) -> HITLResult:
    ticket = email if email is not None else SUPPORT_EMAIL
    decide = reviewer or default_reviewer
    with propagate_attributes(
        tags=["backend:scratch", "pattern:human_in_the_loop"],
        metadata={"pattern": "human_in_the_loop", "backend": "scratch"},
    ):
        summary = summarize(ticket)
        draft = draft_reply(ticket, summary)
        gate_result = gate(ticket, draft)
        if not gate_result.needs_human:
            return HITLResult(
                summary=summary,
                draft=draft,
                gate=gate_result,
                decision=None,
                reply=draft,
                interrupted=False,
            )
        decision = decide(
            {
                "email": ticket,
                "summary": summary,
                "draft": draft,
                "gate": gate_result.model_dump(),
            }
        )
        reply = resume(ticket, draft, decision)
        return HITLResult(
            summary=summary,
            draft=draft,
            gate=gate_result,
            decision=decision,
            reply=reply,
            interrupted=True,
        )


def main() -> None:
    print(run().model_dump_json(indent=2))
    get_client().flush()


if __name__ == "__main__":
    main()
