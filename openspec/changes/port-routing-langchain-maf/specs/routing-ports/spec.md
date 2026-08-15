## ADDED Requirements

### Requirement: LangChain routing module
The langchain-lab package SHALL expose `sd_agentic_langchain.routing` that classifies each shared sample support email into exactly one of `billing`, `shipping`, `cancel`, or `other`, then produces a specialist reply using the matching shared handler prompt.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-langchain python -m sd_agentic_langchain.routing`
- **THEN** the process iterates `SAMPLE_EMAILS` from `sd_agentic_shared.tasks.support_email` and prints a JSON object with `intent` and `reply` for each label

#### Scenario: Shared prompts only
- **WHEN** the LangChain routing module classifies or handles an email
- **THEN** it MUST use `ROUTE_SYSTEM` and the corresponding `BILLING_HANDLER_SYSTEM` / `SHIPPING_HANDLER_SYSTEM` / `CANCEL_HANDLER_SYSTEM` / `OTHER_HANDLER_SYSTEM` from `sd_agentic_shared.prompts` without rewriting those strings locally

#### Scenario: Unknown classify token falls back
- **WHEN** the classifier output is empty or not one of `billing`, `shipping`, `cancel`, `other`
- **THEN** the module MUST treat the intent as `other` and use `OTHER_HANDLER_SYSTEM`

#### Scenario: Langfuse tags
- **WHEN** `run` executes for an email
- **THEN** the Langfuse trace MUST include tags `pattern:routing` and `backend:langchain`

### Requirement: MAF routing module
The maf-lab package SHALL expose `sd_agentic_maf.routing` that classifies each shared sample support email into exactly one of `billing`, `shipping`, `cancel`, or `other`, then produces a specialist reply by running one specialist Agent whose instructions are the matching shared handler prompt.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-maf python -m sd_agentic_maf.routing`
- **THEN** the process iterates `SAMPLE_EMAILS` from `sd_agentic_shared.tasks.support_email` and prints a JSON object with `intent` and `reply` for each label

#### Scenario: Shared prompts only
- **WHEN** the MAF routing module classifies or handles an email
- **THEN** it MUST use `ROUTE_SYSTEM` and the corresponding handler system prompts from `sd_agentic_shared.prompts` without rewriting those strings locally

#### Scenario: One specialist per email
- **WHEN** an email has been classified
- **THEN** the module MUST run exactly one specialist Agent for that intent (not a sequential chain of all handlers, and not a conversational handoff loop)

#### Scenario: Unknown classify token falls back
- **WHEN** the classifier output is empty or not one of `billing`, `shipping`, `cancel`, `other`
- **THEN** the module MUST treat the intent as `other` and use `OTHER_HANDLER_SYSTEM`

#### Scenario: Observability
- **WHEN** `run` executes for an email
- **THEN** an OTEL span named `pattern.routing` MUST be created with attributes identifying `pattern` as `routing` and `backend` as `maf`

### Requirement: Patterns package stays framework-free
`packages/patterns` MUST NOT import LangChain or Microsoft Agent Framework as part of this change.

#### Scenario: No new scratch coupling
- **WHEN** this change is implemented
- **THEN** scratch routing remains the source of the loop and is not modified except if a shared type move is explicitly tasked (it is not)

### Requirement: README progress for routing ports
The repository README SHALL record that routing LangChain and MAF are done and SHALL document run commands for both modules.

#### Scenario: Progress cells
- **WHEN** the ports land
- **THEN** the Progress table row for pattern 2 Routing SHALL show LangChain and MAF as `done`

#### Scenario: Run section
- **WHEN** a developer reads the README Run section
- **THEN** they SHALL find `uv run` commands for `sd_agentic_langchain.routing` and `sd_agentic_maf.routing`
