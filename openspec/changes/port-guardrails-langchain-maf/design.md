## Context

Scratch scans input, drafts, scans output, rewrites on fail. Heuristic fails refunds over $50. LangChain README: guardrail wrappers may stay LCEL.

## Goals / Non-Goals

**Goals:** LCEL not StateGraph. MAF Agents. Same result shape. README shipped.

**Non-Goals:** Changing scratch. Moderation vendors.

## Decisions

1. Both labs one change.
2. LangChain: LCEL prompt | llm | parser for each step.
3. MAF: Agents for input, summarize, draft, output, rewrite.

## Risks / Trade-offs

- [Looks like prompt chaining] → extra input/output JSON guards.

## Migration Plan

Add modules + README.

## Open Questions

None.
