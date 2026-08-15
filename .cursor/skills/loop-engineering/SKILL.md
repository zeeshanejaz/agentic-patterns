---
name: loop-engineering
description: >-
  Runs an autonomous engineering loop against README objectives: pick the next
  pending agentic pattern, plan with openspec-explore, spec with openspec-propose,
  implement with openspec-apply, review with openspec-verify-change, then commit.
  Repeats until the README Progress table is complete. Use when the user asks for
  loop engineering, to work through the README, keep implementing patterns, or
  run the OpenSpec explore-propose-apply-review-commit cycle.
---

# Loop engineering

Work README objectives one OpenSpec change at a time:

**explore → propose → apply → README Progress → review → commit → repeat**

Stop only when the Progress table is complete, the user interrupts, or a blocker is hit.

This skill **orchestrates**. For each phase, **read and follow** that skill in full (do not improvise a shorter version):

| Phase | Skill |
|-------|--------|
| Plan | `.cursor/skills/openspec-explore/SKILL.md` |
| Spec | `.cursor/skills/openspec-propose/SKILL.md` |
| Implement | `.cursor/skills/openspec-apply-change/SKILL.md` |
| Progress | [objectives.md](objectives.md) § README Progress (create table if missing) |
| Review | `.cursor/skills/openspec-verify-change/SKILL.md` |

How to pick the next objective: [objectives.md](objectives.md).

## Stance

- **Autonomous by default.** Do not ask which pattern to do next. Pick it from the README.
- **One change per cycle.** One kebab-case OpenSpec change, one commit.
- **Read-only explore.** Planning must not write application code. Exit explore before propose.
- **Bounded explore.** Investigate the pattern docs and existing labs, decide an approach, then proceed. Do not wait for the user unless blocked.
- **Review is a gate.** CRITICAL findings → fix via apply, re-verify. Do not commit with CRITICAL issues.
- **README Progress is a cycle deliverable.** After apply, update the Progress table before review. If the table is missing, create it. Do not commit unless this cycle's cells flipped.
- **Do not push** unless the user asked.

If the user says "one", "next", or "one cycle", run a single cycle and stop. Otherwise keep looping.

## Outer loop

Copy and keep this updated:

```
Loop progress:
- [ ] Read README + pick next objective
- [ ] Cycle 1: <objective>
- [ ] …
- [ ] README Progress table complete
```

1. Read `README.md` (Objective, Labs, Progress, Next, Learning order). If there is **no Progress table**, create one now using the template in [objectives.md](objectives.md) (infer `done` from modules that already exist). Then pick.
2. Follow [objectives.md](objectives.md) to pick **exactly one** next unit of work.
3. Announce:

   ```
   ## Cycle N: <change-name>
   **Picked:** Pattern #<k> <name> → <scratch | port langchain | port maf | port langchain+maf>
   **Why:** <one sentence from the pick-next rules>
   **Remaining after this:** <count of pending cells in the 21-pattern table, excluding MCP "—" and Special labs>
   ```

4. Run the **inner cycle** below.
5. Re-read `README.md`. If pending work remains, start the next cycle immediately.
6. When every Progress cell is `done` or `—`, stop with a completion summary. Do not invent extra work.

## Inner cycle

### 1. Explore (plan)

Read and follow `openspec-explore`. Stay read-only.

Ground the pass in:

- `docs/agentic-design-patterns.md` and `docs/agentic-design-patterns-docs/pattern-discussion/` for this pattern
- Existing scratch impl in `packages/patterns` (and a prior port, if this is a port)
- `packages/shared` prompts, sample emails, fake tools
- The sibling lab you are targeting (`langchain-lab` / `maf-lab`)

Produce a short plan (intent, files to add/change, non-goals). Then **exit explore**.

### 2. Propose (spec)

Read and follow `openspec-propose`.

Change name: kebab-case, e.g. `impl-planning-scratch`, `port-routing-langchain`.

The proposal must include:

- Same shared task (fake support inbox); same prompts/sample emails from `packages/shared`
- `packages/patterns` must not import LangChain or Microsoft Agent Framework
- Ports use the **same module name** as scratch
- Langfuse tags `pattern:*` and `backend:scratch` / `langchain` / `maf` (or `mcp`)
- Quality/safety patterns (exception handling, HITL, guardrails, evaluation) wrap existing flows when that fits
- A task to update `README.md` Progress / Done / Next / Run when the work lands

Do not skip specs. Apply needs them for review.

### 3. Apply (implement)

Read and follow `openspec-apply-change` for this change. Implement until tasks are done or blocked.

If apply pauses on a design issue, update artifacts, then continue. Do not start a different pattern in this cycle.

### 4. Update README Progress (mandatory)

Do this **after apply, before review**. Follow [objectives.md](objectives.md) § README Progress.

- If `README.md` has no `## Progress` table, **create it**.
- Flip every cell this cycle actually shipped from `pending` to `done`.
- Refresh **Done:**, **Next:**, and **Run** for what landed.
- Leave MCP `#10` as `—`. Do not add MCP or OO-Agents columns. Flip Special labs cells only if this cycle shipped that module.
- Do not mark labs done that were not implemented.

A cycle that ships code but leaves Progress unchanged is incomplete.

### 5. Review

Read and follow `openspec-verify-change` for this change (spec vs git diff).

- **CRITICAL** → apply fixes (do not commit), then verify **once more**. If still CRITICAL, **pause the loop** and report. Do not start the next pattern.
- Missing or stale Progress cells for this cycle are **CRITICAL**.
- **WARNING / SUGGESTION** → fix only if cheap and still in scope; otherwise note them and continue.
- Do not expand into unrelated refactors.

### 6. Commit

Only after review has no CRITICAL issues **and** `git diff README.md` shows the Progress update for this cycle.

Include implementation, OpenSpec artifacts, and README progress updates. Exclude secrets (`.env`, credentials).

If README is unchanged, stop: go back to step 4. Do not commit.

Follow the git commit protocol:

1. `git status` (untracked + staged)
2. `git diff` (staged + unstaged)
3. `git log` (recent messages — match style)
4. Stage relevant files; commit with a message that says **why** (1–2 sentences)
5. `git status` to confirm success

Never update git config, never `--no-verify`, never force-push, never push unless asked.

If the hook fails, fix and make a **new** commit. Do not amend unless the hook only touched files from a commit you just created in this cycle and it was not pushed.

### 7. Cycle report

```
## Cycle N complete: <change-name>

**Objective:** <pattern / lab>
**Commit:** <short hash> <subject>
**Review:** no CRITICAL / N WARNING
**README:** <what Progress cells flipped to done>
**Next pick:** <following objective or "all objectives done">
```

Then either start cycle N+1 or stop.

## Pause / stop

**Pause** (do not pick a new pattern):

- User interrupts or says stop
- Explore cannot decide without a human (missing domain fact, not a code question)
- Apply blocked after a real error
- Review still CRITICAL after the one fix+re-verify pass
- Commit failed and cannot be repaired this cycle

**Stop (success):** the 21-pattern Progress table has no `pending` cells (MCP `—` is complete). Special labs `pending` does not block this.

On pause or completion, list: cycles finished, commits, remaining pending cells, and the blocker if any.

## Constraints (do not violate)

From `README.md`:

- Patterns are the unit of learning; scratch first, then port
- Shared task: do not invent order facts, do not promise refunds over $50, do not blame the customer
- Tools (`lookup_order`, `create_refund`, `search_docs`) are in-memory fakes
- MCP is the integration layer under tool use, not a fourth rewrite of every pattern
- OO-Agents is the object-oriented harness (code as action), not a fifth rewrite of every pattern

## Invoking other skills

Read each phase skill file **when that phase starts**. Follow its CLI (`openspec list/status/instructions`), selection rules, and output format. This file only sequences them and supplies pick-next + commit + loop rules.
