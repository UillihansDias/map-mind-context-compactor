# Compaction Rules

Use these rules when turning a mapped context into a compact continuation packet.

## Preserve

Always preserve:

- the user's current goal
- success condition
- active constraints
- decisions already made
- files and code areas that matter
- verified facts needed for execution
- unresolved questions that could alter work
- risks and missing verification
- next action and verification command

## Drop

Drop or compress:

- politeness, filler, repeated confirmations
- stale plans superseded by later evidence
- dead-end explorations that no longer affect execution
- verbose tool output once the relevant fact is extracted
- duplicate summaries
- speculation that does not affect action

## Separate

Do not blur:

- verified facts vs assumptions
- active work vs background history
- user preference vs one-off instruction
- durable memory vs short-lived state
- completed work vs intended work
- repo evidence vs conversational inference
- blocker vs minor uncertainty

## Source Anchors

Use source anchors when a fact is important, surprising, easy to misremember, or costly to re-check.

Good anchors:

```text
src/importer.ts defines the parser entrypoint.
tests/importer.test.ts currently covers malformed rows.
Command `npm test` failed with 2 importer assertions.
User explicitly said not to change global config.
```

Weak anchors:

```text
It seems...
Probably...
Earlier we discussed...
Some file somewhere...
```

## Size Control

Prefer dense, executable prose over transcript summary.

Default budgets:

- Resume brief: 250-600 words
- Handoff packet: 700-1600 words
- Full context map: as long as needed, but keep repeated detail out

If the budget forces a trade-off, preserve executable state before narrative background.

## Bounded Recursive Decomposition

Use decomposition only when the context is too large or mixed to map directly.

Procedure:

1. Split by source or concern: conversation, repo, memory, issues, commands, generated artifacts.
2. Ask each subcontext the same limited questions: goal, facts, decisions, risks, next actions.
3. Merge only non-duplicative task-relevant results.
4. Stop when more probing is unlikely to change the packet.

Failure mode:

```text
Repeated verification can waste time and degrade clarity.
```

Stop rule:

```text
Do not recursively re-check already verified facts unless new evidence conflicts.
```

## Implications

Add implications only when they help the next agent act.

Good:

```text
Because the dependency was added but lockfile status is unknown, run the package manager check before committing.
```

Bad:

```text
This project is important and should be handled carefully.
```
