## ADDED Requirements

### Requirement: Scratch resource-aware module
The patterns package SHALL expose `sd_agentic_patterns.resource_aware` that classifies ticket complexity and replies on a cheap or expensive path, without importing LangChain or Microsoft Agent Framework.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-patterns python -m sd_agentic_patterns.resource_aware`
- **THEN** the process SHALL print JSON per sample email including `route`, `cost_units`, and `reply`

#### Scenario: Cheap vs expensive
- **WHEN** a ticket is classified `simple`
- **THEN** it MUST use the cheap prompt path
- **WHEN** a ticket is classified `complex` (including refund-over-$50)
- **THEN** it MUST use the expensive prompt path

#### Scenario: Policy
- **WHEN** a reply is written
- **THEN** it MUST follow shared `POLICY`

#### Scenario: Langfuse tags
- **WHEN** `run` executes
- **THEN** the Langfuse trace MUST include tags `pattern:resource_aware` and `backend:scratch`

### Requirement: Shared resource-aware prompts
`RESOURCE_CLASSIFY_SYSTEM`, `RESOURCE_CHEAP_SYSTEM`, and `RESOURCE_EXPENSIVE_SYSTEM` SHALL live in `packages/shared`.

#### Scenario: Prompts are importable
- **WHEN** a lab imports those names from `sd_agentic_shared.prompts`
- **THEN** they MUST be defined

### Requirement: README progress for resource-aware scratch
Pattern 16 scratch SHALL be a shipped file link; LangChain and MAF remain pending; a run command exists.

#### Scenario: Progress cells
- **WHEN** this change lands
- **THEN** the Progress table row for pattern 16 SHALL show scratch as shipped and LangChain and MAF as `pending`

#### Scenario: Run section
- **WHEN** a developer reads the README Run section
- **THEN** they SHALL find `uv run --package sd-agentic-patterns python -m sd_agentic_patterns.resource_aware`
