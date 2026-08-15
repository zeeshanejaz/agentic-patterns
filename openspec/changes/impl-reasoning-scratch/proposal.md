## Why

Reasoning techniques (#17) is next: resource-aware is ported. Scratch should invent CoT (and a tiny self-consistency vote) before ToT graphs hide it.

## What Changes

- Add `sd_agentic_patterns.reasoning`: two CoT samples on `SUPPORT_EMAIL`, each `{steps, reply}`, pick the majority-ish reply under POLICY.
- Shared `REASONING_SYSTEM`. Tags `pattern:reasoning`. README scratch shipped.

## Capabilities

### New Capabilities

- `reasoning-scratch`: From-scratch CoT + self-consistency on the support inbox.

### Modified Capabilities

- (none)

## Impact

- New module, prompt, README. No ports.
