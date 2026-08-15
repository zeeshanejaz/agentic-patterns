## 1. Shared prompts

- [x] 1.1 Add `PLAN_SYSTEM`, `PLAN_REPAIR_SYSTEM`, `PLAN_STEP_SYSTEM`, and `PLAN_REPLAN_SYSTEM` to `packages/shared/src/sd_agentic_shared/prompts.py`, interpolating `POLICY`

## 2. Scratch planning module

- [x] 2.1 Add `packages/patterns/src/sd_agentic_patterns/planning.py` that asks the model for a JSON plan, parses it (repair once, then fallback), and models `Plan` / `PlanStep` / `PlanningResult`
- [x] 2.2 Execute steps in dependency order: `call_tool` for tool steps, `complete` for text steps; checkpoint blocked results; replan remaining steps at most once
- [x] 2.3 Produce a policy-bound `reply`; tag traces `pattern:planning` and `backend:scratch`; run `SUPPORT_EMAIL` in `main`

## 3. README

- [x] 3.1 Flip planning scratch Progress cell to `done` (leave LangChain/MAF pending); refresh Done/Next; add the scratch planning Run command
