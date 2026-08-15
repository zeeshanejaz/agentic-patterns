## Context

Scratch expands EXPLORE_ANGLES, scores, prunes refund-over-$50 and low scores, picks the best kept. LangChain README: exploration wants a graph (branch, score, prune).

## Goals / Non-Goals

**Goals:** LangGraph cycles for expand and score. MAF Agents. Same ExploreResult. README: pattern 21 fully shipped; no pending 21-pattern cells.

**Non-Goals:** Changing scratch. Send/fan-out required if a sequential expand/score graph already shows the pattern.

## Decisions

1. Both labs one change.
2. LangChain: StateGraph expand ⇄ score ⇄ prune, not a Python while around LCEL only.
3. MAF: Agents for branch and score.

## Risks / Trade-offs

- [Looks like voting] → named angles, prune, pick one survivor.

## Migration Plan

Add modules + README.

## Open Questions

None.
