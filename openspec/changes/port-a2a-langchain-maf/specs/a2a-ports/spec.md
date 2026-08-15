## ADDED Requirements

### Requirement: LangChain A2A module
The langchain-lab package SHALL expose `sd_agentic_langchain.a2a` that runs the envelope bus over LangGraph.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-langchain python -m sd_agentic_langchain.a2a`
- **THEN** the process SHALL print JSON that includes `envelopes` with `id`/`sender`/`recipient`/`ttl` and a `reply`

#### Scenario: Graph owns topology
- **WHEN** the module runs
- **THEN** it MUST use a LangGraph `StateGraph` (not only a Python loop around LCEL)

#### Scenario: Langfuse tags
- **WHEN** `run` executes
- **THEN** the Langfuse trace MUST include tags `pattern:a2a` and `backend:langchain`

### Requirement: MAF A2A module
The maf-lab package SHALL expose `sd_agentic_maf.a2a` with MAF Agents on the same bus semantics.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-maf python -m sd_agentic_maf.a2a`
- **THEN** the process SHALL print JSON that includes `envelopes` and a `reply`

#### Scenario: Agents own LLM steps
- **WHEN** specialists or the writer produce text
- **THEN** it MUST use MAF Agent invocation

#### Scenario: Observability
- **WHEN** `run` executes
- **THEN** an OTEL span named `pattern.a2a` MUST have attributes `pattern=a2a` and `backend=maf`

### Requirement: Patterns package stays framework-free
Scratch A2A MUST remain unmodified.

#### Scenario: Scratch unchanged
- **WHEN** this change is implemented
- **THEN** `sd_agentic_patterns.a2a` MUST not gain LangChain or MAF imports

### Requirement: README progress for A2A ports
Pattern 15 LangChain and MAF cells SHALL be shipped file links with run commands.

#### Scenario: Progress cells
- **WHEN** the ports land
- **THEN** the Progress table row for pattern 15 SHALL show scratch, LangChain, and MAF as shipped links

#### Scenario: Run section
- **WHEN** a developer reads the README Run section
- **THEN** they SHALL find `uv run` commands for `sd_agentic_langchain.a2a` and `sd_agentic_maf.a2a`
