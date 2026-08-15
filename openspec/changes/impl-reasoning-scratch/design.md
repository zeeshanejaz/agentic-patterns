## Context

CoT is a prompt; ToT/debate need graphs. Scratch: N=2 CoT JSON samples, prefer shared claims, never invent tracking / $89 refunds.

## Goals / Non-Goals

**Goals:** Module `reasoning`, N=2, print samples + chosen reply. Tags `pattern:reasoning`. README shipped.

**Non-Goals:** Ports. Full ToT. Fine-tuning.

## Decisions

1. JSON `{steps: [str], reply: str}`. Parse fail → one-step fallback.
2. N=2 self-consistency; if replies differ, keep sample 1 but record both.
3. POLICY in the reasoning prompt.

## Risks / Trade-offs

- [Looks like draft] → `steps` are the teaching surface.

## Migration Plan

Add module + prompt + README.

## Open Questions

None.
