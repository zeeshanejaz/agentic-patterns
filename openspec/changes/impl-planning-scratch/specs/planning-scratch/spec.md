## ADDED Requirements

### Requirement: Scratch planning module
The patterns package SHALL expose `sd_agentic_patterns.planning` that decomposes a support email into a step plan with dependencies, executes ready steps, and produces a customer reply without importing LangChain or Microsoft Agent Framework.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-patterns python -m sd_agentic_patterns.planning`
- **THEN** the process SHALL print JSON that includes a `plan` (with `goal` and `steps`), `execution` results per step, `replans`, and `reply` for `SUPPORT_EMAIL`

#### Scenario: Plan has a dependency graph
- **WHEN** a plan is produced
- **THEN** each step MUST have an `id`, an `instruction`, optional `tool` / `arguments`, and `depends_on` listing prior step ids

#### Scenario: Tool steps use shared fakes
- **WHEN** a step names `lookup_order`, `create_refund`, or `search_docs`
- **THEN** the executor MUST call `sd_agentic_shared.tools.call_tool` with that name and arguments (not a live API)

#### Scenario: Replan on blocked checkpoint
- **WHEN** a tool result indicates the order was not found or a refund was refused
- **THEN** the module MUST replan remaining steps at most once before continuing

#### Scenario: Policy
- **WHEN** the final reply is written
- **THEN** it MUST be produced under the shared support `POLICY` (no invented order facts, no refunds over $50 without human approval, no blaming the customer)

#### Scenario: Langfuse tags
- **WHEN** `run` executes
- **THEN** the Langfuse trace MUST include tags `pattern:planning` and `backend:scratch`

### Requirement: Shared planning prompts
Planner, step, and replan prompts SHALL live in `sd_agentic_shared.prompts` so later ports can reuse them.

#### Scenario: Prompts are importable
- **WHEN** a lab imports planning prompts from `sd_agentic_shared.prompts`
- **THEN** `PLAN_SYSTEM`, `PLAN_REPAIR_SYSTEM`, `PLAN_STEP_SYSTEM`, and `PLAN_REPLAN_SYSTEM` MUST be defined

### Requirement: README progress for planning scratch
The repository README SHALL record that planning scratch is done and SHALL document a run command for the module. LangChain and MAF planning cells SHALL remain pending.

#### Scenario: Progress cells
- **WHEN** this change lands
- **THEN** the Progress table row for pattern 6 Planning SHALL show scratch as `done` and LangChain and MAF as `pending`

#### Scenario: Run section
- **WHEN** a developer reads the README Run section
- **THEN** they SHALL find `uv run --package sd-agentic-patterns python -m sd_agentic_patterns.planning`
