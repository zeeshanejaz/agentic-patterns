# Pick the next README objective

Source of truth: the **Progress** table, **Next** line, and **Learning order** in `README.md`. Re-read them at the start of every cycle. Do not trust memory of earlier cycles.

## What "done" means

A pattern is complete when:

| Lab | Complete when |
|-----|----------------|
| scratch | `packages/patterns` module exists and the cell is `done` |
| LangChain | matching module in `packages/langchain-lab` and cell is `done` |
| MAF | matching module in `packages/maf-lab` and cell is `done` |
| MCP (#10) | cell is `—` and notes say the FastMCP lab is done — **skip** |

`pending` = work remaining. `docs only` in Notes means scratch does not exist yet.

The loop is finished when no cell is `pending`.

## Default pick-next (do not ask)

Apply the first matching rule:

1. **Finish 3-way diffs for patterns that already have scratch.** Lowest pattern number where scratch is `done` and LangChain or MAF is `pending`. One cycle ports the missing lab(s). Prefer **one lab per cycle** if the port is non-trivial; both labs in one cycle if they are straightforward mirrors of an existing port (see prompt-chaining).
2. **Else implement the next scratch pattern.** Lowest number with scratch `pending` (skip #10).
3. **Quality/safety wrap.** For #12 exception handling, #13 HITL, #18 guardrails, #19 evaluation: prefer wrapping an existing flow over a standalone clone of every backend. Still land scratch first, then ports, unless the README Next line says otherwise.
4. **Honor an explicit Next line** if it names a single action (e.g. "Planning (#6) from scratch") **and** rule 1 has nothing to port. If Next says "either A or B", use rules 1–2 (ports before new scratch).

Examples with the current table shape:

- Routing scratch done, LangChain pending → `port-routing-langchain` (or langchain+maf if both pending and small)
- Patterns 2–5 scratch done and fully ported, #6 scratch pending → `impl-planning-scratch`
- Never pick #10 for a 3-way port

## Cycle size

One OpenSpec change must be reviewable:

- **Scratch:** one pattern in `packages/patterns` (plus shared prompts/tools only if required)
- **Port:** one pattern into one lab, or both remaining labs if the second is a near-copy
- **README:** Progress / Done / Next / Run updates for what this change actually shipped

Do not implement two different pattern numbers in one cycle.

## Change names

`impl-<pattern>-scratch` · `port-<pattern>-langchain` · `port-<pattern>-maf` · `port-<pattern>-langchain-maf`

Use the README pattern slug (`routing`, `parallelization`, `planning`, `tool-use`, …).

## Grounding files

| Need | Where |
|------|--------|
| Pattern intent | `docs/agentic-design-patterns.md` |
| Discussion | `docs/agentic-design-patterns-docs/pattern-discussion/<slug>.md` |
| Scratch example | `packages/patterns/src/sd_agentic_patterns/` |
| Port example | `packages/langchain-lab/.../prompt_chaining.py`, `packages/maf-lab/.../prompt_chaining.py` |
| Shared task | `packages/shared` (prompts, `support_email`, fake tools) |

## README edits in the same change

After implementation, before commit:

- Flip shipped cells from `pending` to `done`
- Refresh **Done:** and **Next:**
- Add a Run command if a new module should be invocable
- Keep the legend and MCP `—` row intact
