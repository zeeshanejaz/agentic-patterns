## Context

Scratch scores SAMPLE_EMAILS, drafts MAX_EXECUTE=2, age-bumps leftover. LangChain README: a Python queue is possible; prefer a graph for the re-score cycle.

## Goals / Non-Goals

**Goals:** LangGraph cycle, not a Python while around LCEL. MAF Agents. Same result shape. README shipped.

**Non-Goals:** Changing scratch.

## Decisions

1. Both labs one change.
2. LangChain: StateGraph score_all → execute → age → conditional.
3. MAF: Agents for score, summarize, draft; queue loop in Python (no MAF workflow type for this).

## Risks / Trade-offs

- [Looks like routing] → queue + re-rank, not one-email classify.

## Migration Plan

Add modules + README.

## Open Questions

None.
