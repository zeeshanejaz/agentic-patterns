"""Guardrails: input and output checks around a support draft, rewrite on fail."""

from __future__ import annotations

import json
import re
from typing import Any

from langfuse import get_client, observe, propagate_attributes
from pydantic import BaseModel

from sd_agentic_patterns.llm import complete
from sd_agentic_shared.env import load_env
from sd_agentic_shared.prompts import (
    DRAFT_SYSTEM,
    GUARDRAIL_INPUT_SYSTEM,
    GUARDRAIL_OUTPUT_SYSTEM,
    SUMMARIZE_SYSTEM,
)
from sd_agentic_shared.tasks.support_email import SUPPORT_EMAIL

load_env()


class GuardResult(BaseModel):
    input_ok: bool
    output_ok: bool
    violations: list[str]
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


@observe(name="pattern.guardrails")
def run(email: str | None = None) -> GuardResult:
    ticket = email if email is not None else SUPPORT_EMAIL
    with propagate_attributes(
        tags=["backend:scratch", "pattern:guardrails"],
        metadata={"pattern": "guardrails", "backend": "scratch"},
    ):
        in_ok, in_violations = _parse_guard(complete(GUARDRAIL_INPUT_SYSTEM, ticket))
        summary = complete(SUMMARIZE_SYSTEM, ticket)
        draft = complete(DRAFT_SYSTEM, f"Original email:\n{ticket}\n\nFact summary:\n{summary}")
        out_ok, out_violations = _parse_guard(
            complete(GUARDRAIL_OUTPUT_SYSTEM, f"Email:\n{ticket}\n\nDraft:\n{draft}")
        )
        if _promises_over_50(draft):
            out_ok = False
            out_violations = list(out_violations) + ["heuristic: promised refund over $50"]
        violations = [f"input: {item}" for item in in_violations] + [
            f"output: {item}" for item in out_violations
        ]
        reply = draft
        if not in_ok or not out_ok:
            reply = complete(
                DRAFT_SYSTEM,
                (
                    f"Original email:\n{ticket}\n\nFact summary:\n{summary}\n\n"
                    f"The previous draft failed guards: {violations}. "
                    f"Rewrite. Do not promise a refund over $50."
                ),
            )
        return GuardResult(
            input_ok=in_ok,
            output_ok=out_ok,
            violations=violations,
            reply=reply,
        )


def main() -> None:
    print(run().model_dump_json(indent=2))
    get_client().flush()


if __name__ == "__main__":
    main()
