## Why

Guardrails (#18) exists from scratch but LangChain and MAF are pending. LCEL wrappers are the teaching surface.

## What Changes

- LangChain LCEL chains for input/output scans around summarize/draft, rewrite on fail. MAF Agents for the same steps. Tags `pattern:guardrails`. README shipped.

## Capabilities

### New Capabilities

- `guardrails-ports`: LangChain and MAF ports of input/output guards around a support draft.

### Modified Capabilities

- (none)

## Impact

- Two modules + README. Scratch unchanged.
