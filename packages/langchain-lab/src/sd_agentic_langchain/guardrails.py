"""Guardrails: LCEL input/output scans around a support draft."""

from __future__ import annotations

import json
import re
from typing import Any

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langfuse import get_client, observe, propagate_attributes
from langfuse.langchain import CallbackHandler
from pydantic import BaseModel

from sd_agentic_shared.env import load_env, openai_model
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


def _llm() -> ChatOpenAI:
    return ChatOpenAI(model=openai_model())


def _text_chain(system: str):
    prompt = ChatPromptTemplate.from_messages(
        [("system", system), ("human", "{user}")]
    )
    return prompt | _llm() | StrOutputParser()


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
        tags=["backend:langchain", "pattern:guardrails"],
        metadata={"pattern": "guardrails", "backend": "langchain"},
    ):
        handler = CallbackHandler()
        config = {"callbacks": [handler]}
        in_ok, in_violations = _parse_guard(
            _text_chain(GUARDRAIL_INPUT_SYSTEM).invoke({"user": ticket}, config=config)
        )
        summary = _text_chain(SUMMARIZE_SYSTEM).invoke({"user": ticket}, config=config)
        draft = _text_chain(DRAFT_SYSTEM).invoke(
            {"user": f"Original email:\n{ticket}\n\nFact summary:\n{summary}"},
            config=config,
        )
        out_ok, out_violations = _parse_guard(
            _text_chain(GUARDRAIL_OUTPUT_SYSTEM).invoke(
                {"user": f"Email:\n{ticket}\n\nDraft:\n{draft}"},
                config=config,
            )
        )
        if _promises_over_50(draft):
            out_ok = False
            out_violations = list(out_violations) + ["heuristic: promised refund over $50"]
        violations = [f"input: {item}" for item in in_violations] + [
            f"output: {item}" for item in out_violations
        ]
        reply = draft
        if not in_ok or not out_ok:
            reply = _text_chain(DRAFT_SYSTEM).invoke(
                {
                    "user": (
                        f"Original email:\n{ticket}\n\nFact summary:\n{summary}\n\n"
                        f"The previous draft failed guards: {violations}. "
                        f"Rewrite. Do not promise a refund over $50."
                    )
                },
                config=config,
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
