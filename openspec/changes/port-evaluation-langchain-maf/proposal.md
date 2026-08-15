## Why

Evaluation (#19) exists from scratch but LangChain and MAF are pending. LCEL wrappers are the teaching surface; Langfuse remains tracing, not the eval loop.

## What Changes

- LangChain LCEL chains for summarize/draft/judge over `EVAL_CASES`. MAF Agents for the same steps. Tags `pattern:evaluation`. README shipped.

## Capabilities

### New Capabilities

- `evaluation-ports`: LangChain and MAF ports of golden/heuristic/judge evaluation.

### Modified Capabilities

- (none)

## Impact

- Two modules + README. Scratch unchanged.
