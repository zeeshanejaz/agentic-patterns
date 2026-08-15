## ADDED Requirements

### Requirement: Scratch goal-setting module
The patterns package SHALL expose `sd_agentic_patterns.goal_setting` that sets measurable support goals, drafts a reply, scores progress against those goals, and adjusts within an attempt budget, without importing LangChain or Microsoft Agent Framework.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-patterns python -m sd_agentic_patterns.goal_setting`
- **THEN** the process SHALL print JSON that includes `goals`, per-attempt `scores`, a final `reply`, `attempts_used`, and whether targets were `met`

#### Scenario: Set then monitor
- **WHEN** `run` executes
- **THEN** it MUST set 3 to 5 named goals before drafting, and each attempt MUST record PASS or FAIL per goal

#### Scenario: Adjust on drift
- **WHEN** any goal is FAIL and attempts remain under `MAX_ATTEMPTS`
- **THEN** the module MUST revise the reply toward the failed goals and score again

#### Scenario: Budget stop
- **WHEN** all goals PASS or `MAX_ATTEMPTS` is exhausted
- **THEN** the module MUST stop and report `met` true only if every goal PASSed on the last attempt

#### Scenario: Policy
- **WHEN** a reply is written
- **THEN** it MUST be produced under the shared support `POLICY` (no invented order facts, no refunds over $50 without human approval, no blaming the customer)

#### Scenario: Langfuse tags
- **WHEN** `run` executes
- **THEN** the Langfuse trace MUST include tags `pattern:goal_setting` and `backend:scratch`

### Requirement: Shared SLA and goal prompts
The support SLA and goal-setting / monitor / adjust prompts SHALL live in `packages/shared` so later ports can reuse them.

#### Scenario: SLA is importable
- **WHEN** a lab imports `SUPPORT_SLA` from `sd_agentic_shared.prompts`
- **THEN** it MUST describe standing measurable targets for a support ticket (coverage, policy, acknowledging ids from the email)

#### Scenario: Prompts are importable
- **WHEN** a lab imports goal prompts from `sd_agentic_shared.prompts`
- **THEN** `GOAL_SET_SYSTEM`, `GOAL_MONITOR_SYSTEM`, and `GOAL_ADJUST_SYSTEM` MUST be defined

### Requirement: README progress for goal-setting scratch
The repository README SHALL record that goal-setting-and-monitoring scratch is done and SHALL document a run command for the module. LangChain and MAF goal-setting cells SHALL remain pending.

#### Scenario: Progress cells
- **WHEN** this change lands
- **THEN** the Progress table row for pattern 11 Goal setting and monitoring SHALL show scratch as `done` and LangChain and MAF as `pending`

#### Scenario: Run section
- **WHEN** a developer reads the README Run section
- **THEN** they SHALL find `uv run --package sd-agentic-patterns python -m sd_agentic_patterns.goal_setting`
