"""Learning and adaptation: collect feedback, distill lessons, A/B baseline vs adapted."""

from __future__ import annotations

import re

from langfuse import get_client, observe, propagate_attributes
from pydantic import BaseModel

from sd_agentic_patterns.llm import complete
from sd_agentic_shared.env import load_env
from sd_agentic_shared.prompts import LEARNING_DISTILL_SYSTEM, LEARNING_REPLY_SYSTEM
from sd_agentic_shared.tasks.support_email import LEARNING_CASES, LEARNING_HELD_OUT, LearningCase

load_env()

MIN_RATING = 2
POISON_MARKERS = (
    "invent tracking",
    "invent order",
    "blame",
    "their fault",
    "your fault",
    "stupid",
)


class LearningResult(BaseModel):
    kept: list[dict[str, object]]
    dropped: list[dict[str, object]]
    lessons: str
    held_out: str
    baseline: str
    adapted: str


def _is_poison(correction: str) -> bool:
    blob = correction.lower()
    if any(marker in blob for marker in POISON_MARKERS):
        return True
    for match in re.findall(r"\$(\d+(?:\.\d+)?)", blob):
        if float(match) > 50:
            return True
    return False


def _case_blob(case: LearningCase) -> dict[str, object]:
    return {"email": case.email, "rating": case.rating, "correction": case.correction}


@observe(name="step.clean")
def clean_feedback(cases: list[LearningCase]) -> tuple[list[LearningCase], list[LearningCase]]:
    kept: list[LearningCase] = []
    dropped: list[LearningCase] = []
    for case in cases:
        if not case.correction.strip() or case.rating < MIN_RATING or _is_poison(case.correction):
            dropped.append(case)
        else:
            kept.append(case)
    return kept, dropped


@observe(name="step.distill")
def distill(kept: list[LearningCase]) -> str:
    if not kept:
        return ""
    parts = [
        f"Rating {case.rating}/5\nEmail:\n{case.email}\nCorrection:\n{case.correction}"
        for case in kept
    ]
    return complete(LEARNING_DISTILL_SYSTEM, "\n\n".join(parts)).strip()


@observe(name="step.reply")
def write_reply(email: str, lessons: str = "") -> str:
    if lessons.strip():
        user = f"Learned lessons:\n{lessons.strip()}\n\nEmail:\n{email}"
    else:
        user = f"Learned lessons: (none)\n\nEmail:\n{email}"
    return complete(LEARNING_REPLY_SYSTEM, user)


@observe(name="pattern.learning")
def run(
    cases: list[LearningCase] | None = None,
    held_out: str | None = None,
) -> LearningResult:
    batch = cases if cases is not None else LEARNING_CASES
    probe = held_out if held_out is not None else LEARNING_HELD_OUT
    with propagate_attributes(
        tags=["backend:scratch", "pattern:learning"],
        metadata={"pattern": "learning", "backend": "scratch"},
    ):
        kept, dropped = clean_feedback(batch)
        lessons = distill(kept)
        baseline = write_reply(probe, lessons="")
        adapted = write_reply(probe, lessons=lessons)
        return LearningResult(
            kept=[_case_blob(case) for case in kept],
            dropped=[_case_blob(case) for case in dropped],
            lessons=lessons,
            held_out=probe,
            baseline=baseline,
            adapted=adapted,
        )


def main() -> None:
    print(run().model_dump_json(indent=2))
    get_client().flush()


if __name__ == "__main__":
    main()
