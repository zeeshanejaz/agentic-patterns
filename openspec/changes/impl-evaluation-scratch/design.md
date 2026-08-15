## Context

Langfuse is tracing, not the eval loop. The pattern is quality gates before you would ship a draft: known tickets, deterministic policy checks, then a judge score. Wrap summarize → draft; do not reimplement tool use.

## Goals / Non-Goals

**Goals:** Run `EVAL_CASES` (the four `SAMPLE_EMAILS`). Heuristics fail refunds over $50, missing required order ids, and blame language. LLM judge returns `{pass, score, reason}`. Report `pass_rate`. Tags `pattern:evaluation`.

**Non-Goals:** Ports. Langfuse datasets/experiments UI. Production alerting. Wrapping every other pattern.

## Decisions

1. Wrap prompt-chaining's summarize/draft; skip the policy-check step so the judge is the quality gate.
2. Golden cases live in `packages/shared` so ports reuse them.
3. Aggregate JSON: per-case heuristic + judge + `overall_pass`, plus `pass_rate`.

## Risks / Trade-offs

- [Judge disagrees with heuristics] → overall_pass requires both.
- [Looks like reflection] → no revise loop; this is score-and-report only.

## Migration Plan

Add module + prompts + cases + README.

## Open Questions

None.
