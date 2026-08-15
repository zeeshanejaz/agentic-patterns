## ADDED Requirements

### Requirement: LangChain reflection module
The langchain-lab package SHALL expose `sd_agentic_langchain.reflection` that summarizes a support email, drafts a reply, then critiques and revises until the critique starts with `PASS` or `MAX_ROUNDS` (3) is reached, using a LangGraph cycle.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-langchain python -m sd_agentic_langchain.reflection`
- **THEN** the process SHALL print JSON with `summary`, `rounds` (each with `draft` and `critique`), `final`, and `passed` for `SUPPORT_EMAIL`

#### Scenario: Shared prompts
- **WHEN** the graph runs
- **THEN** it MUST use `SUMMARIZE_SYSTEM`, `DRAFT_SYSTEM`, `CRITIC_SYSTEM`, and `REVISE_SYSTEM` from `sd_agentic_shared.prompts`

#### Scenario: Stop conditions
- **WHEN** a critique line starts with `PASS` (case-insensitive) or three critic rounds have run
- **THEN** the graph MUST stop revising and set `passed` true only if the last critique started with `PASS`

#### Scenario: Langfuse tags
- **WHEN** `run` executes
- **THEN** the Langfuse trace MUST include tags `pattern:reflection` and `backend:langchain`

### Requirement: MAF reflection module
The maf-lab package SHALL expose `sd_agentic_maf.reflection` that performs the same summarize → draft → critic/revise loop using MAF Agents and `MAX_ROUNDS` of 3.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-maf python -m sd_agentic_maf.reflection`
- **THEN** the process SHALL print JSON with `summary`, `rounds`, `final`, and `passed` for `SUPPORT_EMAIL`

#### Scenario: Shared prompts
- **WHEN** the loop runs
- **THEN** it MUST use `SUMMARIZE_SYSTEM`, `DRAFT_SYSTEM`, `CRITIC_SYSTEM`, and `REVISE_SYSTEM` from `sd_agentic_shared.prompts`

#### Scenario: Stop conditions
- **WHEN** a critique starts with `PASS` or three critic rounds have run
- **THEN** the loop MUST stop revising and set `passed` true only if the last critique started with `PASS`

#### Scenario: Observability
- **WHEN** `run` executes
- **THEN** an OTEL span named `pattern.reflection` MUST be created with attributes identifying `pattern` as `reflection` and `backend` as `maf`

### Requirement: Patterns package stays framework-free
`packages/patterns` MUST NOT import LangChain or Microsoft Agent Framework as part of this change.

#### Scenario: Scratch unchanged
- **WHEN** this change is implemented
- **THEN** scratch reflection MUST remain unmodified

### Requirement: README progress for reflection ports
The repository README SHALL record that reflection LangChain and MAF are done and SHALL document run commands for both modules.

#### Scenario: Progress cells
- **WHEN** the ports land
- **THEN** the Progress table row for pattern 4 Reflection SHALL show LangChain and MAF as `done`

#### Scenario: Run section
- **WHEN** a developer reads the README Run section
- **THEN** they SHALL find `uv run` commands for `sd_agentic_langchain.reflection` and `sd_agentic_maf.reflection`
