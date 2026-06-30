# Map Mind Context Compactor

Map Mind Context Compactor is an agent skill for turning long, messy coding-agent sessions into compact, source-grounded continuation packets.

It is built for moments where a fresh assistant needs to resume work without rereading the whole conversation: context compaction, handoffs, interrupted sessions, multi-agent delegation, or long-running implementation work with many files and decisions.

The core idea is simple:

```text
Map the context first.
Probe only what matters.
Mind the intent and constraints.
Compact only after the structure is understood.
Check before handing off.
```

## What It Produces

The skill can produce three main artifacts:

- `context-map`: an inventory-first map of goals, sources, facts, assumptions, risks, files, and next actions.
- `handoff-packet`: a fuller continuation packet for another agent or a future session.
- `resume-brief`: a short restart prompt that preserves the next move and the facts that must not be lost.

These artifacts are not generic summaries. They separate verified facts from assumptions, preserve open questions, record tool and file state, and make the next action concrete.

## When To Use It

Use this skill when:

- a coding session is about to be compacted or handed off
- another agent needs to continue work reliably
- a long task has many touched files, decisions, risks, or partial test results
- you need a restart prompt after an interruption
- you want to validate whether a handoff is safe to trust

Avoid using it for small one-step tasks where a normal answer is enough.

## Repository Contents

```text
.
|-- SKILL.md
|-- agents/
|   `-- openai.yaml
|-- assets/
|   `-- templates/
|       |-- context-map.md
|       |-- handoff-packet.md
|       `-- resume-brief.md
|-- references/
|   |-- compaction-rules.md
|   |-- context-taxonomy.md
|   |-- examples.md
|   `-- validation-checks.md
`-- scripts/
    |-- extract_file_refs.py
    |-- score_context_packet.py
    `-- validate_context_packet.py
```

## Quick Start

1. Choose the artifact you need: `context-map`, `handoff-packet`, or `resume-brief`.
2. Gather only the context that affects continuation: user goal, current repo state, touched files, decisions, failed commands, test results, risks, and open questions.
3. Start from the matching template in `assets/templates/`.
4. Fill it with source-grounded facts, not broad transcript summary.
5. Validate or score the finished artifact before trusting it.

Example:

```bash
cp assets/templates/handoff-packet.md handoff.md
python3 scripts/validate_context_packet.py --type handoff-packet handoff.md
python3 scripts/score_context_packet.py --type handoff-packet handoff.md
```

## Validation Tools

`scripts/validate_context_packet.py` checks whether a packet has the required sections, concrete next actions, secret-like content, vague continuation language, and missing absolute file references.

```bash
python3 scripts/validate_context_packet.py path/to/packet.md
python3 scripts/validate_context_packet.py --type resume-brief path/to/resume.md
python3 scripts/validate_context_packet.py --strict-paths path/to/packet.md
```

`scripts/score_context_packet.py` gives a completeness and resumability score.

```bash
python3 scripts/score_context_packet.py path/to/packet.md
```

`scripts/extract_file_refs.py` lists likely local file references in a packet and whether absolute paths exist on the current machine.

```bash
python3 scripts/extract_file_refs.py path/to/packet.md
```

## What A Good Packet Preserves

A strong packet answers:

- What is the user trying to accomplish?
- What has already happened?
- What must not be lost?
- What is verified?
- What is still uncertain?
- Which files, tools, commands, and environments matter?
- What should happen next?
- What should the next agent avoid disturbing?

An excellent packet also says when it is not safe to trust yet, and why.

## Example Handoff Fragment

```markdown
## Goal

Implement CSV import validation for `/orders` and verify it with unit and integration tests.

## Current State

Parser changes are implemented in `src/orders/importer.ts`. Unit tests pass. Integration tests have not been run.

## Facts Verified

- `src/orders/importer.ts` contains the new `validateOrderRow` path.
- `tests/orders/importer.test.ts` covers missing `order_id` and malformed dates.
- `npm test -- importer` passed locally.

## Assumptions

- The integration suite uses the same fixtures as the unit tests. This has not been verified.

## Next Actions

1. Run the order integration tests.
2. If they pass, run the full test suite.
3. Update the handoff if integration fixtures require schema changes.
```

## Design Principles

- Compile context instead of summarizing everything.
- Preserve user intent, constraints, and non-goals.
- Keep verified facts separate from assumptions.
- Include source anchors where a future agent would otherwise need to re-check.
- Make risks and test gaps explicit.
- End with concrete next actions.
- Validate before declaring a handoff ready.

## Skill Entry Point

The main skill instructions live in [`SKILL.md`](SKILL.md). The OpenAI agent-facing manifest is in [`agents/openai.yaml`](agents/openai.yaml).
