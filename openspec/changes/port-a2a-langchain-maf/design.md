## Context

Scratch A2A posts coordinator → billing/shipping envelopes, specialists reply on the bus, coordinator forwards to writer. TTL drops stale mail. `MAX_MESSAGES = 8`.

## Goals / Non-Goals

**Goals:** Same bus semantics and result shape. LangGraph encodes topology. MAF Agents write notes/reply. Tags `pattern:a2a`. README shipped.

**Non-Goals:** Changing scratch. Real network. Peer mesh.

## Decisions

1. Both labs in one change.
2. LangChain: StateGraph nodes `dispatch`, `specialists`, `forward`, `write`. Bus list lives in state.
3. MAF: Python bus + Agents (same control flow as scratch).
4. `K`/`MAX_MESSAGES = 8`.

## Risks / Trade-offs

- [Looks like multi-agent graph] → state is envelopes with ttl, not notes.

## Migration Plan

Add two modules + README.

## Open Questions

None.
