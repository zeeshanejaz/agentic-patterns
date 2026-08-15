## ADDED Requirements

### Requirement: Scratch exception-handling module
The patterns package SHALL expose `sd_agentic_patterns.exception_handling` that wraps the tool-use support loop with classify / retry / fallback / emergency-stop recovery, without importing LangChain or Microsoft Agent Framework.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-patterns python -m sd_agentic_patterns.exception_handling`
- **THEN** the process SHALL print JSON that includes recovery `events`, tool `calls`, a `reply`, and `stopped`

#### Scenario: Transient retry
- **WHEN** a tool raises a transient error (timeout or rate limit)
- **THEN** the module MUST retry that call up to `MAX_RETRIES` times and MUST record each attempt in `events`

#### Scenario: Injected lookup timeouts
- **WHEN** `lookup_order` is invoked
- **THEN** the first two invocations MUST fail as transient timeouts before the real fake tool runs, so the demo shows retries

#### Scenario: Permanent fallback
- **WHEN** a tool failure is permanent or retries are exhausted
- **THEN** the module MUST degrade (call `search_docs` or produce a POLICY-safe fallback reply) rather than crash

#### Scenario: Emergency stop
- **WHEN** recovery events exceed `MAX_EVENTS`
- **THEN** the module MUST stop the tool loop, set `stopped` true, and record an alert event

#### Scenario: Policy
- **WHEN** a reply is written
- **THEN** it MUST be produced under the shared support `POLICY` (no invented order facts, no refunds over $50 without human approval, no blaming the customer)

#### Scenario: Langfuse tags
- **WHEN** `run` executes
- **THEN** the Langfuse trace MUST include tags `pattern:exception_handling` and `backend:scratch`

### Requirement: Shared fallback prompt
A fallback reply prompt SHALL live in `packages/shared` so later ports can reuse it.

#### Scenario: Prompt is importable
- **WHEN** a lab imports `EXCEPTION_FALLBACK_SYSTEM` from `sd_agentic_shared.prompts`
- **THEN** it MUST be defined and interpolate `POLICY`

### Requirement: README progress for exception-handling scratch
The repository README SHALL record that exception-handling scratch is done and SHALL document a run command for the module. LangChain and MAF exception-handling cells SHALL remain pending.

#### Scenario: Progress cells
- **WHEN** this change lands
- **THEN** the Progress table row for pattern 12 Exception handling and recovery SHALL show scratch as `done` and LangChain and MAF as `pending`

#### Scenario: Run section
- **WHEN** a developer reads the README Run section
- **THEN** they SHALL find `uv run --package sd-agentic-patterns python -m sd_agentic_patterns.exception_handling`
