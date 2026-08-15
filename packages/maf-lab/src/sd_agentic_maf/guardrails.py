"""Guardrails with MAF Agents around a support draft. Traces via OTEL."""

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
from sd_agentic_shared.prompts import (
    DRAFT_SYSTEM,
    GUARDRAIL_INPUT_SYSTEM,
    GUARDRAIL_OUTPUT_SYSTEM,
    SUMMARIZE_SYSTEM,
)
from sd_agentic_shared.tasks.support_email import SUPPORT_EMAIL

load_env()
_OTEL_READY = False


class GuardResult(BaseModel):
    input_ok: bool
    output_ok: bool
    violations: list[str]
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


def _parse_guard(raw: str) -> tuple[bool, list[str]]:
    try:
        payload = _extract_json(raw)
        ok = bool(payload.get("ok"))
        violations = [str(item).strip() for item in (payload.get("violations") or []) if str(item).strip()]
        return ok, violations
    except (ValueError, json.JSONDecodeError, TypeError):
        return False, ["guard parse failed"]


def _promises_over_50(text: str) -> bool:
    blob = text.lower()
    if "refund" not in blob:
        return False
    for match in re.findall(r"\$(\d+(?:\.\d+)?)", blob):
        if float(match) > 50:
            return True
    return False


async def run(email: str | None = None) -> GuardResult:
    ticket = email if email is not None else SUPPORT_EMAIL
    _ensure_otel()
    client = _client()
    agents = {
        "input": Agent(client=client, name="input_guard", instructions=GUARDRAIL_INPUT_SYSTEM),
        "summarize": Agent(client=client, name="summarize", instructions=SUMMARIZE_SYSTEM),
        "draft": Agent(client=client, name="draft", instructions=DRAFT_SYSTEM),
        "output": Agent(client=client, name="output_guard", instructions=GUARDRAIL_OUTPUT_SYSTEM),
    }
    with get_tracer().start_as_current_span("pattern.guardrails") as span:
        span.set_attribute("pattern", "guardrails")
        span.set_attribute("backend", "maf")
        in_ok, in_violations = _parse_guard((await agents["input"].run(ticket)).text or "")
        summary = (await agents["summarize"].run(ticket)).text or ""
        draft = (
            await agents["draft"].run(
                f"Original email:\n{ticket}\n\nFact summary:\n{summary}"
            )
        ).text or ""
        out_ok, out_violations = _parse_guard(
            (
                await agents["output"].run(f"Email:\n{ticket}\n\nDraft:\n{draft}")
            ).text
            or ""
        )
        if _promises_over_50(draft):
            out_ok = False
            out_violations = list(out_violations) + ["heuristic: promised refund over $50"]
        violations = [f"input: {item}" for item in in_violations] + [
            f"output: {item}" for item in out_violations
        ]
        reply = draft
        if not in_ok or not out_ok:
            reply = (
                await agents["draft"].run(
                    f"Original email:\n{ticket}\n\nFact summary:\n{summary}\n\n"
                    f"The previous draft failed guards: {violations}. "
                    f"Rewrite. Do not promise a refund over $50."
                )
            ).text or ""
        return GuardResult(
            input_ok=in_ok,
            output_ok=out_ok,
            violations=violations,
            reply=reply,
        )


def main() -> None:
    print(asyncio.run(run()).model_dump_json(indent=2))
    provider = trace.get_tracer_provider()
    flush = getattr(provider, "force_flush", None)
    if callable(flush):
        flush()


if __name__ == "__main__":
    main()
