## Context

Check inputs (injection/harm) and outputs (policy, refunds, invented tracking). Wrap prompt-chaining draft. Deterministic output fail if reply promises a refund over $50.

## Goals / Non-Goals

**Goals:** Module `guardrails`. Input scan + draft + output scan. On fail, rewrite. Print `input_ok`, `output_ok`, `violations`, `reply`. Tags `pattern:guardrails`.

**Non-Goals:** Ports. Full moderation APIs.

## Decisions

1. Wrap summarize+draft.
2. Heuristic output: refund over $50 in the reply → fail even if the model says PASS.
3. Shared `GUARDRAIL_INPUT_SYSTEM` / `GUARDRAIL_OUTPUT_SYSTEM`.

## Risks / Trade-offs

- [Looks like policy check] → input scan + rewrite loop is the extra surface.

## Migration Plan

Add module + prompts + README.

## Open Questions

None.
