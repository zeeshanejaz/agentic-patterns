## ADDED Requirements

### Requirement: LangChain evaluation module
`sd_agentic_langchain.evaluation` SHALL wrap summarize/draft with LCEL heuristics and an LLM judge.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-langchain python -m sd_agentic_langchain.evaluation`
- **THEN** JSON SHALL include `pass_rate` and `cases` with `heuristic_ok`, `judge_pass`, and `overall_pass`

#### Scenario: LCEL wrappers
- **WHEN** the module runs
- **THEN** it MUST use LCEL chains, not a LangGraph `StateGraph`

#### Scenario: Langfuse tags
- **WHEN** `run` executes
- **THEN** tags MUST include `pattern:evaluation` and `backend:langchain`

### Requirement: MAF evaluation module
`sd_agentic_maf.evaluation` SHALL use MAF Agents for summarize, draft, and judge.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-maf python -m sd_agentic_maf.evaluation`
- **THEN** JSON SHALL include `pass_rate` and `cases` with `heuristic_ok`, `judge_pass`, and `overall_pass`

#### Scenario: Observability
- **WHEN** `run` executes
- **THEN** span `pattern.evaluation` MUST set `pattern=evaluation` and `backend=maf`

### Requirement: Patterns package stays framework-free
Scratch evaluation MUST remain unmodified.

#### Scenario: Scratch unchanged
- **WHEN** this change is implemented
- **THEN** scratch MUST not import LangChain or MAF

### Requirement: README progress for evaluation ports
Pattern 19 LangChain and MAF SHALL be shipped links with run commands.

#### Scenario: Progress cells
- **WHEN** the ports land
- **THEN** pattern 19 SHALL show all three labs as shipped links

#### Scenario: Run section
- **WHEN** a developer reads Run
- **THEN** they SHALL find langchain and maf `evaluation` commands
