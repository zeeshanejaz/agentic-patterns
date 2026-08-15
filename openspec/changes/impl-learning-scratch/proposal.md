## Why

Learning and adaptation (#9) is the next scratch pattern: memory (#8) is implemented and ported. Scratch must exist before LangChain/MAF ports so the loop (collect feedback → clean → update prompts/examples → A/B) is invented here, not hidden by a framework memory store.

## What Changes

- Add `sd_agentic_patterns.learning`: baseline replies on a small support batch, ingest simulated supervisor ratings and corrections, distill a compact lessons block, then re-run including a held-out email and print baseline vs adapted.
- Add shared learning cases (emails + feedback) and distill/reply prompts in `packages/shared` so later ports reuse them.
- Do not invent order facts; do not promise refunds over $50. Learning updates the prompt, not model weights. Feedback that would violate POLICY is dropped.
- Tag traces `pattern:learning` and `backend:scratch`.
- Update README Progress (learning scratch → done; LangChain/MAF stay pending), Done/Next, and Run commands.

## Capabilities

### New Capabilities

- `learning-scratch`: From-scratch learning and adaptation on the shared support-inbox task: collect corrections, distill lessons into the prompt, A/B baseline vs adapted.

### Modified Capabilities

- (none)

## Impact

- New module: `packages/patterns/src/sd_agentic_patterns/learning.py`.
- New prompts and learning cases in `packages/shared`.
- README Progress / Done / Next / Run.
- `packages/patterns` still must not import LangChain or MAF. No ports this change.
