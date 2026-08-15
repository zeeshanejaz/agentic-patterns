## Context

The fake inbox has four tickets of unequal urgency (mixed chargeback vs a simple cancel). The pattern is a queue, not a single-email clone of prompt chaining.

## Goals / Non-Goals

**Goals:** Score `SAMPLE_EMAILS` (1–10 plus SLA). Heuristic floor for chargeback / refund over $50. Execute the top `MAX_EXECUTE=2` drafts. Age-bump and re-score leftover. Tags `pattern:prioritization`.

**Non-Goals:** Ports. Fair-share scheduling beyond a +1 age bump. Multi-agent assignment.

## Decisions

1. LLM score plus heuristic floor so mixed always outranks a calm shipping-only ticket.
2. Execute with `DRAFT_SYSTEM` after a short summarize so replies stay on-policy.
3. After each execute, remaining scores += 1 (cap 10) then re-sort.

## Risks / Trade-offs

- [Looks like routing] → routing classifies one email; this ranks a queue and reorders.
- [Starvation] → age bump on leftover is the teaching counter.

## Migration Plan

Add module + prompt + README.

## Open Questions

None.
