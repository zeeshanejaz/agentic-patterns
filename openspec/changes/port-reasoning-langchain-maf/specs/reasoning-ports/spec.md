## ADDED Requirements

### Requirement: LangChain reasoning module
`sd_agentic_langchain.reasoning` SHALL collect CoT samples via LangGraph and print a chosen reply.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-langchain python -m sd_agentic_langchain.reasoning`
- **THEN** JSON SHALL include `samples` with `steps` and a `reply`

#### Scenario: Graph owns the sample loop
- **WHEN** the module runs
- **THEN** it MUST use a LangGraph `StateGraph` for repeated sampling (not a Python `while` around LCEL only)

#### Scenario: Langfuse tags
- **WHEN** `run` executes
- **THEN** tags MUST include `pattern:reasoning` and `backend:langchain`

### Requirement: MAF reasoning module
`sd_agentic_maf.reasoning` SHALL use MAF Agents for CoT samples.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-maf python -m sd_agentic_maf.reasoning`
- **THEN** JSON SHALL include `samples` and `reply`

#### Scenario: Observability
- **WHEN** `run` executes
- **THEN** span `pattern.reasoning` MUST set `pattern=reasoning` and `backend=maf`

### Requirement: Patterns package stays framework-free
Scratch reasoning MUST remain unmodified.

#### Scenario: Scratch unchanged
- **WHEN** this change is implemented
- **THEN** scratch MUST not import LangChain or MAF

### Requirement: README progress for reasoning ports
Pattern 17 LangChain and MAF SHALL be shipped links with run commands.

#### Scenario: Progress cells
- **WHEN** the ports land
- **THEN** pattern 17 SHALL show all three labs as shipped links

#### Scenario: Run section
- **WHEN** a developer reads Run
- **THEN** they SHALL find langchain and maf `reasoning` commands
