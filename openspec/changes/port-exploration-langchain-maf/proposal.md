## Why

Exploration (#21) exists from scratch but LangChain and MAF are pending. Branch/score/prune is a LangGraph cycle; MAF uses Agents.

## What Changes

- LangChain StateGraph expand → score → prune/pick. MAF Agents for the same steps. Tags `pattern:exploration`. README shipped; 21-pattern table complete.

## Capabilities

### New Capabilities

- `exploration-ports`: LangChain and MAF ports of branch/score/prune exploration.

### Modified Capabilities

- (none)

## Impact

- Two modules + README. Scratch unchanged. Progress table should have no pending cells.
