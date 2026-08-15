## Context

Route simple work to cheap/fast models and hard work to expensive ones. Scratch cannot swap real model SKUs easily; it can still **classify complexity** and run two different prompt budgets.

## Goals / Non-Goals

**Goals:** Module `resource_aware`. Classify `simple` vs `complex`. Simple → short FAQ-style reply. Complex → full POLICY draft. Print `route`, `cost_units` (chars/100), `reply`. Run `SAMPLE_EMAILS`. Tags `pattern:resource_aware`. README scratch shipped.

**Non-Goals:** Ports. Real model routing. Caching. Changing openai_model().

## Decisions

1. **Two system prompts, one model.** Teaching surface is the router, not vendor SKUs.
2. **Deterministic override:** mixed SUPPORT_EMAIL / refund-over-50 → complex.
3. **cost_units = ceil(output_chars / 100) + route fee** (1 cheap / 4 expensive).

## Risks / Trade-offs

- [Looks like routing #2] → billing/shipping intents vs compute budget.

## Migration Plan

Add module + prompts + README.

## Open Questions

None.
