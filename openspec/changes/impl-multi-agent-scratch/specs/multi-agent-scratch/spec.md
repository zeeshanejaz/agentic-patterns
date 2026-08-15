## ADDED Requirements

### Requirement: Scratch multi-agent module
The patterns package SHALL expose `sd_agentic_patterns.multi_agent` that runs a coordinator, named specialist agents, a shared notes board, and a writer, without importing LangChain or Microsoft Agent Framework.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-patterns python -m sd_agentic_patterns.multi_agent`
- **THEN** the process SHALL print JSON that includes `assignments`, `notes`, `rounds`, and `reply` for `SUPPORT_EMAIL`

#### Scenario: Coordinator assigns specialists
- **WHEN** a plan of work is produced
- **THEN** each assignment MUST name an agent from the roster `billing`, `shipping`, `policy` and include an instruction

#### Scenario: Specialists write shared notes
- **WHEN** a specialist runs
- **THEN** it MUST append a note `{agent, text}` to the shared board rather than sending a customer email

#### Scenario: Extra coordinator round
- **WHEN** the first specialist round finishes
- **THEN** the coordinator MAY assign more specialists at most once (`MAX_ROUNDS = 2`) before the writer runs

#### Scenario: Policy
- **WHEN** the final reply is written
- **THEN** it MUST be produced under the shared support `POLICY` (no invented order facts, no refunds over $50 without human approval, no blaming the customer)

#### Scenario: Langfuse tags
- **WHEN** `run` executes
- **THEN** the Langfuse trace MUST include tags `pattern:multi_agent` and `backend:scratch`

### Requirement: Shared multi-agent prompts
Coordinator, specialist, review, and writer prompts SHALL live in `sd_agentic_shared.prompts` so later ports can reuse them.

#### Scenario: Prompts are importable
- **WHEN** a lab imports multi-agent prompts from `sd_agentic_shared.prompts`
- **THEN** `COORDINATOR_SYSTEM`, `COORDINATOR_REVIEW_SYSTEM`, `BILLING_AGENT_SYSTEM`, `SHIPPING_AGENT_SYSTEM`, `POLICY_AGENT_SYSTEM`, and `WRITER_AGENT_SYSTEM` MUST be defined

### Requirement: README progress for multi-agent scratch
The repository README SHALL record that multi-agent collaboration scratch is done and SHALL document a run command for the module. LangChain and MAF multi-agent cells SHALL remain pending.

#### Scenario: Progress cells
- **WHEN** this change lands
- **THEN** the Progress table row for pattern 7 Multi-agent collaboration SHALL show scratch as `done` and LangChain and MAF as `pending`

#### Scenario: Run section
- **WHEN** a developer reads the README Run section
- **THEN** they SHALL find `uv run --package sd-agentic-patterns python -m sd_agentic_patterns.multi_agent`
