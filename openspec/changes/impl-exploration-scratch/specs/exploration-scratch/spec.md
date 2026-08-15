## ADDED Requirements

### Requirement: From-scratch exploration module
`sd_agentic_patterns.exploration` SHALL expand reply angles, score them, prune weak branches, and pick a survivor.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-patterns python -m sd_agentic_patterns.exploration`
- **THEN** JSON SHALL include `branches` (each with `angle`, `score`, `kept`, `reply`) and a chosen `reply`

#### Scenario: Branch, score, prune
- **WHEN** `run` executes
- **THEN** it MUST draft every shared `EXPLORE_ANGLES` item, score each, and set `kept` false when the score is below threshold or the draft promises a refund over $50

#### Scenario: Langfuse tags
- **WHEN** `run` executes
- **THEN** tags MUST include `pattern:exploration` and `backend:scratch`

### Requirement: Patterns package stays framework-free
The exploration module MUST NOT import LangChain or Microsoft Agent Framework.

#### Scenario: No framework imports
- **WHEN** the module is inspected
- **THEN** it MUST use the OpenAI wrapper in `sd_agentic_patterns.llm` only

### Requirement: README progress for exploration scratch
Pattern 21 scratch SHALL be a shipped link; LangChain and MAF remain pending until ported.

#### Scenario: Progress cell
- **WHEN** this change lands
- **THEN** pattern 21 scratch SHALL link `packages/patterns/src/sd_agentic_patterns/exploration.py`

#### Scenario: Run section
- **WHEN** a developer reads Run
- **THEN** they SHALL find the from-scratch `exploration` command
