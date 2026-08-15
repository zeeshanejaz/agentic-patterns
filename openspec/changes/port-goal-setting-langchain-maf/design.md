## Context

Scratch goal-setting sets 3–5 KPIs, drafts, scores PASS/FAIL per goal, and revises while `MAX_ATTEMPTS = 3` remains. Shared SLA and prompts already exist. LangChain lab README: goal monitoring belongs in graph state (unknown iteration).

## Goals / Non-Goals

**Goals:**

- Same set/monitor/adjust semantics, same result shape, same module name `goal_setting`.
- LangGraph: nodes `set_goals`, `adjust`, `monitor`; loop until all PASS or budget exhausted.
- MAF: Agents for set / adjust / monitor inside the same loop as scratch.
- Tags `pattern:goal_setting` and `backend:langchain` / `backend:maf`.
- README cells and run commands.

**Non-Goals:**

- Changing scratch, prompts, or `SUPPORT_SLA`.
- Planning tools/DAGs, evaluation infra (#19), exception retries (#12).
- A Python `while` around LCEL for the LangChain port.

## Decisions

1. **Both labs in one change.** One progress-board loop, two modules.

2. **LangChain: LangGraph cycle.** State holds email, goals, reply, failed scores, attempts, attempt index. Conditional after monitor: `adjust` if failed and under budget, else END.

   Alternative: LCEL + Python for-loop — rejected; lab README forbids reinventing the cycle that way.

3. **MAF: Python for-loop of Agents.** Set, adjust, monitor are Agents. Parent span `pattern.goal_setting`.

4. **CLI runs `SUPPORT_EMAIL`**, same as scratch.

## Risks / Trade-offs

- [Looks like reflection graph] → state carries a goal list and per-goal scores, not a single critic string.
- [JSON fragility] → same fallbacks as scratch.

## Migration Plan

Add two modules and README lines. Rollback is delete + revert README.

## Open Questions

None.
