## ADDED Requirements

### Requirement: From-scratch prioritization module
`sd_agentic_patterns.prioritization` SHALL score a support inbox, execute the highest-priority tickets, and re-score the rest.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-patterns python -m sd_agentic_patterns.prioritization`
- **THEN** JSON SHALL include `initial`, `executed`, and `leftover`

#### Scenario: Inbox
- **WHEN** `run` executes
- **THEN** it MUST rank the shared `SAMPLE_EMAILS` queue

#### Scenario: Execute budget
- **WHEN** `run` executes
- **THEN** it MUST draft at most `MAX_EXECUTE` tickets and leave the rest in `leftover`

#### Scenario: Langfuse tags
- **WHEN** `run` executes
- **THEN** tags MUST include `pattern:prioritization` and `backend:scratch`

### Requirement: Patterns package stays framework-free
The prioritization module MUST NOT import LangChain or Microsoft Agent Framework.

#### Scenario: No framework imports
- **WHEN** the module is inspected
- **THEN** it MUST use the OpenAI wrapper in `sd_agentic_patterns.llm` only

### Requirement: README progress for prioritization scratch
Pattern 20 scratch SHALL be a shipped link; LangChain and MAF remain pending until ported.

#### Scenario: Progress cell
- **WHEN** this change lands
- **THEN** pattern 20 scratch SHALL link `packages/patterns/src/sd_agentic_patterns/prioritization.py`

#### Scenario: Run section
- **WHEN** a developer reads Run
- **THEN** they SHALL find the from-scratch `prioritization` command
