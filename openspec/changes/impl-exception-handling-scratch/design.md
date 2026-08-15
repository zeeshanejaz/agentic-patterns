## Context

The pattern catches failures, classifies temporary vs permanent, retries with capped backoff, degrades to fallbacks, and emergency-stops plus alerts on critical errors. Tool use (#5) already calls `lookup_order` / `create_refund` / `search_docs`. Those fakes never raise, so this lab **wraps** execute with injected faults rather than cloning a new inbox task.

## Goals / Non-Goals

**Goals:**

- Scratch module `exception_handling` wrapping the tool-use loop, tags `pattern:exception_handling`, `backend:scratch`.
- Inject the first two `lookup_order` calls as transient timeouts so retries are visible without a live flaky API.
- Classify: transient (timeout, rate_limit) → retry up to `MAX_RETRIES = 2`; permanent → fallback `search_docs` or a POLICY-safe reply; critical → stop and record an alert.
- Print JSON with recovery `events`, successful `calls`, `reply`, and `stopped`.
- README scratch cell done; Next points at exception-handling ports.

**Non-Goals:**

- LangChain / MAF ports (LCEL retry/fallback later).
- Changing `tools.py` / order fixtures.
- HITL (#13), guardrails (#18), evaluation infra (#19).
- Real `time.sleep` delays long enough to stall the CLI (`BACKOFF_SECONDS = 0`; log the intended backoff).

## Decisions

1. **Wrap tool use, don't invent a new task.** Same `SUPPORT_EMAIL` and `OPENAI_TOOLS`. Recovery lives in `execute_with_recovery`.

2. **Injected timeouts on lookup_order.** A counter `LOOKUP_TIMEOUTS = 2` raises `TransientError` before the real fake. After that, `call_tool` runs. Unknown tools are `PermanentError`. A tool named `emergency_stop` (if the model ever calls it) is unused; critical is raised only if recovery itself exceeds a safety cap (`MAX_EVENTS = 12`) to avoid retry storms.

   Simpler critical path: if the same tool fails transiently `MAX_RETRIES + 1` times, escalate to fallback (permanent), not critical. Critical = uncaught / `CriticalError` from a poison injection we don't need for v1.

   Revised: skip a dedicated critical injector. **Critical** = more than `MAX_EVENTS` recovery actions in one run → emergency-stop. That's the cascade guard.

3. **Backoff is recorded, not slept.** `BACKOFF_SECONDS = 0`.

4. **Fallback** for a permanently failed `lookup_order`: call `search_docs` once with query `shipping`. If that also fails, write a POLICY-safe "could not look up the order" reply via `EXCEPTION_FALLBACK_SYSTEM` and stop the tool loop.

## Risks / Trade-offs

- [Looks like tool use] → the teaching surface is the recovery log (`events`), not the tool list.
- [LLM may not call lookup_order] → SUPPORT_EMAIL mentions order ids; same prompt as tool use. If no lookup, events may be empty; still a valid run.
- [Retry storms] → `MAX_RETRIES` per call and `MAX_EVENTS` per run.

## Migration Plan

Add module + optional prompt + README. Rollback is delete those.

## Open Questions

None.
