"""Prompt chaining from scratch: summarize → draft reply → policy check."""

from __future__ import annotations

from langfuse import get_client, observe, propagate_attributes

from sd_agentic_patterns.llm import complete
from sd_agentic_shared.env import load_env
from sd_agentic_shared.prompts import CHECK_SYSTEM, DRAFT_SYSTEM, SUMMARIZE_SYSTEM
from sd_agentic_shared.tasks.support_email import SUPPORT_EMAIL, TicketDraft

load_env()


@observe(name="step.summarize")
def summarize(email: str) -> str:
    return complete(SUMMARIZE_SYSTEM, email)


@observe(name="step.draft")
def draft_reply(email: str, summary: str) -> str:
    user = f"Original email:\n{email}\n\nFact summary:\n{summary}"
    return complete(DRAFT_SYSTEM, user)


@observe(name="step.check")
def check_policy(email: str, summary: str, reply: str) -> str:
    user = (
        f"Original email:\n{email}\n\n"
        f"Summary:\n{summary}\n\n"
        f"Draft reply:\n{reply}"
    )
    return complete(CHECK_SYSTEM, user)


@observe(name="pattern.prompt_chaining")
def run(email: str) -> TicketDraft:
    with propagate_attributes(
        tags=["backend:scratch", "pattern:chaining"],
        metadata={"pattern": "prompt_chaining", "backend": "scratch"},
    ):
        summary = summarize(email)
        reply = draft_reply(email, summary)
        policy_ok = check_policy(email, summary, reply)
        return TicketDraft(summary=summary, reply=reply, policy_ok=policy_ok)


def main() -> None:
    result = run(SUPPORT_EMAIL)
    print(result.model_dump_json(indent=2))
    get_client().flush()


if __name__ == "__main__":
    main()
