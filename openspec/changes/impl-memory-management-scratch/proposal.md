## Why

Memory management (#8) is the next scratch pattern: patterns 1–7 are implemented and ported. Scratch must exist before LangChain/MAF ports so the loop (classify → store → retrieve within a token budget) is invented here, not hidden by a framework checkpointer.

## What Changes

- Add `sd_agentic_patterns.memory_management`: a three-tier in-memory store (short-term, episodic, long-term) over a multi-turn support thread. Each turn retrieves relevant memory, replies under POLICY, then extracts new memories and compact if over budget.
- Add a small `MEMORY_THREAD` of follow-up emails in `packages/shared` plus extract/retrieve/reply prompts so later ports reuse them.
- Do not invent order facts; do not promise refunds over $50. Memory is in-process (no database).
- Tag traces `pattern:memory_management` and `backend:scratch`.
- Update README Progress (memory scratch → done; LangChain/MAF stay pending), Done/Next, and Run commands.

## Capabilities

### New Capabilities

- `memory-management-scratch`: From-scratch memory management on the shared support-inbox task: three-tier store, retrieve-then-reply, compact on budget.

### Modified Capabilities

- (none)

## Impact

- New module: `packages/patterns/src/sd_agentic_patterns/memory_management.py`.
- New prompts and `MEMORY_THREAD` in `packages/shared`.
- README Progress / Done / Next / Run.
- `packages/patterns` still must not import LangChain or MAF. No ports this change.
