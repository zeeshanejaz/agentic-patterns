## Context

Scratch HITL wraps summarize → draft, gates on refunds over $50, pauses via a reviewer callback, resumes with approve/edit/deny. Canned `HITL_DECISION` is deny. LangChain README: HITL cannot pause a chain well; `interrupt()` is the feature.

## Goals / Non-Goals

**Goals:**

- Same gate/resume semantics, same result shape, same module name `human_in_the_loop`.
- LangGraph: MemorySaver checkpointer, `interrupt()` in a human node, second `invoke` with `Command(resume=...)` using canned decision (CLI stays non-interactive).
- MAF: Agents for LLM steps; Python callback pause like scratch.
- Tags `pattern:human_in_the_loop` and `backend:langchain` / `backend:maf`.
- README cells and run commands.

**Non-Goals:**

- Changing scratch or `HITL_DECISION`.
- A real web UI or stdin prompt.
- Live human reviewers.

## Decisions

1. **Both labs in one change.**

2. **LangChain: `interrupt()` + checkpointer.** Nodes: summarize, draft, gate, human (interrupt), resume. Skip human node if `needs_human` is false. Demo resumes immediately with `HITL_DECISION` so `python -m` still exits.

   Alternative: Python `if` calling the canned decision inside a node — rejected; that hides `interrupt()`.

3. **MAF: callback, not a fake interrupt.** MAF has no LangGraph-style interrupt in this lab; copy scratch control flow with Agents.

4. **Deterministic gate override** (refund over $50) copied from scratch.

## Risks / Trade-offs

- [interrupt API churn] → use `langgraph.types.interrupt` and `Command(resume=)` as in current LangGraph.
- [Looks like prompt chaining] → the extra human node and two-phase invoke are the pattern.

## Migration Plan

Add two modules and README lines. Rollback is delete + revert README.

## Open Questions

None.
