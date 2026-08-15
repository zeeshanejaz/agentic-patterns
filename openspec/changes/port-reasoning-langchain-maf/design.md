## Context

Scratch runs two CoT JSON samples and keeps the first reply. LangChain README: CoT is a prompt; self-consistency loops prefer a graph.

## Goals / Non-Goals

**Goals:** LangGraph sample cycle; MAF Agents; same shape; README shipped.

**Non-Goals:** ToT branching. Changing scratch.

## Decisions

1. Both labs one change.
2. LangGraph: `sample` node until `len(samples) >= 2`.
3. MAF: two Agent runs.

## Risks / Trade-offs

- [JSON fragility] → same fallback as scratch.

## Migration Plan

Add modules + README.

## Open Questions

None.
