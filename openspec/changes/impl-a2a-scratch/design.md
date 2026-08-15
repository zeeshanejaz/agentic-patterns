## Context

A2A is structured messages (ids, expiry, replies) between agents. Multi-agent (#7) uses a shared notes list. This lab is a **mailbox**, not a whiteboard.

## Goals / Non-Goals

**Goals:**

- Module `a2a`, tags `pattern:a2a`, `backend:scratch`.
- Envelope `{id, sender, recipient, body, ttl, in_reply_to}`. Bus delivers only if `ttl >= turn`. Cap `MAX_MESSAGES = 8`.
- Coordinator posts to billing and shipping; they reply on the bus; writer reads delivered mail and writes the customer reply under POLICY.
- README scratch shipped; Next = A2A ports.

**Non-Goals:**

- Ports. Real network/auth. Peer mesh. Changing multi_agent.py.

## Decisions

1. **In-process list bus.** Teaching surface is envelope metadata, not sockets.
2. **Reuse specialist system prompts.** New `A2A_MESSAGE_SYSTEM` tells agents to output a short bus note, not a customer email.
3. **TTL in turns.** Coordinator messages ttl=2; replies ttl=1.

## Risks / Trade-offs

- [Looks like multi-agent] → evidence is `envelopes` with ids/ttl, not `notes`.
- [Loop storms] → MAX_MESSAGES.

## Migration Plan

Add module + optional prompt + README.

## Open Questions

None.
