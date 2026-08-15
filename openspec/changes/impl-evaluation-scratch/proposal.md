## Why

Evaluation and monitoring (#19) is next. Quality/safety wraps an existing draft flow: golden cases, heuristic gates, and an LLM judge — not a fourth clone of every backend.

## What Changes

- Add `sd_agentic_patterns.evaluation` wrapping summarize/draft over a small golden inbox. Heuristics plus `EVAL_JUDGE_SYSTEM`. Tags `pattern:evaluation`. README scratch shipped.

## Capabilities

### New Capabilities

- `evaluation-scratch`: From-scratch golden/heuristic/judge wrap around a support draft.

### Modified Capabilities

- (none)

## Impact

- New module, judge prompt, golden cases, README. No ports.
