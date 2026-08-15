## Context

Scratch multi-agent is a coordinator that assigns `billing` / `shipping` / `policy` specialists onto a shared notes board, may review once more (`MAX_ROUNDS = 2`), then a writer replies. Shared prompts already exist. Routing is one handler; parallelization has no coordinator. This port must stay coordinator-worker.

## Goals / Non-Goals

**Goals:**

- Same roster, same `MAX_ROUNDS`, same result shape, same module name `multi_agent`.
- LangGraph encodes the outer coordinate → specialists → optional review → write cycle.
- MAF uses Agent.run for coordinator / specialists / writer inside the same control flow as scratch.
- Tags `pattern:multi_agent` and `backend:langchain` / `backend:maf`.
- README cells and run commands.

**Non-Goals:**

- Changing scratch or shared prompts.
- A2A peer mesh. Tool-bound specialists. MagenticBuilder.
- MCP / OO-Agents.

## Decisions

1. **Both labs in one change.** One supervisor loop, two small modules.

2. **LangChain: LangGraph cycle.** Nodes: `coordinate`, `specialists`, `review`, `write`. State holds `email`, `pending` assignments, accumulated `assignments` / `notes`, `rounds`, `reply`. After `specialists`, go to `review` if `rounds < MAX_ROUNDS`, else `write`. After `review`, go to `specialists` if pending remains, else `write`. JSON parse / fallback stay in Python helpers copied from scratch.

   Alternative: Python while-loop calling LCEL — rejected; would not show LangGraph cycles.

3. **MAF: Python while-loop of Agents.** SequentialBuilder cannot branch on DONE. Coordinator / review / billing / shipping / policy / writer are Agents with the shared system prompts. Parent span `pattern.multi_agent` with `pattern` / `backend` attributes.

4. **CLI runs `SUPPORT_EMAIL` once**, same as scratch.

## Risks / Trade-offs

- [Looks like routing] → same multi-assignment + writer as scratch.
- [JSON fragility] → fallback assigns all three, copied from scratch.

## Migration Plan

Add two modules and README lines. Rollback is delete + revert README.

## Open Questions

None.
