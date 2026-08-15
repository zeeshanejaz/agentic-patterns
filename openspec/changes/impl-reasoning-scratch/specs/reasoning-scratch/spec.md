## ADDED Requirements

### Requirement: Scratch reasoning module
`sd_agentic_patterns.reasoning` SHALL produce CoT samples and a chosen policy-bound reply without LangChain or MAF.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-patterns python -m sd_agentic_patterns.reasoning`
- **THEN** the process SHALL print JSON with `samples` (each with `steps` and `reply`) and `reply`

#### Scenario: Chain of thought
- **WHEN** `run` executes
- **THEN** it MUST produce at least two samples each containing reasoning `steps` before the customer `reply`

#### Scenario: Policy
- **WHEN** a reply is chosen
- **THEN** it MUST follow shared `POLICY`

#### Scenario: Langfuse tags
- **WHEN** `run` executes
- **THEN** tags MUST include `pattern:reasoning` and `backend:scratch`

### Requirement: Shared reasoning prompt
`REASONING_SYSTEM` SHALL live in shared prompts.

#### Scenario: Prompt is importable
- **WHEN** a lab imports `REASONING_SYSTEM`
- **THEN** it MUST be defined

### Requirement: README progress for reasoning scratch
Pattern 17 scratch SHALL be a shipped link; LangChain/MAF pending; run command exists.

#### Scenario: Progress cells
- **WHEN** this change lands
- **THEN** pattern 17 scratch SHALL be shipped and LangChain/MAF `pending`

#### Scenario: Run section
- **WHEN** a developer reads Run
- **THEN** they SHALL find `sd_agentic_patterns.reasoning`
