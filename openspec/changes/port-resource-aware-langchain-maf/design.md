## Context

Scratch classifies simple/complex (refund-over-50 forces complex) then cheap vs expensive prompts. LangChain README: resource-aware router chain is enough.

## Goals / Non-Goals

**Goals:** LCEL branch; MAF Agents; same result shape; README shipped.

**Non-Goals:** Real model SKUs. Graph. Changing scratch.

## Decisions

1. Both labs one change.
2. LangChain: classify chain then `RunnableBranch`.
3. MAF: three Agents.
4. Same cost_units formula.

## Risks / Trade-offs

- [Looks like routing] → route values are simple/complex budgets, not billing/shipping.

## Migration Plan

Add modules + README.

## Open Questions

None.
