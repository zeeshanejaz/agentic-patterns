## Context

The planning diagram is: goal → milestones/DAG → constraint check → assign tool per step → execute with checkpoints → replan or escalate on blockers → acceptance. The shared task is still the fake support inbox. Tool use already has an open-ended function-calling loop; planning should **write a plan first**, then execute it.

## Goals / Non-Goals

**Goals:**

- Scratch module `planning` with Langfuse tags `pattern:planning`, `backend:scratch`.
- Structured plan (JSON) with step ids, optional tool + arguments, `depends_on`.
- Execute in dependency order using `call_tool` for tool steps and `complete()` for text steps.
- One replan of remaining steps when a checkpoint is blocked (order missing or refund refused).
- Shared prompts for planner, step execution, and replan.
- README scratch cell done; Next points at planning ports or multi-agent scratch.

**Non-Goals:**

- LangChain / MAF ports.
- Human escalation UI (HITL is #13); blocked refunds stay in the execution log and the reply.
- Changing existing fake tool data.
- Full project-management software (no budgets/SLAs beyond POLICY).

## Decisions

1. **Plan JSON then execute**, not ReAct. Distinguishes this pattern from tool use.

2. **Planner fills `arguments`** so the executor does not guess order ids. If JSON parse fails, one repair `complete()` then a tiny fallback plan: `search_docs` then a text reply.

3. **Blocked checkpoint** = tool result starts with `No order found` or `REFUSED`. Then replan leftover steps once (`MAX_REPLANS = 1`) with the log as context.

4. **Reply** is the last text step if present, else a final `complete()` over the execution log with POLICY.

5. **Topological order**; if the DAG is cyclic, fall back to listed order.

## Risks / Trade-offs

- [Planner invents order ids] → prompt forbids it; tools return `No order found` and trigger replan.
- [JSON fragility] → repair pass + fallback plan.
- [Overlap with tool use] → plan-first DAG is the teaching difference.

## Migration Plan

Add module + prompts + README. Rollback is delete those.

## Open Questions

None.
