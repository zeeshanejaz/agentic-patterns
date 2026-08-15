## ADDED Requirements

### Requirement: Scratch human-in-the-loop module
The patterns package SHALL expose `sd_agentic_patterns.human_in_the_loop` that drafts a support reply, pauses for a human decision when the gate fires, and resumes, without importing LangChain or Microsoft Agent Framework.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-patterns python -m sd_agentic_patterns.human_in_the_loop`
- **THEN** the process SHALL print JSON that includes `summary`, `draft`, `gate`, `decision`, `reply`, and `interrupted`

#### Scenario: Gate on high-risk refund
- **WHEN** the email asks for a refund over $50
- **THEN** the module MUST set the gate to need a human (`interrupted` true) before sending a customer reply

#### Scenario: Resume from decision
- **WHEN** the reviewer returns `deny`
- **THEN** the final reply MUST NOT promise a refund over $50
- **WHEN** the reviewer returns `approve`
- **THEN** the final reply MAY use the draft (still under POLICY)
- **WHEN** the reviewer returns `edit`
- **THEN** the final reply MUST use the edited text from the decision

#### Scenario: Policy
- **WHEN** a reply is written
- **THEN** it MUST be produced under the shared support `POLICY`

#### Scenario: Langfuse tags
- **WHEN** `run` executes
- **THEN** the Langfuse trace MUST include tags `pattern:human_in_the_loop` and `backend:scratch`

### Requirement: Shared HITL prompts and canned decision
Gate/resume prompts and a non-interactive reviewer decision SHALL live in `packages/shared` so later ports can reuse them.

#### Scenario: Decision is importable
- **WHEN** a lab imports `HITL_DECISION` from `sd_agentic_shared.tasks.support_email`
- **THEN** it MUST have an `action` of `approve`, `edit`, or `deny`

#### Scenario: Prompts are importable
- **WHEN** a lab imports HITL prompts from `sd_agentic_shared.prompts`
- **THEN** `HITL_GATE_SYSTEM` and `HITL_RESUME_SYSTEM` MUST be defined

### Requirement: README progress for HITL scratch
The repository README SHALL record that human-in-the-loop scratch is done and SHALL document a run command for the module. LangChain and MAF HITL cells SHALL remain pending.

#### Scenario: Progress cells
- **WHEN** this change lands
- **THEN** the Progress table row for pattern 13 Human-in-the-loop SHALL show scratch as `done` and LangChain and MAF as `pending`

#### Scenario: Run section
- **WHEN** a developer reads the README Run section
- **THEN** they SHALL find `uv run --package sd-agentic-patterns python -m sd_agentic_patterns.human_in_the_loop`
