# Validation Checks

Use this reference when a context packet needs strict review.

## Required Output Checks

Use the artifact-specific validator mode for the file being produced:

```bash
python3 scripts/validate_context_packet.py --type context-map path/to/context-map.md
python3 scripts/validate_context_packet.py --type handoff-packet path/to/handoff.md
python3 scripts/validate_context_packet.py --type resume-brief path/to/resume.md
```

Auto-detection is acceptable for files created from the bundled templates. Use an explicit `--type` when the title has been changed, omitted, or embedded inside another document.

A deployable packet should have:

- one explicit goal
- one current status
- user intent
- constraints or an explicit `None known`
- decisions made or an explicit `None recorded`
- verified facts separated from assumptions
- open questions or an explicit `None blocking`
- active files/code areas or an explicit `None identified`
- tool/environment state or an explicit `None relevant`
- risks or an explicit `None known`
- concrete next actions
- non-goals or an explicit `None stated`
- resume prompt
- implications for next agent

A context map should have:

- one explicit goal
- success condition
- sources inspected
- user intent
- constraints
- decisions or an explicit `None recorded`
- verified facts
- assumptions
- active files/code areas
- tool/environment state
- risks
- open questions
- concrete next actions
- non-goals
- implications for next agent

A resume brief should have:

- resume prompt
- goal
- current state
- must-preserve facts or constraints
- verified facts
- uncertainties
- next action
- verification needed

## Process Checks

The agent should be able to answer:

- Was a context map built before compacting?
- Were targeted probes used instead of broad rereading?
- Were important claims verified from source?
- Were contradictions marked instead of hidden?
- Were privacy boundaries respected?
- Was the packet validated after writing?

## Safety Checks

Reject or warn if the packet includes:

- API keys, tokens, passwords, private keys, or cookies
- raw private transcript dumps
- unneeded personal data
- destructive next actions without confirmation language
- public posting/sharing actions without approval
- credential setup instructions containing real secrets

## Trust Checks

Warn if:

- no source anchors exist for execution-critical facts
- next action is vague
- packet says work is complete but verification is absent
- file references are malformed
- local file references do not exist
- assumptions are phrased as facts
- multiple goals conflict
- current state is missing

## Verdicts

Use one of:

```text
PASS: Safe to resume from this packet.
WARN: Usable, but the next agent must address listed gaps.
FAIL: Not safe to trust yet.
```

Never upgrade a `FAIL` to `PASS` because the wording sounds polished.
