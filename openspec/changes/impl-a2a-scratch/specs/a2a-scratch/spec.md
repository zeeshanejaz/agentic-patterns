## ADDED Requirements

### Requirement: Scratch A2A module
The patterns package SHALL expose `sd_agentic_patterns.a2a` that coordinates support specialists over a message bus of envelopes and produces a policy-bound customer reply, without importing LangChain or Microsoft Agent Framework.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-patterns python -m sd_agentic_patterns.a2a`
- **THEN** the process SHALL print JSON that includes `envelopes` (each with `id`, `sender`, `recipient`, `ttl`) and a `reply`

#### Scenario: Bus drops stale mail
- **WHEN** an envelope's `ttl` is below the current turn
- **THEN** the bus MUST NOT deliver it to the recipient

#### Scenario: Cap
- **WHEN** posted envelopes would exceed `MAX_MESSAGES`
- **THEN** the module MUST stop posting further specialist mail

#### Scenario: Policy
- **WHEN** the writer replies
- **THEN** it MUST follow shared `POLICY`

#### Scenario: Langfuse tags
- **WHEN** `run` executes
- **THEN** the Langfuse trace MUST include tags `pattern:a2a` and `backend:scratch`

### Requirement: Shared A2A message prompt
An inter-agent message prompt SHALL live in `packages/shared`.

#### Scenario: Prompt is importable
- **WHEN** a lab imports `A2A_MESSAGE_SYSTEM` from `sd_agentic_shared.prompts`
- **THEN** it MUST be defined

### Requirement: README progress for A2A scratch
The README SHALL record A2A scratch as shipped and document a run command. LangChain and MAF A2A cells SHALL remain pending.

#### Scenario: Progress cells
- **WHEN** this change lands
- **THEN** the Progress table row for pattern 15 Inter-agent communication (A2A) SHALL show scratch as shipped and LangChain and MAF as `pending`

#### Scenario: Run section
- **WHEN** a developer reads the README Run section
- **THEN** they SHALL find `uv run --package sd-agentic-patterns python -m sd_agentic_patterns.a2a`
