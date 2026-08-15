"""Reflection: draft → critic → revise until PASS or max rounds."""

from __future__ import annotations

from langfuse import get_client, observe, propagate_attributes
from pydantic import BaseModel

from sd_agentic_patterns.llm import complete
from sd_agentic_shared.env import load_env
from sd_agentic_shared.prompts import CRITIC_SYSTEM, DRAFT_SYSTEM, REVISE_SYSTEM, SUMMARIZE_SYSTEM
from sd_agentic_shared.tasks.support_email import SUPPORT_EMAIL

load_env()

MAX_ROUNDS = 3


class ReflectionRound(BaseModel):
    draft: str
    critique: str


class ReflectionResult(BaseModel):
    summary: str
    rounds: list[ReflectionRound]
    final: str
    passed: bool


@observe(name="step.summarize")
def summarize(email: str) -> str:
    return complete(SUMMARIZE_SYSTEM, email)


@observe(name="step.draft")
def draft_reply(email: str, summary: str) -> str:
    return complete(DRAFT_SYSTEM, f"Original email:\n{email}\n\nFact summary:\n{summary}")


@observe(name="step.critic")
def critique(email: str, draft: str) -> str:
    return complete(CRITIC_SYSTEM, f"Original email:\n{email}\n\nDraft:\n{draft}")


@observe(name="step.revise")
def revise(email: str, draft: str, critique_text: str) -> str:
    user = (
        f"Original email:\n{email}\n\n"
        f"Current draft:\n{draft}\n\n"
        f"Critic:\n{critique_text}"
    )
    return complete(REVISE_SYSTEM, user)


def _passed(critique_text: str) -> bool:
    return critique_text.strip().upper().startswith("PASS")


@observe(name="pattern.reflection")
def run(email: str, max_rounds: int = MAX_ROUNDS) -> ReflectionResult:
    with propagate_attributes(
        tags=["backend:scratch", "pattern:reflection"],
        metadata={"pattern": "reflection", "backend": "scratch"},
    ):
        summary = summarize(email)
        draft = draft_reply(email, summary)
        rounds: list[ReflectionRound] = []
        passed = False
        for _ in range(max_rounds):
            critique_text = critique(email, draft)
            rounds.append(ReflectionRound(draft=draft, critique=critique_text))
            if _passed(critique_text):
                passed = True
                break
            draft = revise(email, draft, critique_text)
        return ReflectionResult(
            summary=summary,
            rounds=rounds,
            final=draft,
            passed=passed,
        )


def main() -> None:
    print(run(SUPPORT_EMAIL).model_dump_json(indent=2))
    get_client().flush()


if __name__ == "__main__":
    main()
