## Why

Exception handling and recovery (#12) is the next scratch pattern: goal setting (#11) is implemented and ported. Quality/safety patterns wrap an existing flow. Scratch must exist before ports so classify → retry → fallback → emergency-stop is invented here, not hidden by LCEL retries.

## What Changes

- Add `sd_agentic_patterns.exception_handling`: the tool-use support loop with a recovery wrapper around tool execution. Inject a couple of transient `lookup_order` timeouts so the demo is deterministic.
- Classify transient vs permanent vs critical. Retry transients with a capped backoff. Degrade to `search_docs` / a policy-safe fallback reply on permanent failure. Emergency-stop and record an alert on critical errors.
- Reuse shared `POLICY`, `SUPPORT_EMAIL`, and fake tools. Do not change `packages/shared` tool implementations. Add a small fallback prompt if needed.
- Tag traces `pattern:exception_handling` and `backend:scratch`.
- Update README Progress (exception-handling scratch → done; LangChain/MAF stay pending), Done/Next, and Run commands.

## Capabilities

### New Capabilities

- `exception-handling-scratch`: From-scratch exception handling wrapping the tool-use support loop: classify, retry, fallback, emergency-stop.

### Modified Capabilities

- (none)

## Impact

- New module: `packages/patterns/src/sd_agentic_patterns/exception_handling.py`.
- Optional fallback prompt in `packages/shared`.
- README Progress / Done / Next / Run.
- `packages/patterns` still must not import LangChain or MAF. No ports this change. Fake tool data stays unchanged.
