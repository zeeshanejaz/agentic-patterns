## ADDED Requirements

### Requirement: LangChain parallelization module
The langchain-lab package SHALL expose `sd_agentic_langchain.parallelization` that implements sectioning and voting on the shared support email using LangGraph fan-out/fan-in.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-langchain python -m sd_agentic_langchain.parallelization`
- **THEN** the process SHALL print a sectioning JSON object with `order`, `payment`, `ask`, and `summary`, and a voting JSON object with `drafts` and `merged`, using `SUPPORT_EMAIL`

#### Scenario: Sectioning uses shared prompts
- **WHEN** sectioning runs
- **THEN** the three extractors MUST use `SECTION_ORDER_SYSTEM`, `SECTION_PAYMENT_SYSTEM`, and `SECTION_ASK_SYSTEM`, and the merge step MUST use `MERGE_SECTIONS_SYSTEM`

#### Scenario: Voting uses three drafts then merge
- **WHEN** voting runs
- **THEN** the module MUST produce three draft replies and merge them with `VOTE_MERGE_SYSTEM`

#### Scenario: Langfuse tags
- **WHEN** sectioning or voting runs
- **THEN** the Langfuse trace MUST include tags `pattern:parallelization` and `backend:langchain`

### Requirement: MAF parallelization module
The maf-lab package SHALL expose `sd_agentic_maf.parallelization` that implements sectioning and voting on the shared support email using concurrent MAF agents.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-maf python -m sd_agentic_maf.parallelization`
- **THEN** the process SHALL print a sectioning JSON object with `order`, `payment`, `ask`, and `summary`, and a voting JSON object with `drafts` and `merged`, using `SUPPORT_EMAIL`

#### Scenario: Sectioning uses ConcurrentBuilder
- **WHEN** sectioning runs
- **THEN** the three extractors MUST run via `ConcurrentBuilder` (or equivalent fan-out) using the shared section prompts, then a merge Agent MUST use `MERGE_SECTIONS_SYSTEM`

#### Scenario: Voting uses concurrent drafts
- **WHEN** voting runs
- **THEN** three draft Agents MUST run concurrently and a merge Agent MUST use `VOTE_MERGE_SYSTEM`

#### Scenario: Observability
- **WHEN** sectioning or voting runs
- **THEN** an OTEL span named `pattern.parallelization.sectioning` or `pattern.parallelization.voting` MUST be created with attributes identifying `pattern` as `parallelization` and `backend` as `maf`

### Requirement: Patterns package stays framework-free
`packages/patterns` MUST NOT import LangChain or Microsoft Agent Framework as part of this change.

#### Scenario: Scratch unchanged
- **WHEN** this change is implemented
- **THEN** scratch parallelization MUST remain unmodified

### Requirement: README progress for parallelization ports
The repository README SHALL record that parallelization LangChain and MAF are done and SHALL document run commands for both modules.

#### Scenario: Progress cells
- **WHEN** the ports land
- **THEN** the Progress table row for pattern 3 Parallelization SHALL show LangChain and MAF as `done`

#### Scenario: Run section
- **WHEN** a developer reads the README Run section
- **THEN** they SHALL find `uv run` commands for `sd_agentic_langchain.parallelization` and `sd_agentic_maf.parallelization`
