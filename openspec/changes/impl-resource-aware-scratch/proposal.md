## Why

Resource-aware optimization (#16) is the next scratch pattern: A2A is implemented and ported. Scratch must invent cheap-vs-expensive routing before LCEL routers hide it.

## What Changes

- Add `sd_agentic_patterns.resource_aware`: classify support-email complexity, send simple tickets to a cheap/short path and mixed/high-stakes tickets to an expensive draft, record a fake cost.
- Shared classify + cheap/expensive prompts. Same sample emails. Tags `pattern:resource_aware`, `backend:scratch`.
- README Progress / Done / Next / Run.

## Capabilities

### New Capabilities

- `resource-aware-scratch`: From-scratch cheap/expensive routing on the shared support-inbox task.

### Modified Capabilities

- (none)

## Impact

- New module `resource_aware.py`, prompts, README. No ports. Patterns stay framework-free.
