## Why

Reasoning (#17) exists from scratch (CoT samples + pick) but LangChain and MAF are pending. Self-consistency is a graph loop.

## What Changes

- LangGraph sample loop (`N_SAMPLES = 2`) then pick. MAF Agents for each sample. Same `REASONING_SYSTEM` and result shape. Tags `pattern:reasoning`. README shipped.

## Capabilities

### New Capabilities

- `reasoning-ports`: LangChain and MAF ports of CoT self-consistency on the support inbox.

### Modified Capabilities

- (none)

## Impact

- Two modules + README. Scratch unchanged.
