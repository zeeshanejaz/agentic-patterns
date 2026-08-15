## Context

Not voting (pattern 3) and not CoT samples (pattern 17): each branch is a *different strategy*, then a scorer prunes. Shared task stays the mixed support email.

## Goals / Non-Goals

**Goals:** Expand three named angles, draft each, score 1–10, prune below `KEEP_THRESHOLD` or refund-over-$50, pick the highest kept (fallback: highest scored). Tags `pattern:exploration`.

**Non-Goals:** Ports. Open-ended web search. Unbounded trees.

## Decisions

1. Fixed `EXPLORE_ANGLES` in shared so ports match.
2. Heuristic prune for refund > $50 even if the judge likes the draft.
3. No rewrite after pick — exploration ends at selection.

## Risks / Trade-offs

- [Looks like voting] → angles are distinct strategies, not N samples of the same prompt.
- [Looks like reasoning] → no CoT JSON; branch/score/prune is the loop.

## Migration Plan

Add module + prompts + README.

## Open Questions

None.
