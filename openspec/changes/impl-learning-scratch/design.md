## Context

The pattern collects corrections, ratings, and outcomes; cleans noise; updates prompts, policies, or examples (rarely weights); then A/B tests whether the change helped. Memory (#8) stores facts about *this* customer. Learning updates the *agent's* behavior so future tickets of the same kind improve. Existing labs have no feedback loop.

## Goals / Non-Goals

**Goals:**

- Scratch module `learning` with Langfuse tags `pattern:learning`, `backend:scratch`.
- Baseline replies on a shared batch, ingest simulated supervisor ratings/corrections, distill a compact lessons block into the reply prompt, re-run including a held-out email, print baseline vs adapted.
- Drop feedback that would violate POLICY (poison / learn the wrong lesson).
- Shared learning cases and distill/reply prompts in `packages/shared`.
- README scratch cell done; Next points at learning ports.

**Non-Goals:**

- LangChain / MAF ports.
- Fine-tuning or weight updates.
- Vector DB / embeddings (RAG is #14). Memory store (#8).
- Real persistence, live CSAT, or human review UI (HITL is #13).
- Changing existing fake tool data.

## Decisions

1. **Prompt lessons, not weights.** Distill feedback into a short "learned lessons" string injected into the reply system prompt. Teaching surface is collect → clean → update → compare.

2. **Simulated supervisor feedback, not LLM-invented outcomes.** Shared `LEARNING_CASES` are `{email, rating, correction}` plus `LEARNING_HELD_OUT`. Ratings and corrections are authored so the demo is deterministic about *what* was learned.

3. **Clean noise before distill.** Drop cases with empty correction, rating below a floor (`MIN_RATING = 1` on a 1–5 scale means keep 2+), or correction that asks to invent facts / promise a refund over $50 / blame the customer.

4. **A/B is two `complete()` passes on the held-out email:** baseline (POLICY only) vs adapted (POLICY + lessons). Print both replies plus the lessons block. No automated scorer this change (evaluation is #19).

5. **Module name `learning`.** Matches the short slug used in change names (`impl-learning-scratch`); traces use `pattern:learning`.

## Risks / Trade-offs

- [Looks like memory] → lessons are agent-wide rules/examples, not customer facts; held-out email is a new ticket, not a follow-up turn.
- [Poisoned feedback] → drop POLICY-violating corrections before distill.
- [Lessons too long] → distill prompt caps the block (few bullets); no unbounded concatenation of raw corrections.
- [A/B is qualitative] → demo prints both replies; scoring waits for #19.

## Migration Plan

Add module + prompts + cases + README. Rollback is delete those.

## Open Questions

None.
