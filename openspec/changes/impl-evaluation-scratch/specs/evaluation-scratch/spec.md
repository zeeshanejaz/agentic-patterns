## ADDED Requirements

### Requirement: From-scratch evaluation module
`sd_agentic_patterns.evaluation` SHALL wrap summarize/draft with golden heuristics and an LLM judge.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-patterns python -m sd_agentic_patterns.evaluation`
- **THEN** JSON SHALL include `pass_rate` and a `cases` list with `heuristic_ok`, `judge_pass`, and `overall_pass`

#### Scenario: Golden cases
- **WHEN** `run` executes
- **THEN** it MUST score the shared `EVAL_CASES` inbox (the four sample emails)

#### Scenario: Heuristics
- **WHEN** a draft promises a refund over $50, omits a required order id, or blames the customer
- **THEN** `heuristic_ok` MUST be false

#### Scenario: Langfuse tags
- **WHEN** `run` executes
- **THEN** tags MUST include `pattern:evaluation` and `backend:scratch`

### Requirement: Patterns package stays framework-free
The evaluation module MUST NOT import LangChain or Microsoft Agent Framework.

#### Scenario: No framework imports
- **WHEN** the module is inspected
- **THEN** it MUST use the OpenAI wrapper in `sd_agentic_patterns.llm` only

### Requirement: README progress for evaluation scratch
Pattern 19 scratch SHALL be a shipped link; LangChain and MAF remain pending until ported.

#### Scenario: Progress cell
- **WHEN** this change lands
- **THEN** pattern 19 scratch SHALL link `packages/patterns/src/sd_agentic_patterns/evaluation.py`

#### Scenario: Run section
- **WHEN** a developer reads Run
- **THEN** they SHALL find the from-scratch `evaluation` command
