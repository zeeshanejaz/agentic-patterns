## Context

Scratch wraps summarize/draft, scores `EVAL_CASES` with heuristics plus an LLM judge. LangChain README: evaluation is not a graph; LCEL wrappers/parsers are enough.

## Goals / Non-Goals

**Goals:** LCEL not StateGraph. MAF Agents. Same `EvalReport` shape. README shipped.

**Non-Goals:** Changing scratch. Langfuse experiment datasets.

## Decisions

1. Both labs one change.
2. LangChain: LCEL prompt | llm | parser per step.
3. MAF: Agents for summarize, draft, judge.
4. Reuse shared heuristics (refund > $50, must_mention, blame markers).

## Risks / Trade-offs

- [Looks like prompt chaining] → extra judge + golden pass_rate, no revise.

## Migration Plan

Add modules + README.

## Open Questions

None.
