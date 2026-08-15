## ADDED Requirements

### Requirement: Scratch guardrails module
`sd_agentic_patterns.guardrails` SHALL check input and output around a support draft without LangChain or MAF.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-patterns python -m sd_agentic_patterns.guardrails`
- **THEN** JSON SHALL include `input_ok`, `output_ok`, `violations`, and `reply`

#### Scenario: Output policy guard
- **WHEN** a draft promises a refund over $50
- **THEN** `output_ok` MUST be false and the final reply MUST NOT promise that refund

#### Scenario: Policy
- **WHEN** a reply is emitted
- **THEN** it MUST follow shared `POLICY`

#### Scenario: Langfuse tags
- **WHEN** `run` executes
- **THEN** tags MUST include `pattern:guardrails` and `backend:scratch`

### Requirement: Shared guardrail prompts
`GUARDRAIL_INPUT_SYSTEM` and `GUARDRAIL_OUTPUT_SYSTEM` SHALL live in shared prompts.

#### Scenario: Prompts are importable
- **WHEN** a lab imports those names
- **THEN** they MUST be defined

### Requirement: README progress for guardrails scratch
Pattern 18 scratch SHALL be a shipped link; LangChain/MAF pending.

#### Scenario: Progress cells
- **WHEN** this change lands
- **THEN** pattern 18 scratch SHALL be shipped and LangChain/MAF `pending`

#### Scenario: Run section
- **WHEN** a developer reads Run
- **THEN** they SHALL find `sd_agentic_patterns.guardrails`
