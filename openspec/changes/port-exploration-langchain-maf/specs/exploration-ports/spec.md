## ADDED Requirements

### Requirement: LangChain exploration module
`sd_agentic_langchain.exploration` SHALL expand, score, and prune reply angles with a LangGraph cycle.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-langchain python -m sd_agentic_langchain.exploration`
- **THEN** JSON SHALL include `branches` (angle, score, kept, reply) and a chosen `reply`

#### Scenario: LangGraph cycle
- **WHEN** the module runs
- **THEN** it MUST use a `StateGraph` for expand → score → prune, not a Python `while` around LCEL only

#### Scenario: Langfuse tags
- **WHEN** `run` executes
- **THEN** tags MUST include `pattern:exploration` and `backend:langchain`

### Requirement: MAF exploration module
`sd_agentic_maf.exploration` SHALL use MAF Agents to expand and score branches.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-maf python -m sd_agentic_maf.exploration`
- **THEN** JSON SHALL include `branches` and a chosen `reply`

#### Scenario: Observability
- **WHEN** `run` executes
- **THEN** span `pattern.exploration` MUST set `pattern=exploration` and `backend=maf`

### Requirement: Patterns package stays framework-free
Scratch exploration MUST remain unmodified.

#### Scenario: Scratch unchanged
- **WHEN** this change is implemented
- **THEN** scratch MUST not import LangChain or MAF

### Requirement: README progress for exploration ports
Pattern 21 LangChain and MAF SHALL be shipped links; the 21-pattern table SHALL have no `pending` cells.

#### Scenario: Progress cells
- **WHEN** the ports land
- **THEN** pattern 21 SHALL show all three labs as shipped links

#### Scenario: Run section
- **WHEN** a developer reads Run
- **THEN** they SHALL find langchain and maf `exploration` commands
