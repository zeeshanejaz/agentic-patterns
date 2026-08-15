## Context

The pattern is specialized agents under a coordinator, sharing structured memory and acceptance criteria. Routing already sends an email to **one** handler. Parallelization runs independent extractors with no coordinator. Multi-agent must keep a named roster, a shared notes board, and a writer that only sees those notes.

The shared task is still the fake support inbox. `SUPPORT_EMAIL` mixes billing, shipping, and a $89 refund ask, so a coordinator should dispatch more than one specialist.

## Goals / Non-Goals

**Goals:**

- Scratch module `multi_agent` with Langfuse tags `pattern:multi_agent`, `backend:scratch`.
- Coordinator emits JSON assignments from a fixed roster: `billing`, `shipping`, `policy`.
- Specialists write team notes onto a shared board (not customer emails).
- Coordinator may dispatch one extra round (`MAX_ROUNDS = 2`) after reading the board.
- Writer produces the customer reply from the board under POLICY.
- Shared prompts for coordinator, specialists, review, and writer.
- README scratch cell done; Next points at multi-agent ports.

**Non-Goals:**

- LangChain / MAF ports.
- Peer-to-peer A2A messaging (pattern #15).
- Binding fake tools onto specialists (tool use / planning already cover that).
- MagenticBuilder / group chat frameworks.
- Changing existing fake tool data.

## Decisions

1. **Coordinator-worker, not a peer mesh.** The teaching surface is a supervisor plus specialists plus a writer. A2A topologies wait for pattern 15.

2. **Fixed roster** (`billing`, `shipping`, `policy`) so the coordinator chooses who runs, unlike routing (exactly one) and parallelization (always all extractors). Unknown agent names are dropped. If JSON parse fails, assign all three with a generic instruction.

3. **Shared notes board** is an in-memory list of `{agent, text}`. Each specialist sees the email plus notes so far. Writer sees only the board (plus the original email for addressing), not a private specialist transcript.

4. **Second coordinator round** after specialists run: output `DONE` or more assignments. Cap at `MAX_ROUNDS = 2` so the loop cannot fan out forever.

5. **No tools in this pattern.** Specialists reason from the email and POLICY. Distinguishes collaboration (roles + shared memory) from planning/tool use.

## Risks / Trade-offs

- [Looks like routing] → coordinator may assign several specialists; writer merges notes.
- [Looks like parallelization] → coordinator chooses the subset; optional second round; notes are a shared board.
- [JSON fragility] → repair is skip: fallback assigns all three specialists.
- [Writer invents facts] → prompt forbids it; POLICY interpolated.

## Migration Plan

Add module + prompts + README. Rollback is delete those.

## Open Questions

None.
