## ADDED Requirements

### Requirement: LangChain goal-setting module
The langchain-lab package SHALL expose `sd_agentic_langchain.goal_setting` that sets measurable support goals, scores progress, and adjusts within `MAX_ATTEMPTS` via LangGraph.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-langchain python -m sd_agentic_langchain.goal_setting`
- **THEN** the process SHALL print JSON that includes `goals`, per-attempt `scores`, a final `reply`, `attempts_used`, and whether targets were `met`

#### Scenario: Graph owns the cycle
- **WHEN** the module runs
- **THEN** it MUST use a LangGraph `StateGraph` with set-goals, adjust, and monitor nodes, and MUST NOT implement the attempt loop as a Python `while` around LCEL only

#### Scenario: Adjust on drift
- **WHEN** any goal is FAIL and attempts remain under `MAX_ATTEMPTS`
- **THEN** the graph MUST continue to an adjust node and score again

#### Scenario: Shared prompts
- **WHEN** the module runs
- **THEN** it MUST use `SUPPORT_EMAIL` and `SUPPORT_SLA` / `GOAL_SET_SYSTEM` / `GOAL_MONITOR_SYSTEM` / `GOAL_ADJUST_SYSTEM` from shared packages

#### Scenario: Langfuse tags
- **WHEN** `run` executes
- **THEN** the Langfuse trace MUST include tags `pattern:goal_setting` and `backend:langchain`

### Requirement: MAF goal-setting module
The maf-lab package SHALL expose `sd_agentic_maf.goal_setting` that runs the same set → adjust → monitor flow with MAF Agents and returns the same result shape.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-maf python -m sd_agentic_maf.goal_setting`
- **THEN** the process SHALL print JSON that includes `goals`, attempts with scores, `reply`, `attempts_used`, and `met`

#### Scenario: Agents own LLM steps
- **WHEN** the module sets goals, adjusts a reply, or monitors scores
- **THEN** it MUST use MAF Agent invocation rather than a hand-rolled OpenAI `complete()` helper

#### Scenario: Observability
- **WHEN** `run` executes
- **THEN** an OTEL span named `pattern.goal_setting` MUST be created with attributes identifying `pattern` as `goal_setting` and `backend` as `maf`

### Requirement: Patterns package stays framework-free
`packages/patterns` MUST NOT import LangChain or Microsoft Agent Framework as part of this change.

#### Scenario: Scratch unchanged
- **WHEN** this change is implemented
- **THEN** scratch goal setting MUST remain unmodified

### Requirement: README progress for goal-setting ports
The repository README SHALL record that goal-setting-and-monitoring LangChain and MAF are done and SHALL document run commands for both modules.

#### Scenario: Progress cells
- **WHEN** the ports land
- **THEN** the Progress table row for pattern 11 Goal setting and monitoring SHALL show scratch, LangChain, and MAF as `done`

#### Scenario: Run section
- **WHEN** a developer reads the README Run section
- **THEN** they SHALL find `uv run` commands for `sd_agentic_langchain.goal_setting` and `sd_agentic_maf.goal_setting`
