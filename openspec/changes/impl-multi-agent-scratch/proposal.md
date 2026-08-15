## Why

Multi-agent collaboration (#7) is the next scratch pattern: core-loop patterns 1–6 are implemented and ported. Scratch must exist before LangChain/MAF ports so the loop (coordinator → specialists → shared notes → writer) is invented here, not hidden by a framework supervisor.

## What Changes

- Add `sd_agentic_patterns.multi_agent`: a coordinator assigns billing / shipping / policy specialists, they write notes onto a shared board, the coordinator may dispatch one extra round, then a writer produces a policy-bound customer reply.
- Add shared coordinator / specialist / writer prompts in `packages/shared` so later ports reuse the same strings.
- Use `SUPPORT_EMAIL`. Do not invent order facts; do not promise refunds over $50. Specialists write team notes, not customer emails.
- Tag traces `pattern:multi_agent` and `backend:scratch`.
- Update README Progress (multi-agent scratch → done; LangChain/MAF stay pending), Done/Next, and Run commands.

## Capabilities

### New Capabilities

- `multi-agent-scratch`: From-scratch multi-agent collaboration on the shared support-inbox task: coordinator, named specialists, shared notes, writer.

### Modified Capabilities

- (none)

## Impact

- New module: `packages/patterns/src/sd_agentic_patterns/multi_agent.py`.
- New prompts in `packages/shared/src/sd_agentic_shared/prompts.py`.
- README Progress / Done / Next / Run.
- `packages/patterns` still must not import LangChain or MAF. No ports this change.
