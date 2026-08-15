## Context

HITL pauses at high-risk / low-confidence / compliance points for a human to approve, edit, deny, or take over, then resumes. POLICY already forbids promising refunds over $50 without human approval. `SUPPORT_EMAIL` asks for an $89 refund — a natural gate. LangChain later uses `interrupt()`; scratch must show an explicit pause/resume callback.

## Goals / Non-Goals

**Goals:**

- Scratch module `human_in_the_loop` wrapping summarize → draft (prompt chaining), tags `pattern:human_in_the_loop`, `backend:scratch`.
- Gate: `needs_human` when refund over $50 is requested or the draft would promise one.
- Reviewer is a callback `reviewer(payload) -> HITLDecision` (approve / edit / deny). Default uses canned `HITL_DECISION` (deny the $89 refund).
- Resume writes the final reply from the decision. Print JSON: draft, gate, decision, reply, interrupted.
- README scratch cell done; Next points at HITL ports.

**Non-Goals:**

- LangChain `interrupt()` / checkpointers (ports).
- Real stdin/UI. Live humans. Changing fake tools.
- Exception retries (#12) or evaluation (#19).

## Decisions

1. **Wrap prompt chaining, not tool use.** Summarize + draft are enough to produce something a human can approve. Gate is the HITL surface.

2. **Canned reviewer in shared.** `HITL_DECISION = {action: "deny", note: "..."}` so `python -m` is non-interactive. `run(..., reviewer=)` stays injectable for later ports/tests.

3. **Always interrupt SUPPORT_EMAIL.** Gate prompt plus a deterministic override: if the email mentions a refund over $50, `needs_human` is true even if the model says otherwise.

4. **Deny by default** for the demo so the final reply does not promise $89.

## Risks / Trade-offs

- [Looks like policy check] → checker is PASS/FAIL; HITL is pause/resume with an external decision.
- [Blocking CLI] → canned decision, not stdin.

## Migration Plan

Add module + prompts + canned decision + README. Rollback is delete those.

## Open Questions

None.
