## Context

Scratch reflection summarizes the email, drafts a reply, then loops critic → optional revise up to three times. PASS is `critique.strip().upper().startswith("PASS")`. Shared prompts already exist.

## Goals / Non-Goals

**Goals:**

- Same loop, same `MAX_ROUNDS`, same result shape, same module name `reflection`.
- LangGraph encodes the cycle with conditional edges.
- MAF uses Agent.run for each step inside the same control flow as scratch.
- Tags `pattern:reflection` and `backend:langchain` / `backend:maf`.
- README cells and run commands.

**Non-Goals:**

- Changing scratch. MagenticBuilder / group-chat reflection. New prompts. MCP.

## Decisions

1. **Both labs in one change.** One loop, two small modules.

2. **LangChain: conditional cycle.** Nodes: summarize, draft, critic, revise. After critic, go to END if passed or `round_index >= MAX_ROUNDS`, else revise → critic. Critic appends `{draft, critique}` to `rounds` and sets `final` to the current draft.

   Alternative: Python for-loop calling LCEL chains — rejected; would not show LangGraph cycles.

3. **MAF: Python for-loop of Agents.** SequentialBuilder cannot branch on PASS. Do not fake a workflow cycle. Parent span `pattern.reflection` with `pattern`/`backend` attributes.

4. **CLI runs `SUPPORT_EMAIL` once**, same as scratch.

## Risks / Trade-offs

- [Infinite revise] → hard stop at `MAX_ROUNDS`.
- [PASS false positives] → same startswith rule as scratch.

## Migration Plan

Add two modules and README lines. Rollback is delete + revert README.

## Open Questions

None.
