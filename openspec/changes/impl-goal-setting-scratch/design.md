## Context

The pattern defines measurable goals (deadlines, budgets, KPIs), runs quality gates, compares progress to targets, and adjusts when the system drifts. Planning (#6) builds a tool DAG. Reflection (#4) is one critic PASS/FAIL. Evaluation (#19) is production golden tests. This lab is a **progress board** on the fake support inbox.

## Goals / Non-Goals

**Goals:**

- Scratch module `goal_setting` with Langfuse tags `pattern:goal_setting`, `backend:scratch`.
- Set 3–5 measurable goals from a shared support SLA + `SUPPORT_EMAIL`.
- Each attempt: draft/revise → monitor JSON scores → if any FAIL and attempts remain, adjust toward failed goals.
- Stop on all PASS or when `MAX_ATTEMPTS = 3` is exhausted; print goals, per-attempt scores, final reply, and whether targets were met.
- README scratch cell done; Next points at goal-setting ports.

**Non-Goals:**

- LangChain / MAF ports.
- Planning DAGs, tool calls, or replanning (#6).
- Production metrics / golden tests (#19). Exception retries (#12). HITL (#13).
- Changing fake tool data.

## Decisions

1. **Named KPIs, not a single critic.** Monitor returns `{id, status: PASS|FAIL, reason}` per goal so the board is the teaching surface.

2. **Shared SLA, LLM sets instance goals.** `SUPPORT_SLA` lists standing targets (cover every ask, stay in POLICY, acknowledge ids from the email, no invented tracking). A set-goals `complete()` turns that plus the email into 3–5 concrete goals. Fallback: three canned goals if JSON parse fails.

3. **Budget is `MAX_ATTEMPTS = 3`.** Attempt 1 drafts; later attempts revise using failed-goal reasons. No extra LLM calls beyond set + (draft|revise) + monitor per attempt.

4. **Heuristic policy gate stays in the monitor prompt** (POLICY interpolated). Do not add a separate reflection critic.

5. **Module name `goal_setting`.** Traces use `pattern:goal_setting`.

## Risks / Trade-offs

- [Looks like reflection] → multiple named goals + attempt budget + explicit scores, not one PASS/FAIL critic.
- [Looks like planning] → no tools/DAG; the plan is "meet these KPIs".
- [JSON fragility] → canned fallback goals; a failed monitor parse counts as FAIL for all open goals so the loop can still adjust.

## Migration Plan

Add module + prompts + README. Rollback is delete those.

## Open Questions

None.
