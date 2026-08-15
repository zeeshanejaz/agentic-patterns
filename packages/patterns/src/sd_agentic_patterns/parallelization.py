"""Parallelization: sectioning (split work) and voting (N drafts, then merge)."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

from langfuse import get_client, observe, propagate_attributes
from pydantic import BaseModel

from sd_agentic_patterns.llm import complete
from sd_agentic_shared.env import load_env
from sd_agentic_shared.prompts import (
    MERGE_SECTIONS_SYSTEM,
    SECTION_ASK_SYSTEM,
    SECTION_ORDER_SYSTEM,
    SECTION_PAYMENT_SYSTEM,
    VOTE_MERGE_SYSTEM,
)
from sd_agentic_shared.tasks.support_email import SUPPORT_EMAIL

load_env()


class SectionResult(BaseModel):
    order: str
    payment: str
    ask: str
    summary: str


class VoteResult(BaseModel):
    drafts: list[str]
    merged: str


@observe(name="step.section_order")
def section_order(email: str) -> str:
    return complete(SECTION_ORDER_SYSTEM, email)


@observe(name="step.section_payment")
def section_payment(email: str) -> str:
    return complete(SECTION_PAYMENT_SYSTEM, email)


@observe(name="step.section_ask")
def section_ask(email: str) -> str:
    return complete(SECTION_ASK_SYSTEM, email)


@observe(name="step.merge_sections")
def merge_sections(order: str, payment: str, ask: str) -> str:
    user = f"Order facts:\n{order}\n\nPayment facts:\n{payment}\n\nCustomer ask:\n{ask}"
    return complete(MERGE_SECTIONS_SYSTEM, user)


@observe(name="pattern.parallelization.sectioning")
def run_sectioning(email: str) -> SectionResult:
    with propagate_attributes(
        tags=["backend:scratch", "pattern:parallelization"],
        metadata={"pattern": "parallelization", "mode": "sectioning", "backend": "scratch"},
    ):
        with ThreadPoolExecutor(max_workers=3) as pool:
            order_f = pool.submit(section_order, email)
            payment_f = pool.submit(section_payment, email)
            ask_f = pool.submit(section_ask, email)
            order = order_f.result()
            payment = payment_f.result()
            ask = ask_f.result()
        summary = merge_sections(order, payment, ask)
        return SectionResult(order=order, payment=payment, ask=ask, summary=summary)


@observe(name="step.vote_draft")
def vote_draft(email: str, index: int) -> str:
    system = (
        "Write a short support reply to the email. Do not invent tracking, "
        "order status, or refund amounts. Worker "
        f"{index}."
    )
    return complete(system, email, temperature=0.8)


@observe(name="step.vote_merge")
def vote_merge(email: str, drafts: list[str]) -> str:
    numbered = "\n\n".join(f"Draft {i}:\n{d}" for i, d in enumerate(drafts, start=1))
    return complete(VOTE_MERGE_SYSTEM, f"Original email:\n{email}\n\n{numbered}")


@observe(name="pattern.parallelization.voting")
def run_voting(email: str, n: int = 3) -> VoteResult:
    with propagate_attributes(
        tags=["backend:scratch", "pattern:parallelization"],
        metadata={"pattern": "parallelization", "mode": "voting", "backend": "scratch"},
    ):
        with ThreadPoolExecutor(max_workers=n) as pool:
            drafts = list(pool.map(lambda i: vote_draft(email, i), range(1, n + 1)))
        merged = vote_merge(email, drafts)
        return VoteResult(drafts=drafts, merged=merged)


def main() -> None:
    print("=== sectioning ===")
    print(run_sectioning(SUPPORT_EMAIL).model_dump_json(indent=2))
    print("\n=== voting ===")
    print(run_voting(SUPPORT_EMAIL).model_dump_json(indent=2))
    get_client().flush()


if __name__ == "__main__":
    main()
