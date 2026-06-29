# Context Taxonomy

Use this taxonomy to map context before compacting it. Include only categories that affect continuation.

## Required Classes

### Goal

The concrete outcome the user wants. Keep one primary goal unless the task is explicitly multi-goal.

### Current State

Where the work stands now:

- completed
- in progress
- blocked
- not started
- partially verified

### User Intent

What the user cares about, including working style, constraints, and trust boundaries. Separate durable preferences from task-local instructions.

### Verified Facts

Facts grounded in source evidence:

- file contents
- command output
- tool result
- user statement
- issue/PR/document text
- memory excerpt

Use source anchors when the fact affects execution.

### Assumptions

Reasonable inferences that are not directly verified. Keep them corrigible and brief.

### Decisions

Choices already made that should not be reopened without a reason.

Record:

- decision
- rationale
- source/evidence
- reversal condition, if known

### Open Questions

Missing answers that could change the next action. Do not list decorative unknowns.

### Active Files / Code Areas

Touched or relevant files, modules, APIs, configs, docs, tests, generated artifacts, and scripts.

Include:

- path
- role
- status
- reason it matters

### Tool State / Environment

Running servers, pending sessions, failed commands, installed tools, package manager state, branch status, dirty worktree, network/API assumptions, and platform constraints.

### Risks

Things that could cause a wrong continuation:

- stale assumption
- missing verification
- destructive operation
- hidden dependency
- conflicting instructions
- secret exposure
- test gap

### Non-Goals

Work explicitly out of scope or intentionally deferred.

### Next Actions

Concrete execution steps. Prefer ordered actions with verification.

### Implications for Next Agent

Derived consequences from the mapped context.

Example:

```text
Because the schema changed and only unit tests ran, run the integration suite before touching the importer again.
```

## Contradiction Handling

When sources conflict:

1. State the conflict.
2. Prefer newer direct evidence over older summaries.
3. Mark unresolved conflicts explicitly.
4. Do not collapse conflict into a confident statement.

## Source Strength

Prefer evidence in this order when available:

1. Current file contents or live command/tool output
2. Current user instruction
3. Current issue/PR/spec/document
4. Recent memory with source lines
5. Older summaries or inferred context

If the best available source is weak, say so.
