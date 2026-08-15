## Why

Goal setting and monitoring (#11) is the next scratch pattern: learning (#9) is implemented and ported, and MCP (#10) is a special lab. Scratch must exist before LangChain/MAF ports so the loop (set measurable goals → draft → score vs targets → adjust if drifting within a budget) is invented here.

## What Changes

- Add `sd_agentic_patterns.goal_setting`: set measurable support goals from a shared SLA, draft a reply, monitor PASS/FAIL per goal, and revise while the attempt budget remains if any goal is failing.
- Add shared SLA/goals prompts in `packages/shared` so later ports reuse them. Use the existing `SUPPORT_EMAIL` task.
- Do not invent order facts; do not promise refunds over $50. Goals are named KPIs, not a planning DAG and not a single reflection critic.
- Tag traces `pattern:goal_setting` and `backend:scratch`.
- Update README Progress (goal-setting scratch → done; LangChain/MAF stay pending), Done/Next, and Run commands.

## Capabilities

### New Capabilities

- `goal-setting-scratch`: From-scratch goal setting and monitoring on the shared support-inbox task: set KPIs, score progress, adjust within a budget.

### Modified Capabilities

- (none)

## Impact

- New module: `packages/patterns/src/sd_agentic_patterns/goal_setting.py`.
- New prompts (and optional SLA text) in `packages/shared`.
- README Progress / Done / Next / Run.
- `packages/patterns` still must not import LangChain or MAF. No ports this change.
