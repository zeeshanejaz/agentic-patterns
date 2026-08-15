---
name: openspec-verify-change
description: >-
  Review code changes against an OpenSpec specification. Looks up the change's
  delta specs (and related proposal/design/tasks), compares them to the actual
  git diff, and reports whether implementation matches the spec. Use when the
  user asks for a code review, spec review, to verify a change, to check if
  implementation matches the spec, or before archiving an OpenSpec change.
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.9.0"
---

Review whether the code changes match the OpenSpec specification for a change.

This is a **read-only review**. Do not edit application code, mark tasks done, or archive unless the user explicitly asks after the report.

**Store selection:** If the user names a store (a store is a standalone OpenSpec repo registered on this machine) or the work lives in one, run `openspec store list --json` to discover registered store ids, then pass `--store <id>` on the commands that read specs and changes (`status`, `instructions`, `list`, `show`, `validate`). Once selected, treat `--store <id>` as sticky for the rest of the workflow. Without a store, commands act on the nearest local `openspec/` root.

**Input**: Optionally specify a change name. If omitted, infer from conversation context. If vague or ambiguous you MUST prompt for available changes.

**Steps**

1. **Select the change**

   If a name is provided, use it. Otherwise:
   - Infer from conversation context if the user mentioned a change
   - Auto-select if only one active change exists
   - If ambiguous, run `openspec list --json` to get available changes and use the **AskUserQuestion tool** to let the user select

   When prompting, show changes that have implementation tasks (tasks artifact exists).
   Include the schema used for each change if available.
   Mark changes with incomplete tasks as "(In Progress)".

   Always announce: "Using change: <name>" and how to override (e.g., `/opsx:verify <other>`).

   **Named spec without a change:** If the user names a capability (not a change), look up `openspec/specs/<capability>/spec.md` (or the path from `openspec show <capability>` / status JSON). Review the git diff against that main spec. Skip task-completion checks that only apply to a change.

2. **Check status to understand the schema**
   ```bash
   openspec status --change "<name>" --json
   ```
   Parse the JSON to understand:
   - `schemaName`: The workflow being used (e.g., "spec-driven")
   - `planningHome`, `changeRoot`, `artifactPaths`, and `actionContext`: path and scope context
   - Which artifacts exist for this change

   If status reports `actionContext.mode: "workspace-planning"` and you cannot resolve readable artifact paths, explain the limitation and STOP.

3. **Get planning context and load artifacts**

   ```bash
   openspec instructions apply --change "<name>" --json
   ```

   This returns the change directory and `contextFiles` (artifact ID -> array of concrete file paths). Read **all** available artifacts from `contextFiles`:
   - **specs** — source of truth for behavior (requirements + scenarios)
   - **proposal** — intent, scope, and non-goals
   - **design** — technical decisions (if present)
   - **tasks** — implementation checklist

   If `contextFiles.specs` is empty, also check `artifactPaths.specs.existingOutputPaths` from status JSON.

4. **Collect the code changes under review**

   Default to **branch changes** (committed + staged + unstaged vs the merge-base with the default/base branch).

   Override when the user asks:
   - uncommitted / working tree / not-yet-committed → uncommitted changes only
   - a specific PR or branch → review that target (check it out only if needed and safe)
   - named files → those files plus their diff

   Gather:
   ```bash
   git status --short
   git diff
   git diff --cached
   git diff <base>...HEAD
   git log --oneline <base>...HEAD
   ```
   Use the repository's actual default branch as `<base>` unless the user named one.

   If the diff is empty, say so and still check whether spec requirements appear implemented in the current tree (the work may already be committed on the base branch).

5. **Initialize verification report structure**

   Create a report structure with three dimensions:
   - **Completeness**: Track tasks and spec coverage
   - **Correctness**: Track requirement implementation and scenario coverage against the **diff and code**
   - **Coherence**: Track design adherence, scope, and pattern consistency

   Each dimension can have CRITICAL, WARNING, or SUGGESTION issues.

6. **Verify Completeness**

   **Task Completion**:
   - If `contextFiles.tasks` exists, read every file path in it
   - Parse checkboxes: `- [ ]` (incomplete) vs `- [x]` (complete)
   - Count complete vs total tasks
   - If incomplete tasks exist:
     - Add CRITICAL issue for each incomplete task
     - Recommendation: "Complete task: <description>" or "Mark as done if already implemented"

   **Spec Coverage**:
   - If delta specs exist in `contextFiles.specs` (or main spec, if reviewing a capability):
     - Extract all requirements (marked with `### Requirement:`)
     - For ADDED/MODIFIED requirements, look for implementation in the **diff first**, then the surrounding code
     - For REMOVED requirements, confirm the behavior is actually gone
     - If a requirement appears unimplemented:
       - Add CRITICAL issue: "Requirement not found: <requirement name>"
       - Recommendation: "Implement requirement X: <description>"

7. **Verify Correctness**

   **Requirement Implementation Mapping**:
   - For each requirement from the spec:
     - Map it to evidence in the diff (preferred) or existing code
     - Note file paths and line ranges
     - Assess if implementation matches requirement intent (`SHALL`/`MUST`)
     - If divergence detected:
       - Add WARNING: "Implementation may diverge from spec: <details>"
       - Recommendation: "Review `<file>:<lines>` against requirement X"

   **Scenario Coverage**:
   - For each scenario (marked with `#### Scenario:`):
     - Check GIVEN/WHEN/THEN (or WHEN/THEN) conditions in the changed code
     - Check whether tests exist covering the scenario
     - If a scenario appears uncovered:
       - Add WARNING: "Scenario not covered: <scenario name>"
       - Recommendation: "Add test or implementation for scenario: <description>"

   **Scope (code review)**:
   - Compare the diff to proposal scope / non-goals and to the spec deltas
   - Extra behavior in the diff that the spec does not ask for → WARNING (scope creep)
   - Spec behavior with no corresponding change → CRITICAL or WARNING (see completeness)
   - Changes that only update OpenSpec artifacts with no code → note that; do not treat as implementation

8. **Verify Coherence**

   **Design Adherence**:
   - If `contextFiles.design` exists:
     - Extract key decisions (look for sections like "Decision:", "Approach:", "Architecture:")
     - Verify implementation follows those decisions
     - If contradiction detected:
       - Add WARNING: "Design decision not followed: <decision>"
       - Recommendation: "Update implementation or revise design.md to match reality"
   - If no design.md: Skip design adherence check, note "No design.md to verify against"

   **Code Pattern Consistency**:
   - Review **new/changed** code for consistency with project patterns
   - Check file naming, directory structure, coding style
   - If significant deviations found:
     - Add SUGGESTION: "Code pattern deviation: <details>"
     - Recommendation: "Consider following project pattern: <example>"

9. **Generate Verification Report**

   **Summary Scorecard**:
   ```markdown
   ## Verification Report: <change-name>

   **Change:** <name>
   **Schema:** <schema-name>
   **Spec source:** <delta spec paths or main spec path>
   **Diff:** <branch changes | uncommitted | named files> vs <base>

   ### Summary
   | Dimension    | Status            |
   |--------------|-------------------|
   | Completeness | X/Y tasks, N reqs |
   | Correctness  | M/N reqs covered  |
   | Coherence    | Followed/Issues   |
   ```

   Include a **Requirement mapping** table before issues:

   | Requirement | Spec | Evidence | Verdict |
   |-------------|------|----------|---------|
   | <name> | ADDED/MODIFIED/REMOVED | `file.ts:123` or "not found" | Match / Diverge / Missing |

   **Issues by Priority**:

   1. **CRITICAL** (Must fix before archive):
      - Incomplete tasks
      - Missing requirement implementations
      - Each with specific, actionable recommendation

   2. **WARNING** (Should fix):
      - Spec/design divergences
      - Missing scenario coverage
      - Scope creep
      - Each with specific recommendation

   3. **SUGGESTION** (Nice to fix):
      - Pattern inconsistencies
      - Minor improvements
      - Each with specific recommendation

   **Final Assessment**:
   - If CRITICAL issues: "X critical issue(s) found. Fix before archiving."
   - If only warnings: "No critical issues. Y warning(s) to consider. Ready for archive (with noted improvements)."
   - If all clear: "All checks passed. Ready for archive."

   Do not fix findings or re-run the review unless the user explicitly asks.

**Spec lookup notes**

Delta specs (under a change) use:

- `## ADDED Requirements` — new behavior that must appear in the diff
- `## MODIFIED Requirements` — existing behavior that must change as described
- `## REMOVED Requirements` — behavior that must no longer exist
- `## RENAMED Requirements` — FROM/TO; treat as the same requirement under the new name

Requirements look like:

```markdown
### Requirement: Dark Mode Toggle
The system SHALL let a user switch between light and dark themes.

#### Scenario: Respects the OS preference on first load
- **GIVEN** a user who has never set a theme
- **WHEN** they open the app on a device set to dark mode
- **THEN** the app renders in dark mode
```

Review against the **delta** (what this change promised), not the entire main spec, unless the user asked to review a capability's main spec.

**Verification Heuristics**

- **Completeness**: Focus on objective checklist items (checkboxes, requirements list)
- **Correctness**: Prefer the git diff as evidence; use keyword search and file path analysis when the diff is incomplete. Do not require perfect certainty
- **Coherence**: Look for glaring inconsistencies, don't nitpick style
- **False Positives**: When uncertain, prefer SUGGESTION over WARNING, WARNING over CRITICAL
- **Actionability**: Every issue must have a specific recommendation with file/line references where applicable
- **Not a general PR review**: Do not expand into unrelated nits, security hunts, or refactors unless they contradict the spec. Spec match is the job.

**Graceful Degradation**

- If only tasks.md exists: verify task completion only, skip spec/design checks
- If tasks + specs exist: verify completeness and correctness, skip design
- If full artifacts: verify all three dimensions
- If specs exist but the diff is empty: still map requirements to current code and say the working tree had nothing to review
- Always note which checks were skipped and why

**Output Format**

Use clear markdown with:
- Table for summary scorecard
- Requirement mapping table
- Grouped lists for issues (CRITICAL/WARNING/SUGGESTION)
- Code references in format: `file.ts:123`
- Specific, actionable recommendations
- No vague suggestions like "consider reviewing"

**Guardrails**
- Read artifacts from CLI-resolved paths; do not assume `openspec/changes/<name>/...`
- Do not implement fixes, edit specs, or archive as part of this review
- If no change and no spec can be resolved, stop and ask
