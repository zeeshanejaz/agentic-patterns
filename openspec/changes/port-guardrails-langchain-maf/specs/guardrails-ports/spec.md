## ADDED Requirements

### Requirement: LangChain guardrails module
`sd_agentic_langchain.guardrails` SHALL wrap a draft with LCEL input/output checks.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-langchain python -m sd_agentic_langchain.guardrails`
- **THEN** JSON SHALL include `input_ok`, `output_ok`, `violations`, and `reply`

#### Scenario: LCEL wrappers
- **WHEN** the module runs
- **THEN** it MUST use LCEL chains, not a LangGraph `StateGraph`

#### Scenario: Langfuse tags
- **WHEN** `run` executes
- **THEN** tags MUST include `pattern:guardrails` and `backend:langchain`

### Requirement: MAF guardrails module
`sd_agentic_maf.guardrails` SHALL use MAF Agents for scans and draft/rewrite.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-maf python -m sd_agentic_maf.guardrails`
- **THEN** JSON SHALL include `input_ok`, `output_ok`, `violations`, and `reply`

#### Scenario: Observability
- **WHEN** `run` executes
- **THEN** span `pattern.guardrails` MUST set `pattern=guardrails` and `backend=maf`

### Requirement: Patterns package stays framework-free
Scratch guardrails MUST remain unmodified.

#### Scenario: Scratch unchanged
- **WHEN** this change is implemented
- **THEN** scratch MUST not import LangChain or MAF

### Requirement: README progress for guardrails ports
Pattern 18 LangChain and MAF SHALL be shipped links with run commands.

#### Scenario: Progress cells
- **WHEN** the ports land
- **THEN** pattern 18 SHALL show all three labs as shipped links

#### Scenario: Run section
- **WHEN** a developer reads Run
- **THEN** they SHALL find langchain and maf `guardrails` commands
