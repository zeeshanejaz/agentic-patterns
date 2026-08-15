## ADDED Requirements

### Requirement: Scratch memory-management module
The patterns package SHALL expose `sd_agentic_patterns.memory_management` that maintains short-term, episodic, and long-term memory across a support-email thread and produces a policy-bound reply each turn, without importing LangChain or Microsoft Agent Framework.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-patterns python -m sd_agentic_patterns.memory_management`
- **THEN** the process SHALL print JSON for each `MEMORY_THREAD` turn that includes `turn`, `retrieved`, `reply`, and the memory snapshot (`short_term`, `episodic`, `long_term`)

#### Scenario: Three memory tiers
- **WHEN** a turn is processed
- **THEN** short-term MUST be the current email, episodic MUST be turn summaries, and long-term MUST be durable customer facts

#### Scenario: Retrieve before reply
- **WHEN** a reply is written on turn 2 or later
- **THEN** the writer MUST receive retrieved episodic and/or long-term items from prior turns (not only the current email)

#### Scenario: Compact on budget
- **WHEN** episodic items exceed `MAX_EPISODIC` or long-term items exceed `MAX_LONG_TERM`
- **THEN** the store MUST drop the oldest items of that tier until it fits

#### Scenario: Policy
- **WHEN** a reply is written
- **THEN** it MUST be produced under the shared support `POLICY` (no invented order facts, no refunds over $50 without human approval, no blaming the customer)

#### Scenario: Langfuse tags
- **WHEN** `run` executes
- **THEN** the Langfuse trace MUST include tags `pattern:memory_management` and `backend:scratch`

### Requirement: Shared memory thread and prompts
The multi-turn emails and memory prompts SHALL live in `packages/shared` so later ports can reuse them.

#### Scenario: Thread is importable
- **WHEN** a lab imports `MEMORY_THREAD` from `sd_agentic_shared.tasks.support_email`
- **THEN** it MUST be a sequence of at least three related support emails starting with `SUPPORT_EMAIL`

#### Scenario: Prompts are importable
- **WHEN** a lab imports memory prompts from `sd_agentic_shared.prompts`
- **THEN** `MEMORY_EXTRACT_SYSTEM`, `MEMORY_REPLY_SYSTEM` MUST be defined

### Requirement: README progress for memory-management scratch
The repository README SHALL record that memory management scratch is done and SHALL document a run command for the module. LangChain and MAF memory cells SHALL remain pending.

#### Scenario: Progress cells
- **WHEN** this change lands
- **THEN** the Progress table row for pattern 8 Memory management SHALL show scratch as `done` and LangChain and MAF as `pending`

#### Scenario: Run section
- **WHEN** a developer reads the README Run section
- **THEN** they SHALL find `uv run --package sd-agentic-patterns python -m sd_agentic_patterns.memory_management`
