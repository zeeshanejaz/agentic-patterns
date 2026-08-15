## ADDED Requirements

### Requirement: Scratch learning module
The patterns package SHALL expose `sd_agentic_patterns.learning` that collects simulated supervisor feedback, distills it into prompt lessons, and compares a baseline reply to an adapted reply on a held-out support email, without importing LangChain or Microsoft Agent Framework.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-patterns python -m sd_agentic_patterns.learning`
- **THEN** the process SHALL print JSON that includes kept feedback, the distilled `lessons` string, a `baseline` reply, and an `adapted` reply for `LEARNING_HELD_OUT`

#### Scenario: Baseline then adapt
- **WHEN** `run` executes
- **THEN** it MUST produce a baseline reply using POLICY without lessons, distill lessons from cleaned feedback, and produce an adapted reply using POLICY plus those lessons

#### Scenario: Held-out comparison
- **WHEN** baseline and adapted replies are written
- **THEN** both MUST be produced for the same `LEARNING_HELD_OUT` email (a new ticket, not a memory follow-up)

#### Scenario: Clean before distill
- **WHEN** feedback is ingested
- **THEN** the module MUST drop cases with empty corrections, rating below `MIN_RATING`, or corrections that ask to invent order facts, promise a refund over $50, or blame the customer

#### Scenario: Policy
- **WHEN** a reply is written
- **THEN** it MUST be produced under the shared support `POLICY` (no invented order facts, no refunds over $50 without human approval, no blaming the customer)

#### Scenario: Langfuse tags
- **WHEN** `run` executes
- **THEN** the Langfuse trace MUST include tags `pattern:learning` and `backend:scratch`

### Requirement: Shared learning cases and prompts
The learning emails, supervisor feedback, and distill/reply prompts SHALL live in `packages/shared` so later ports can reuse them.

#### Scenario: Cases are importable
- **WHEN** a lab imports `LEARNING_CASES` and `LEARNING_HELD_OUT` from `sd_agentic_shared.tasks.support_email`
- **THEN** `LEARNING_CASES` MUST be a sequence of at least two items each with `email`, `rating`, and `correction`, and `LEARNING_HELD_OUT` MUST be a support email that is not identical to any case email

#### Scenario: Prompts are importable
- **WHEN** a lab imports learning prompts from `sd_agentic_shared.prompts`
- **THEN** `LEARNING_DISTILL_SYSTEM` and `LEARNING_REPLY_SYSTEM` MUST be defined

### Requirement: README progress for learning scratch
The repository README SHALL record that learning-and-adaptation scratch is done and SHALL document a run command for the module. LangChain and MAF learning cells SHALL remain pending.

#### Scenario: Progress cells
- **WHEN** this change lands
- **THEN** the Progress table row for pattern 9 Learning and adaptation SHALL show scratch as `done` and LangChain and MAF as `pending`

#### Scenario: Run section
- **WHEN** a developer reads the README Run section
- **THEN** they SHALL find `uv run --package sd-agentic-patterns python -m sd_agentic_patterns.learning`
