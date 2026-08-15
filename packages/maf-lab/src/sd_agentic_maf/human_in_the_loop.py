"""Human-in-the-loop with MAF Agents and a canned reviewer. Traces via OTEL."""

from __future__ import annotations

import asyncio
import json
import re
from collections.abc import Callable
from typing import Any

from agent_framework import Agent
from agent_framework.observability import get_tracer
from agent_framework.openai import OpenAIChatClient
from opentelemetry import trace
from pydantic import BaseModel

from sd_agentic_maf.otel import configure_maf_otel
from sd_agentic_shared.env import load_env, openai_model, workspace_root
from sd_agentic_shared.prompts import (
    DRAFT_SYSTEM,
    HITL_GATE_SYSTEM,
    HITL_RESUME_SYSTEM,
    SUMMARIZE_SYSTEM,
)
from sd_agentic_shared.tasks.support_email import HITL_DECISION, SUPPORT_EMAIL, HITLDecision

load_env()
_OTEL_READY = False


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
        "summarize": Agent(client=client, name="summarize", instructions=SUMMARIZE_SYSTEM),
        "draft": Agent(client=client, name="draft", instructions=DRAFT_SYSTEM),
        "gate": Agent(client=client, name="gate", instructions=HITL_GATE_SYSTEM),
        "resume": Agent(client=client, name="resume", instructions=HITL_RESUME_SYSTEM),
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


def _refund_over_50(text: str) -> bool:
    blob = text.lower()
    if "refund" not in blob and "chargeback" not in blob:
        return False
    for match in re.findall(r"\$(\d+(?:\.\d+)?)", blob):
        if float(match) > 50:
            return True
    return "full refund" in blob


def _parse_gate(email: str, draft: str, raw: str) -> GateResult:
    try:
        payload = _extract_json(raw)
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


def default_reviewer(payload: dict[str, Any]) -> HITLDecision:
    _ = payload
    return HITL_DECISION


async def run(
    email: str | None = None,
    reviewer: Callable[[dict[str, Any]], HITLDecision] | None = None,
) -> HITLResult:
    ticket = email if email is not None else SUPPORT_EMAIL
    decide = reviewer or default_reviewer
    _ensure_otel()
    agents = build_agents()
    with get_tracer().start_as_current_span("pattern.human_in_the_loop") as span:
        span.set_attribute("pattern", "human_in_the_loop")
        span.set_attribute("backend", "maf")
        summary = await _complete(agents["summarize"], ticket)
        draft = await _complete(
            agents["draft"],
            f"Original email:\n{ticket}\n\nFact summary:\n{summary}",
        )
        gate = _parse_gate(
            ticket,
            draft,
            await _complete(
                agents["gate"],
                f"Email:\n{ticket}\n\nDraft:\n{draft}",
            ),
        )
        if not gate.needs_human:
            return HITLResult(
                summary=summary,
                draft=draft,
                gate=gate,
                decision=None,
                reply=draft,
                interrupted=False,
            )
        decision = decide(
            {
                "email": ticket,
                "summary": summary,
                "draft": draft,
                "gate": gate.model_dump(),
            }
        )
        action = decision.action.strip().lower()
        if action == "edit" and decision.edited_reply.strip():
            reply = decision.edited_reply.strip()
        else:
            reply = await _complete(
                agents["resume"],
                (
                    f"Action: {action}\nNote: {decision.note}\n\n"
                    f"Edited text:\n{decision.edited_reply or '(none)'}\n\n"
                    f"Draft:\n{draft}\n\nEmail:\n{ticket}"
                ),
            )
        return HITLResult(
            summary=summary,
            draft=draft,
            gate=gate,
            decision=decision,
            reply=reply,
            interrupted=True,
        )


def main() -> None:
    print(asyncio.run(run()).model_dump_json(indent=2))
    provider = trace.get_tracer_provider()
    flush = getattr(provider, "force_flush", None)
    if callable(flush):
        flush()


if __name__ == "__main__":
    main()
