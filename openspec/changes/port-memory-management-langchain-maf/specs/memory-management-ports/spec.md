## ADDED Requirements

### Requirement: LangChain memory-management module
The langchain-lab package SHALL expose `sd_agentic_langchain.memory_management` that maintains short-term, episodic, and long-term memory across `MEMORY_THREAD` via LangGraph and produces a policy-bound reply each turn.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-langchain python -m sd_agentic_langchain.memory_management`
- **THEN** the process SHALL print JSON for each `MEMORY_THREAD` turn that includes `turn`, `retrieved`, `reply`, and the memory snapshot (`short_term`, `episodic`, `long_term`)

#### Scenario: Retrieve before reply
- **WHEN** a reply is written on turn 2 or later
- **THEN** the writer MUST receive retrieved episodic and/or long-term items from prior turns

#### Scenario: Compact on budget
- **WHEN** episodic items exceed `MAX_EPISODIC` or long-term items exceed `MAX_LONG_TERM`
- **THEN** the store MUST drop the oldest items of that tier until it fits

#### Scenario: Shared thread and prompts
- **WHEN** the module runs
- **THEN** it MUST use `MEMORY_THREAD` from `sd_agentic_shared.tasks.support_email` and `MEMORY_EXTRACT_SYSTEM` / `MEMORY_REPLY_SYSTEM` from shared prompts

#### Scenario: Langfuse tags
- **WHEN** `run` executes
- **THEN** the Langfuse trace MUST include tags `pattern:memory_management` and `backend:langchain`

### Requirement: MAF memory-management module
The maf-lab package SHALL expose `sd_agentic_maf.memory_management` that runs the same retrieve → reply → extract flow with MAF Agents and returns the same result shape.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-maf python -m sd_agentic_maf.memory_management`
- **THEN** the process SHALL print JSON for each `MEMORY_THREAD` turn with `turn`, `retrieved`, `reply`, and the memory snapshot

#### Scenario: Agents own LLM steps
- **WHEN** the module writes a reply or extracts memories
- **THEN** it MUST use MAF Agent invocation rather than a hand-rolled OpenAI `complete()` helper

#### Scenario: Observability
- **WHEN** `run` executes
- **THEN** an OTEL span named `pattern.memory_management` MUST be created with attributes identifying `pattern` as `memory_management` and `backend` as `maf`

### Requirement: Patterns package stays framework-free
`packages/patterns` MUST NOT import LangChain or Microsoft Agent Framework as part of this change.

#### Scenario: Scratch unchanged
- **WHEN** this change is implemented
- **THEN** scratch memory management MUST remain unmodified

### Requirement: README progress for memory-management ports
The repository README SHALL record that memory management LangChain and MAF are done and SHALL document run commands for both modules.

#### Scenario: Progress cells
- **WHEN** the ports land
- **THEN** the Progress table row for pattern 8 Memory management SHALL show scratch, LangChain, and MAF as `done`

#### Scenario: Run section
- **WHEN** a developer reads the README Run section
- **THEN** they SHALL find `uv run` commands for `sd_agentic_langchain.memory_management` and `sd_agentic_maf.memory_management`
