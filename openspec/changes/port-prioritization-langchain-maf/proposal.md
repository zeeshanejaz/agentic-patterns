## Why

Prioritization (#20) exists from scratch but LangChain and MAF are pending. The re-score loop is a LangGraph cycle; MAF uses Agents plus the same queue.

## What Changes

- LangChain StateGraph: score → execute top → age leftover. MAF Agents for score/draft. Tags `pattern:prioritization`. README shipped.

## Capabilities

### New Capabilities

- `prioritization-ports`: LangChain and MAF ports of inbox scoring, execute-top, re-score.

### Modified Capabilities

- (none)

## Impact

- Two modules + README. Scratch unchanged.
