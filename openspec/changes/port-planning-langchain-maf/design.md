## Context

Scratch planning writes a JSON DAG first, executes ready steps (shared `call_tool` or an LLM text step), and replans leftover steps once if a checkpoint is blocked (`No order found` / `REFUSED`). Shared prompts already exist. Tool use is a ReAct loop; this port must stay plan-first so the three backends remain comparable.

## Goals / Non-Goals

**Goals:**

- Same DAG, same `MAX_REPLANS = 1`, same result shape (`plan`, `execution`, `replans`, `reply`), same module name `planning`.
- LangGraph encodes the outer plan → execute-step → optional replan cycle.
- MAF uses Agent.run for planner / repair / step / replan inside the same control flow as scratch.
- Tool steps still call `sd_agentic_shared.tools.call_tool` (plan-specified, not a bound-tool ReAct loop).
- Tags `pattern:planning` and `backend:langchain` / `backend:maf`.
- README cells and run commands.

**Non-Goals:**

- Changing scratch or shared prompts.
- Binding tools onto a LangGraph `ToolNode` / MAF Agent (that is tool use).
- HITL escalation UI. MagenticBuilder / multi-agent planners.
- MCP.

## Decisions

1. **Both labs in one change.** One DAG loop, two small modules. Same as reflection and tool-use ports.

2. **LangChain: LangGraph cycle over dynamic steps.** Nodes: `plan`, `execute`, `replan`, `reply`. State holds `email`, parsed `plan`, remaining `queue`, `execution` results, `replans`, and `reply`. After `execute`, go to `replan` if the last step is blocked, leftover steps remain, and `replans < MAX_REPLANS`; else `execute` again if the queue is non-empty; else `reply`. JSON parse / repair / fallback stay in Python helpers copied from scratch (the graph is the teaching surface, not JSON parsing).

   Alternative: Python while-loop calling LCEL chains — rejected; would not show LangGraph cycles, unlike reflection.

3. **MAF: Python while-loop of Agents.** SequentialBuilder cannot branch on blocked checkpoints. Planner / repair / step / replan are Agents with the shared system prompts. Tool steps still use `call_tool`. Parent span `pattern.planning` with `pattern` / `backend` attributes.

4. **CLI runs `SUPPORT_EMAIL` once**, same as scratch.

## Risks / Trade-offs

- [Planner invents order ids] → same prompts and blocked-checkpoint replan as scratch.
- [JSON fragility] → repair pass + fallback plan, copied from scratch.
- [Overlap with tool use] → plan-specified `call_tool`, not bound-tool ReAct.

## Migration Plan

Add two modules and README lines. Rollback is delete + revert README.

## Open Questions

None.
