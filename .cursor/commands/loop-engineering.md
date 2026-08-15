---
name: /loop-engineering
id: loop-engineering
category: Workflow
description: Work README objectives in a loop — explore, propose, apply, review, commit — until Progress is done
---

Follow `.cursor/skills/loop-engineering/SKILL.md` and `.cursor/skills/loop-engineering/objectives.md`.

Work README objectives one OpenSpec change at a time:

**explore → propose → apply → review → commit → repeat**

Stop only when the Progress table is complete, the user interrupts, or a blocker is hit.

**Input**: Optional. `one` / `next` = single cycle. A pattern name or number = pick that objective (still one cycle unless they asked to keep going). Otherwise loop until the README Progress table has no `pending` cells.

**Phases** (read and follow each skill in full when that phase starts):

1. **Pick next** from `README.md` using `objectives.md`. Do not ask which pattern.
2. **Explore** — `.cursor/skills/openspec-explore/SKILL.md` (read-only, bounded; then exit)
3. **Propose** — `.cursor/skills/openspec-propose/SKILL.md`
4. **Apply** — `.cursor/skills/openspec-apply-change/SKILL.md`
5. **Review** — `.cursor/skills/openspec-verify-change/SKILL.md` (CRITICAL → fix once and re-verify; still CRITICAL → pause)
6. **Commit** — implementation + OpenSpec artifacts + README progress; never push unless asked
7. Re-read README and start the next cycle, or stop if complete

Announce each cycle: picked objective, why, remaining pending cells. After each commit, report hash, review outcome, README cells flipped, and the next pick.
