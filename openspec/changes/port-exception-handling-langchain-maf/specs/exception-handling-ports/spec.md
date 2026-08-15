## ADDED Requirements

### Requirement: LangChain exception-handling module
The langchain-lab package SHALL expose `sd_agentic_langchain.exception_handling` that wraps the LangGraph tool-use loop with classify / retry / fallback / emergency-stop recovery.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-langchain python -m sd_agentic_langchain.exception_handling`
- **THEN** the process SHALL print JSON that includes recovery `events`, tool `calls`, a `reply`, and `stopped`

#### Scenario: Graph owns the agent loop
- **WHEN** the module runs
- **THEN** it MUST use a LangGraph agent ⇄ tools cycle (not a Python `while` around LCEL only) and MUST run tools through Recovery

#### Scenario: Injected lookup timeouts
- **WHEN** `lookup_order` is invoked
- **THEN** the first two invocations MUST fail as transient timeouts before the real fake tool runs

#### Scenario: Shared prompts
- **WHEN** the module writes a fallback reply
- **THEN** it MUST use `EXCEPTION_FALLBACK_SYSTEM` from shared prompts

#### Scenario: Langfuse tags
- **WHEN** `run` executes
- **THEN** the Langfuse trace MUST include tags `pattern:exception_handling` and `backend:langchain`

### Requirement: MAF exception-handling module
The maf-lab package SHALL expose `sd_agentic_maf.exception_handling` that wraps the MAF tool-use Agent with the same Recovery and returns the same result shape.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-maf python -m sd_agentic_maf.exception_handling`
- **THEN** the process SHALL print JSON that includes `events`, `calls`, `reply`, and `stopped`

#### Scenario: Agent owns the tool loop
- **WHEN** the module runs
- **THEN** it MUST use a MAF Agent with tools rather than a hand-rolled OpenAI `complete()` helper for the agent loop

#### Scenario: Observability
- **WHEN** `run` executes
- **THEN** an OTEL span named `pattern.exception_handling` MUST be created with attributes identifying `pattern` as `exception_handling` and `backend` as `maf`

### Requirement: Patterns package stays framework-free
`packages/patterns` MUST NOT import LangChain or Microsoft Agent Framework as part of this change.

#### Scenario: Scratch unchanged
- **WHEN** this change is implemented
- **THEN** scratch exception handling MUST remain unmodified

### Requirement: README progress for exception-handling ports
The repository README SHALL record that exception-handling LangChain and MAF are done and SHALL document run commands for both modules.

#### Scenario: Progress cells
- **WHEN** the ports land
- **THEN** the Progress table row for pattern 12 Exception handling and recovery SHALL show scratch, LangChain, and MAF as `done`

#### Scenario: Run section
- **WHEN** a developer reads the README Run section
- **THEN** they SHALL find `uv run` commands for `sd_agentic_langchain.exception_handling` and `sd_agentic_maf.exception_handling`
