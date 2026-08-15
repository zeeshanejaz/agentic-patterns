## Context

Scratch tool use is an OpenAI function-calling loop: model may call `lookup_order` / `create_refund` / `search_docs` (in-memory fakes), we execute via `call_tool`, results go back until a plain reply or `MAX_STEPS = 6`. System text is local to the module and interpolates `POLICY`. MCP already wraps the same tools; this change is LangChain and MAF only.

## Goals / Non-Goals

**Goals:**

- Same tools, same support email, same result shape `{calls, reply}`.
- LangGraph agent ⇄ ToolNode cycle; MAF Agent with tools (loop hidden by the framework — that is the learning point).
- Tags `pattern:tool_use` and `backend:langchain` / `backend:maf`.
- README cells and run commands.

**Non-Goals:**

- Changing scratch, shared tool impls, or the MCP lab.
- Real order/payment APIs.
- New prompts in shared (copy scratch's SYSTEM string).

## Decisions

1. **Both labs in one change.** Bind the same three functions; two modules.

2. **LangChain: `StructuredTool.from_function` + `ToolNode` + `tools_condition`.** Extract `ToolCallRecord`s from the resulting messages. `recursion_limit` sized for six model turns; on overflow reply `Stopped: too many tool steps.`

   Alternative: hand-rolled LCEL loop copying scratch — rejected; would hide nothing LangGraph-specific.

3. **MAF: `Agent(..., tools=[lookup_order, create_refund, search_docs])`.** `FunctionMiddleware` records name/arguments/result. Reply is `AgentResponse.text`. Do not reimplement the tool loop in Python.

4. **SYSTEM prompt** copied from scratch (POLICY + tool-use instructions), not MCP's `SUPPORT_AGENT_PROMPT`.

## Risks / Trade-offs

- [MAF max iterations default is 100] → demo emails finish in a few steps; LangChain still caps at 6.
- [create_refund amount types] → keep shared function signatures.

## Migration Plan

Add two modules and README lines. Rollback is delete + revert README.

## Open Questions

None.
