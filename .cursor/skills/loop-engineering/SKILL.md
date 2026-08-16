---
name: loop-engineering
description: >-
  Runs an autonomous engineering loop against README objectives: pick the next
  pending item from README.md, plan with openspec-explore, spec with
  openspec-propose, implement with openspec-apply, update README Progress,
  review with openspec-verify-change, then commit. Repeats until README
  Progress has no pending work. Use when the user asks for loop engineering,
  to work through the README, or to run the OpenSpec explore-propose-apply-
  review-commit cycle.
---

# Loop engineering

Work README objectives one OpenSpec change at a time:

**explore → propose → apply → README Progress → review → commit → repeat**

Stop only when README Progress is complete, the user interrupts, or a blocker is hit.

This skill **orchestrates**. For each phase, **read and follow** that skill in full (do not improvise a shorter version):

| Phase | Skill |
|-------|--------|
| Plan | `.cursor/skills/openspec-explore/SKILL.md` |
| Spec | `.cursor/skills/openspec-propose/SKILL.md` |
| Implement | `.cursor/skills/openspec-apply-change/SKILL.md` |
| Review | `.cursor/skills/openspec-verify-change/SKILL.md` |

Pick-next, grounding, and constraints come from **`README.md` only**. Do not use a sidecar objectives file.

## Stance

- **Autonomous by default.** Do not ask which item to do next. Pick it from the README.
- **One change per cycle.** One kebab-case OpenSpec change, one commit.
- **Read-only explore.** Planning must not write application code. Exit explore before propose.
- **Bounded explore.** Investigate README-linked docs and existing code, decide an approach, then proceed. Do not wait for the user unless blocked.
- **Review is a gate.** CRITICAL findings → fix via apply, re-verify. Do not commit with CRITICAL issues.
- **README Progress is a cycle deliverable.** After apply, update Progress before review. Do not commit unless this cycle's shipped work is reflected there.
- **Do not push** unless the user asked.

If the user says "one", "next", or "one cycle", run a single cycle and stop. Otherwise keep looping.

## Outer loop

Copy and keep this updated:

```
Loop progress:
- [ ] Read README + pick next objective
- [ ] Cycle 1: <objective>
- [ ] …
- [ ] README Progress complete
```

1. Read `README.md` (Objective, Progress, Next, Learning order / equivalent, and any constraints). If there is **no Progress table** but Objective lists discrete trackable items, create a table from those items (infer shipped vs pending from the codebase). Do not invent rows the README does not imply.
2. Pick **exactly one** next unit of work using **Pick next** below.
3. Announce:

   ```
   ## Cycle N: <change-name>
   **Picked:** <objective>
   **Why:** <one sentence from README Progress / Next / Learning order>
   **Remaining after this:** <count of pending Progress cells, excluding skip markers>
   ```

4. Run the **inner cycle** below.
5. Re-read `README.md`. If pending work remains, start the next cycle immediately.
6. When every Progress cell is shipped or an explicit skip (`—`, `n/a`, or README-documented skip), stop with a completion summary. Do not invent extra work.

## Pick next

Source of truth: **Progress**, **Next**, **Objective**, and **Learning order** (or similarly named sections) in `README.md`. Re-read them every cycle. Do not trust memory of earlier cycles.

A cell is **pending** if it says `pending` (or equivalent). A cell is **shipped** if it is a markdown link to source, `done`, or another explicit shipped marker. Skip cells marked `—` / `n/a` unless the README says to work them.

Apply the first matching rule:

1. **Honor an unambiguous Next line** that names a single action.
2. **Finish in-flight rows.** Lowest table row that already has some shipped cells and still has pending cells. Prefer one pending lab/column per cycle if the work is non-trivial; do both remaining columns only if they are straightforward mirrors of an existing port in that row.
3. **Else the next fully pending row** in table order, following Learning order / Objective (e.g. implement the primary path first, then ports).
4. **If Next says "either A or B"**, use rules 2–3. Do not pick at random.
5. **Skip what the README marks as skip** (special cases, not-a-port notes, `—` cells).

Change name: kebab-case from the objective (`impl-<thing>`, `port-<thing>-<target>`, or whatever the README's vocabulary suggests).

One OpenSpec change must be reviewable: one capability in one place, or a small set of mirror ports of that same capability. Do not implement two different Progress rows in one cycle.

## Inner cycle

### 1. Explore (plan)

Read and follow `openspec-explore`. Stay read-only.

Ground the pass in whatever `README.md` points at: pattern/docs links, existing implementations to mirror, shared fixtures, and the target package/lab for this pick.

Produce a short plan (intent, files to add/change, non-goals). Then **exit explore**.

### 2. Propose (spec)

Read and follow `openspec-propose`.

The proposal must include:

- Constraints and shared fixtures the README states (do not invent a parallel task)
- A task to update `README.md` Progress / Done / Next / Run when the work lands

Do not skip specs. Apply needs them for review.

### 3. Apply (implement)

Read and follow `openspec-apply-change` for this change. Implement until tasks are done or blocked.

If apply pauses on a design issue, update artifacts, then continue. Do not start a different objective in this cycle.

### 4. Update README Progress (mandatory)

Do this **after apply, before review**.

- If `README.md` has no `## Progress` table but Objective lists trackable items, **create it** from the README (not from a hardcoded template).
- Flip every cell this cycle actually shipped from `pending` to a markdown link to the main module (`[<file>](<path>)`). If the table already uses `done` as its shipped marker, keep that convention.
- Refresh **Done:** and **Next:** if those lines exist.
- Add a Run command if a new module should be invocable.
- Do not mark work shipped that was not implemented.

A cycle that ships code but leaves Progress unchanged is incomplete.

### 5. Review

Read and follow `openspec-verify-change` for this change (spec vs git diff).

- **CRITICAL** → apply fixes (do not commit), then verify **once more**. If still CRITICAL, **pause the loop** and report. Do not start the next objective.
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

**Objective:** <what shipped>
**Commit:** <short hash> <subject>
**Review:** no CRITICAL / N WARNING
**README:** <what Progress cells flipped>
**Next pick:** <following objective or "all objectives done">
```

Then either start cycle N+1 or stop.

## Pause / stop

**Pause** (do not pick a new objective):

- User interrupts or says stop
- Explore cannot decide without a human (missing domain fact, not a code question)
- Apply blocked after a real error
- Review still CRITICAL after the one fix+re-verify pass
- Commit failed and cannot be repaired this cycle

**Stop (success):** README Progress has no `pending` cells (skip markers count as complete).

On pause or completion, list: cycles finished, commits, remaining pending cells, and the blocker if any.

## Constraints

Follow constraints stated in `README.md`. Do not add project-specific policy here.

## Invoking other skills

Read each phase skill file **when that phase starts**. Follow its CLI (`openspec list/status/instructions`), selection rules, and output format. This file only sequences them and supplies pick-next + commit + loop rules.
