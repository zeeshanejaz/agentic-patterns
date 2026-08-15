## Why

Planning (#6) is the next scratch pattern: core-loop patterns 1–5 are already implemented and ported. Scratch must exist before LangChain/MAF ports so the loop (decompose → DAG → execute → replan) is invented here, not hidden by a framework.

## What Changes

- Add `sd_agentic_patterns.planning`: LLM emits a JSON plan (goal + steps with ids, tools/arguments, dependencies), execute ready steps, checkpoint, replan remaining work at most once if a tool step is blocked, then produce a policy-bound customer reply.
- Add shared planner/step prompts in `packages/shared` so later ports reuse the same strings.
- Use the existing fake tools (`lookup_order`, `create_refund`, `search_docs`) and `SUPPORT_EMAIL`. Do not invent order facts; do not promise refunds over $50.
- Tag traces `pattern:planning` and `backend:scratch`.
- Update README Progress (planning scratch → done; LangChain/MAF stay pending), Done/Next, and Run commands.

## Capabilities

### New Capabilities

- `planning-scratch`: From-scratch planning on the shared support-inbox task: decompose, execute a dependency graph with fake tools, replan on blockers, reply.

### Modified Capabilities

- (none)

## Impact

- New module: `packages/patterns/src/sd_agentic_patterns/planning.py`.
- New prompts in `packages/shared/src/sd_agentic_shared/prompts.py`.
- README Progress / Done / Next / Run.
- `packages/patterns` still must not import LangChain or MAF. No ports this change.
