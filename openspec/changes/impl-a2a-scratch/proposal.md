## Why

Inter-agent communication / A2A (#15) is the next scratch pattern: RAG (#14) is implemented and ported. Multi-agent (#7) already shares a notes board; A2A must invent a message bus (ids, TTL, replies) so later ports can show graph topology.

## What Changes

- Add `sd_agentic_patterns.a2a`: a support inbox over a message bus. Coordinator, billing, and shipping exchange envelopes; stale messages drop; a writer replies from delivered mail.
- Reuse existing specialist prompts and `SUPPORT_EMAIL`. Add a small envelope/bus prompt if needed.
- Tag traces `pattern:a2a` and `backend:scratch`.
- Update README Progress (A2A scratch → shipped), Done/Next, and Run.

## Capabilities

### New Capabilities

- `a2a-scratch`: From-scratch A2A on the shared support-inbox task: envelopes on a bus, TTL, capped loop, writer reply.

### Modified Capabilities

- (none)

## Impact

- New module: `packages/patterns/src/sd_agentic_patterns/a2a.py`.
- Optional prompt in `packages/shared`.
- README. No LangChain/MAF this change. `packages/patterns` stays framework-free.
