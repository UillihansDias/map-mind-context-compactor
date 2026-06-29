---
name: map-mind-context-compactor
description: Create validated context maps, handoff packets, resume briefs, and compaction summaries for long coding-agent sessions. Use when preserving task state across context compaction, handing work to another agent, recovering from interrupted sessions, preparing Codex/Antigravity/OpenClaw to continue complex work, or checking that decisions, constraints, files, risks, verified facts, assumptions, and next actions are not lost.
---

# Map Mind Context Compactor

Use this skill as a context compiler, not a summarizer. Build a compact, source-grounded operating packet that lets a fresh coding assistant resume without rereading the full session.

Core rule:

```text
Map the context first.
Probe only what matters.
Mind the intent and constraints.
Compact only after the structure is understood.
Check before handing off.
```

## Quick Start

1. Identify the requested artifact: `context-map`, `handoff-packet`, `resume-brief`, or validation report.
2. Read only the relevant context sources: conversation, repo status, touched files, memory files, issue/PR text, task notes, tool outputs, and existing handoffs.
3. Build a context inventory before writing the compacted packet.
4. Separate verified facts, assumptions, decisions, open questions, constraints, risks, and next actions.
5. Use the templates in `assets/templates/` when the user wants a written artifact.
6. Run `scripts/validate_context_packet.py` on any final artifact when a file is produced. Use `--type context-map`, `--type handoff-packet`, or `--type resume-brief` when the heading is missing or ambiguous.
7. If validation fails, fix the packet or clearly state why it is not safe to trust yet.

## Workflow

### 1. Intake

Capture:

- Goal and success condition
- User intent and preferences that matter for continuation
- Workspace/repo/project scope
- Active constraints and non-goals
- Time-sensitive or environment-specific facts
- Privacy and secret-handling boundaries

Do not treat every prior message as equally important. Preserve what changes future execution.

### 2. Map

Create an external context map before compacting. Include:

- People, projects, files, tools, commands, dependencies, decisions, blockers, timeline, risks, and open loops
- Touched files with paths and status where known
- Tool state that affects continuation, such as running servers, failed commands, pending sessions, or uncommitted work
- Source anchors for facts that would be costly or risky to reconstruct

Read `references/context-taxonomy.md` when the context is large, mixed, or unclear.

### 3. Probe

Treat long context as an external environment, not a blob to summarize.

Use targeted probes:

- Search before broad reading.
- Inspect files or logs only when they affect the next action.
- Verify claims that influence execution.
- Stop probing when the packet can answer: goal, state, constraints, verified facts, risks, and next action.

For huge contexts, split into subcontexts, query each for task-relevant facts, and merge only the useful results. Do not recursively re-check already verified facts unless new evidence conflicts.

### 4. Mind

Model the user and task intent explicitly:

- What the user is trying to accomplish
- What they care about preserving
- What they do not want disturbed
- What trust boundaries apply
- Which assumptions are safe and which need confirmation
- What the likely next move is

Keep durable preferences separate from one-off instructions. Do not promote task-local details into long-term memory unless the user asks or the fact is future-useful.

### 5. Compact

Produce the smallest executable packet that preserves continuity.

Prefer this shape:

```text
1. Goal
2. Current State
3. User Intent
4. Constraints
5. Decisions Made
6. Facts Verified
7. Assumptions
8. Open Questions
9. Active Files / Code Areas
10. Tool State / Environment
11. Risks
12. Next Actions
13. Non-Goals
14. Resume Prompt
15. Implications for Next Agent
```

Read `references/compaction-rules.md` before compacting a long, conflicted, high-stakes, or multi-agent session.

### 6. Check

Validate process and output:

- Intake complete enough to resume
- Context map built before summary
- Verified facts separated from assumptions
- Open loops preserved
- Next action concrete
- Claims source-grounded where execution depends on them
- No accidental secrets, credentials, or raw private dumps
- File references exist or are marked unresolved
- Packet fits the chosen size budget

Run validation and scoring. The scripts auto-detect standard template headings; pass `--type` explicitly for partial or renamed files.

```bash
python3 scripts/validate_context_packet.py path/to/packet.md
python3 scripts/score_context_packet.py path/to/packet.md
python3 scripts/validate_context_packet.py --type resume-brief path/to/resume.md
```

Read `references/validation-checks.md` when validation fails or the handoff is high-stakes.

### 7. Resume Test

Ask:

```text
Could a fresh assistant continue correctly from this without rereading the whole session?
```

If not, the packet fails. State what is missing instead of pretending the handoff is complete.

## Optional Consistency Mode

Use for messy, high-stakes, or long-running work.

1. Generate two independent compacted packets or two verifier passes.
2. Keep source-backed facts.
3. Flag disagreements as uncertainty.
4. Do not hide disagreement by averaging it away.

For multi-agent use, separate producer and verifier roles:

- Producer creates the packet.
- Verifier critiques omissions, unsupported claims, stale assumptions, unsafe leakage, vague next actions, and missing source anchors.

## Output Artifacts

Use the bundled templates:

- `assets/templates/context-map.md` for inventory-first mapping
- `assets/templates/handoff-packet.md` for full continuation packets
- `assets/templates/resume-brief.md` for short restart prompts

Use `scripts/extract_file_refs.py` to list referenced files from a packet and check whether local paths exist.

## Quality Bar

A good packet answers:

```text
What is the user trying to do?
What has already happened?
What must not be lost?
What is verified?
What is still uncertain?
Which files/tools matter?
What should happen next?
```

An excellent packet can also say:

```text
This context packet is not safe to trust yet because X is missing or unsupported.
```
