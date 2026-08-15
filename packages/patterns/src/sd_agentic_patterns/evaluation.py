"""Evaluation: golden cases, heuristics, and an LLM judge around summarize/draft."""

from __future__ import annotations

import json
import re
from typing import Any

from langfuse import get_client, observe, propagate_attributes
from pydantic import BaseModel

from sd_agentic_patterns.llm import complete
from sd_agentic_shared.env import load_env
from sd_agentic_shared.prompts import DRAFT_SYSTEM, EVAL_JUDGE_SYSTEM, SUMMARIZE_SYSTEM
from sd_agentic_shared.tasks.support_email import EVAL_CASES, EvalCase

load_env()

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


@observe(name="step.evaluate_case")
def evaluate_case(case: EvalCase) -> CaseEval:
    summary = complete(SUMMARIZE_SYSTEM, case.email)
    reply = complete(
        DRAFT_SYSTEM,
        f"Original email:\n{case.email}\n\nFact summary:\n{summary}",
    )
    violations = _heuristics(case, reply)
    judge = _parse_judge(
        complete(
            EVAL_JUDGE_SYSTEM,
            f"Email:\n{case.email}\n\nDraft:\n{reply}",
        )
    )
    heuristic_ok = not violations
    overall = heuristic_ok and judge.passed
    return CaseEval(
        id=case.id,
        heuristic_ok=heuristic_ok,
        heuristic_violations=violations,
        judge_pass=judge.passed,
        judge_score=judge.score,
        judge_reason=judge.reason,
        overall_pass=overall,
        reply=reply,
    )


@observe(name="pattern.evaluation")
def run(cases: list[EvalCase] | None = None) -> EvalReport:
    inbox = cases if cases is not None else EVAL_CASES
    with propagate_attributes(
        tags=["backend:scratch", "pattern:evaluation"],
        metadata={"pattern": "evaluation", "backend": "scratch"},
    ):
        results = [evaluate_case(case) for case in inbox]
        passed = sum(1 for item in results if item.overall_pass)
        rate = (passed / len(results)) if results else 0.0
        return EvalReport(pass_rate=rate, cases=results)


def main() -> None:
    print(run().model_dump_json(indent=2))
    get_client().flush()


if __name__ == "__main__":
    main()
