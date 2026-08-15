## ADDED Requirements

### Requirement: LangChain prioritization module
`sd_agentic_langchain.prioritization` SHALL score a support inbox with a LangGraph re-score cycle.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-langchain python -m sd_agentic_langchain.prioritization`
- **THEN** JSON SHALL include `initial`, `executed`, and `leftover`

#### Scenario: LangGraph cycle
- **WHEN** the module runs
- **THEN** it MUST use a `StateGraph` for score → execute → age leftover, not a Python `while` around LCEL only

#### Scenario: Langfuse tags
- **WHEN** `run` executes
- **THEN** tags MUST include `pattern:prioritization` and `backend:langchain`

### Requirement: MAF prioritization module
`sd_agentic_maf.prioritization` SHALL use MAF Agents to score and draft tickets from the inbox.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-maf python -m sd_agentic_maf.prioritization`
- **THEN** JSON SHALL include `initial`, `executed`, and `leftover`

#### Scenario: Observability
- **WHEN** `run` executes
- **THEN** span `pattern.prioritization` MUST set `pattern=prioritization` and `backend=maf`

### Requirement: Patterns package stays framework-free
Scratch prioritization MUST remain unmodified.

#### Scenario: Scratch unchanged
- **WHEN** this change is implemented
- **THEN** scratch MUST not import LangChain or MAF

### Requirement: README progress for prioritization ports
Pattern 20 LangChain and MAF SHALL be shipped links with run commands.

#### Scenario: Progress cells
- **WHEN** the ports land
- **THEN** pattern 20 SHALL show all three labs as shipped links

#### Scenario: Run section
- **WHEN** a developer reads Run
- **THEN** they SHALL find langchain and maf `prioritization` commands
