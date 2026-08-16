---
name: /loop-engineering
id: loop-engineering
category: Workflow
description: Work README objectives in a loop — explore, propose, apply, review, commit — until Progress is done
---

Follow `.cursor/skills/loop-engineering/SKILL.md`.

Work README objectives one OpenSpec change at a time:

**explore → propose → apply → README Progress → review → commit → repeat**

Stop only when the Progress table is complete, the user interrupts, or a blocker is hit.

**Input**: Optional. `one` / `next` = single cycle. An objective name or number = pick that item (still one cycle unless they asked to keep going). Otherwise loop until the README Progress table has no `pending` cells.

**Phases** (read and follow each skill in full when that phase starts):

1. **Pick next** from `README.md` (Progress, Next, Objective, Learning order). Do not ask which item. Do not use a sidecar objectives file.
2. **Explore** — `.cursor/skills/openspec-explore/SKILL.md` (read-only, bounded; then exit)
3. **Propose** — `.cursor/skills/openspec-propose/SKILL.md`
4. **Apply** — `.cursor/skills/openspec-apply-change/SKILL.md`
5. **README Progress** — flip shipped cells (`pending` → `[<file>](<path>)` or the table's existing shipped marker); **create the Progress table from README Objective if none exists**. Do not commit without this.
6. **Review** — `.cursor/skills/openspec-verify-change/SKILL.md` (CRITICAL → fix once and re-verify; still CRITICAL → pause). Stale Progress cells are CRITICAL.
7. **Commit** — implementation + OpenSpec artifacts + README progress; never push unless asked
8. Re-read README and start the next cycle, or stop if complete

Announce each cycle: picked objective, why, remaining pending cells. After each commit, report hash, review outcome, README cells flipped, and the next pick.
