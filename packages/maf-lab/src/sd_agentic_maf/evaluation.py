"""Evaluation with MAF Agents: summarize/draft plus heuristics and an LLM judge."""

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
from sd_agentic_shared.prompts import DRAFT_SYSTEM, EVAL_JUDGE_SYSTEM, SUMMARIZE_SYSTEM
from sd_agentic_shared.tasks.support_email import EVAL_CASES, EvalCase

load_env()
_OTEL_READY = False

BLAME_MARKERS = ("your fault", "their fault", "you should have", "stupid")


class JudgeVerdict(BaseModel):
    passed: bool
    score: int
    reason: str


class CaseEval(BaseModel):
    id: str
    heuristic_ok: bool
    heuristic_violations: list[str]
    judge_pass: bool
    judge_score: int
    judge_reason: str
    overall_pass: bool
    reply: str


class EvalReport(BaseModel):
    pass_rate: float
    cases: list[CaseEval]


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


def _promises_over_50(text: str) -> bool:
    blob = text.lower()
    if "refund" not in blob:
        return False
    for match in re.findall(r"\$(\d+(?:\.\d+)?)", blob):
        if float(match) > 50:
            return True
    return False


def _heuristics(case: EvalCase, reply: str) -> list[str]:
    violations: list[str] = []
    blob = reply.lower()
    if _promises_over_50(reply):
        violations.append("promised refund over $50")
    if case.must_mention and not any(token.lower() in blob for token in case.must_mention):
        violations.append(f"missing required id ({', '.join(case.must_mention)})")
    if any(marker in blob for marker in BLAME_MARKERS):
        violations.append("blames the customer")
    return violations


def _parse_judge(raw: str) -> JudgeVerdict:
    try:
        payload = _extract_json(raw)
        score = int(payload.get("score") or 0)
        score = max(1, min(5, score))
        passed = bool(payload.get("pass"))
        reason = str(payload.get("reason") or "").strip() or "no reason"
        return JudgeVerdict(passed=passed, score=score, reason=reason)
    except (ValueError, json.JSONDecodeError, TypeError):
        return JudgeVerdict(passed=False, score=1, reason="judge parse failed")


async def run(cases: list[EvalCase] | None = None) -> EvalReport:
    inbox = cases if cases is not None else EVAL_CASES
    _ensure_otel()
    client = _client()
    agents = {
        "summarize": Agent(client=client, name="summarize", instructions=SUMMARIZE_SYSTEM),
        "draft": Agent(client=client, name="draft", instructions=DRAFT_SYSTEM),
        "judge": Agent(client=client, name="judge", instructions=EVAL_JUDGE_SYSTEM),
    }
    with get_tracer().start_as_current_span("pattern.evaluation") as span:
        span.set_attribute("pattern", "evaluation")
        span.set_attribute("backend", "maf")
        results: list[CaseEval] = []
        for case in inbox:
            summary = (await agents["summarize"].run(case.email)).text or ""
            reply = (
                await agents["draft"].run(
                    f"Original email:\n{case.email}\n\nFact summary:\n{summary}"
                )
            ).text or ""
            violations = _heuristics(case, reply)
            judge = _parse_judge(
                (await agents["judge"].run(f"Email:\n{case.email}\n\nDraft:\n{reply}")).text or ""
            )
            heuristic_ok = not violations
            results.append(
                CaseEval(
                    id=case.id,
                    heuristic_ok=heuristic_ok,
                    heuristic_violations=violations,
                    judge_pass=judge.passed,
                    judge_score=judge.score,
                    judge_reason=judge.reason,
                    overall_pass=heuristic_ok and judge.passed,
                    reply=reply,
                )
            )
        passed = sum(1 for item in results if item.overall_pass)
        rate = (passed / len(results)) if results else 0.0
        return EvalReport(pass_rate=rate, cases=results)


def main() -> None:
    print(asyncio.run(run()).model_dump_json(indent=2))
    provider = trace.get_tracer_provider()
    flush = getattr(provider, "force_flush", None)
    if callable(flush):
        flush()


if __name__ == "__main__":
    main()
