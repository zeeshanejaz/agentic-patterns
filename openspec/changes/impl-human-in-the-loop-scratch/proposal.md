## Why

Human-in-the-loop (#13) is the next scratch pattern: exception handling (#12) is implemented and ported. Quality/safety patterns wrap an existing flow. Scratch must invent pause → human decision → resume before LangGraph `interrupt()`.

## What Changes

- Add `sd_agentic_patterns.human_in_the_loop`: wrap summarize → draft, gate on high-risk (refund over $50 / policy fail), pause for a reviewer callback, then resume (approve / edit / deny).
- Add shared gate/resume prompts and a canned `HITL_DECISION` so the CLI demo does not block on stdin.
- Do not invent order facts; do not promise refunds over $50 unless the human approved. Tag traces `pattern:human_in_the_loop` and `backend:scratch`.
- Update README Progress (HITL scratch → done; LangChain/MAF stay pending), Done/Next, and Run commands.

## Capabilities

### New Capabilities

- `human-in-the-loop-scratch`: From-scratch HITL wrapping the support draft flow: gate, pause for a reviewer, resume.

### Modified Capabilities

- (none)

## Impact

- New module: `packages/patterns/src/sd_agentic_patterns/human_in_the_loop.py`.
- New prompts and canned decision in `packages/shared`.
- README Progress / Done / Next / Run.
- `packages/patterns` still must not import LangChain or MAF. No ports this change.
