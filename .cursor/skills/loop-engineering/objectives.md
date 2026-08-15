# Pick the next README objective

Source of truth: the **Progress** table, **Next** line, and **Learning order** in `README.md`. Re-read them at the start of every cycle. Do not trust memory of earlier cycles.

The **Special labs** table (MCP, OO-Agents) is not part of pick-next or loop completion. Skip it unless the user or the main **Next** line names a special-lab module. **Special labs next** is documentation, not a pick.

## What "done" means

A pattern is complete when:

| Lab | Complete when |
|-----|----------------|
| scratch | `packages/patterns` module exists and the cell is a markdown link to that file |
| LangChain | matching module in `packages/langchain-lab` and the cell links to that file |
| MAF | matching module in `packages/maf-lab` and the cell links to that file |
| MCP (#10) | cell is `—` and Special labs MCP row links the modules — **skip** |
| OO-Agents | Special labs row only; never a Progress column — **skip** |

`pending` = work remaining. Shipped cells are `[<module>.py](<path>)`, never the word `done`. `docs only` in Notes means scratch does not exist yet.

The loop is finished when no cell in the 21-pattern Progress table is `pending`. Special labs `pending` does not keep the loop running.

## Default pick-next (do not ask)

Apply the first matching rule:

1. **Finish 3-way diffs for patterns that already have scratch.** Lowest pattern number where scratch is a source link and LangChain or MAF is `pending`. One cycle ports the missing lab(s). Prefer **one lab per cycle** if the port is non-trivial; both labs in one cycle if they are straightforward mirrors of an existing port (see prompt-chaining).
2. **Else implement the next scratch pattern.** Lowest number with scratch `pending` (skip #10).
3. **Quality/safety wrap.** For #12 exception handling, #13 HITL, #18 guardrails, #19 evaluation: prefer wrapping an existing flow over a standalone clone of every backend. Still land scratch first, then ports, unless the README Next line says otherwise.
4. **Honor an explicit Next line** if it names a single action (e.g. "Planning (#6) from scratch") **and** rule 1 has nothing to port. If Next says "either A or B", use rules 1–2 (ports before new scratch).
5. **Never pick MCP or OO-Agents** as a pattern port (`port-*-mcp`, `port-*-nooa`). **Special labs next** is not a pick-next signal. Only work a special lab when the user asks, or when the main **Next** line names `impl-nooa-lab` / an MCP module.

Examples with the current table shape:

- Routing scratch linked, LangChain pending → `port-routing-langchain` (or langchain+maf if both pending and small)
- Patterns 2–5 scratch linked and fully ported, #6 scratch pending → `impl-planning-scratch`
- Never pick #10 for a 3-way port
- Never pick OO-Agents as a fourth port column

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
| LangChain vs LangGraph | `packages/langchain-lab/README.md` (when LCEL is enough vs a `StateGraph`) |
| Shared task | `packages/shared` (prompts, `support_email`, fake tools) |

## README Progress

Source of truth for pick-next **and** a required edit every cycle. Do this after apply, before review. Do not commit if `git diff README.md` has no Progress change for the cells this cycle shipped.

### Create the table if it is missing

`README.md` must have a `## Progress` section with a markdown table. If that heading or table is absent (new repo, deleted section, or a README that only has prose):

1. Insert the table **after Objective / Labs** (before Setup), using the template below.
2. Fill cells from the **codebase**, not from memory. Shipped cells are markdown links to the main module (`[<module>.py](<path>)`), not the word `done`:
   - scratch: link `packages/patterns/src/sd_agentic_patterns/<module>.py` if it exists
   - LangChain: link the matching module under `packages/langchain-lab`
   - MAF: link the matching module under `packages/maf-lab`
   - otherwise `pending`
   - pattern `#10` is always `—` (not a 3-way port)
   - Special labs: MCP links `demo` / `tool_use` / `server` iff those files exist in `packages/mcp-lab`; OO-Agents links `demo` / `support` iff those files exist in `packages/nooa-lab`; otherwise `pending`. Do not add MCP or OO-Agents columns to the 21-pattern table.
3. Add **Done:** and **Next:** lines under the table.
4. Then continue the cycle (pick / implement / flip what this cycle ships).

Template (21 rows; keep this shape and legend):

```markdown
## Progress

Legend: `[file.py](path)` = shipped · pending · MCP and OO-Agents are special labs (not 3-way ports)

| # | Pattern | scratch | LangChain | MAF | Notes |
|---|---|---|---|---|---|
| 1 | Prompt chaining | pending | pending | pending | |
| 2 | Routing | pending | pending | pending | |
| 3 | Parallelization | pending | pending | pending | |
| 4 | Reflection | pending | pending | pending | |
| 5 | Tool use | pending | pending | pending | |
| 6 | Planning | pending | pending | pending | |
| 7 | Multi-agent collaboration | pending | pending | pending | |
| 8 | Memory management | pending | pending | pending | |
| 9 | Learning and adaptation | pending | pending | pending | |
| 10 | Model Context Protocol | — | — | — | FastMCP lab — see Special labs |
| 11 | Goal setting and monitoring | pending | pending | pending | |
| 12 | Exception handling and recovery | pending | pending | pending | |
| 13 | Human-in-the-loop | pending | pending | pending | |
| 14 | Knowledge retrieval (RAG) | pending | pending | pending | |
| 15 | Inter-agent communication (A2A) | pending | pending | pending | |
| 16 | Resource-aware optimization | pending | pending | pending | |
| 17 | Reasoning techniques | pending | pending | pending | |
| 18 | Guardrails / safety | pending | pending | pending | |
| 19 | Evaluation and monitoring | pending | pending | pending | |
| 20 | Prioritization | pending | pending | pending | |
| 21 | Exploration and discovery | pending | pending | pending | |

**Done:** <one line of what exists>
**Next:** <one line from pick-next>

## Special labs

| Lab | Package | demo | agent loop | extra | Notes |
|---|---|---|---|---|---|
| MCP | `packages/mcp-lab` | pending | pending (`tool_use`) | pending (`server`) | discover/authorize tools via FastMCP |
| OO-Agents | `packages/nooa-lab` | pending | pending (`support`) | — | Python object + CodeAct |

**Special labs next:** <documentation only; not a pick-next signal>
```

### After each cycle (table already exists)

Before review / commit:

- Flip **only** the cells this cycle shipped (`pending` → `[<module>.py](<path-to-that-lab's-file>)`)
- Refresh **Done:** and **Next:**
- Add a Run command if a new module should be invocable
- Keep the legend and MCP `—` row intact
- If this cycle shipped a special-lab module, flip the matching **Special labs** cell to a source link; do not add MCP/OO-Agents columns to the 21-pattern table
- Do not link a lab unless its module exists

Commit gate: if this cycle added or ported a module and the matching Progress cell is still `pending`, the cycle is not done — edit README first.
