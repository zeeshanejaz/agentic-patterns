## ADDED Requirements

### Requirement: LangChain resource-aware module
`sd_agentic_langchain.resource_aware` SHALL classify complexity and reply on a cheap or expensive LCEL path.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-langchain python -m sd_agentic_langchain.resource_aware`
- **THEN** the process SHALL print JSON per sample email with `route`, `cost_units`, and `reply`

#### Scenario: LCEL branch
- **WHEN** the module replies
- **THEN** it MUST use LCEL (`RunnableBranch` or equivalent) rather than a LangGraph `StateGraph`

#### Scenario: Langfuse tags
- **WHEN** `run` executes
- **THEN** tags MUST include `pattern:resource_aware` and `backend:langchain`

### Requirement: MAF resource-aware module
`sd_agentic_maf.resource_aware` SHALL use MAF Agents for classify and both reply paths.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-maf python -m sd_agentic_maf.resource_aware`
- **THEN** the process SHALL print JSON with `route`, `cost_units`, and `reply`

#### Scenario: Observability
- **WHEN** `run` executes
- **THEN** an OTEL span `pattern.resource_aware` MUST set `pattern=resource_aware` and `backend=maf`

### Requirement: Patterns package stays framework-free
Scratch resource-aware MUST remain unmodified.

#### Scenario: Scratch unchanged
- **WHEN** this change is implemented
- **THEN** scratch MUST not import LangChain or MAF

### Requirement: README progress for resource-aware ports
Pattern 16 LangChain and MAF SHALL be shipped file links with run commands.

#### Scenario: Progress cells
- **WHEN** the ports land
- **THEN** pattern 16 SHALL show all three labs as shipped links

#### Scenario: Run section
- **WHEN** a developer reads Run
- **THEN** they SHALL find langchain and maf `resource_aware` commands
