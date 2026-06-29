# Examples

## Handoff Packet Fragment

```markdown
## Goal

Implement CSV import validation for `/orders` and verify it with unit and integration tests.

## Current State

Parser changes are implemented in `src/orders/importer.ts`. Unit tests pass. Integration tests have not been run.

## Verified Facts

- `src/orders/importer.ts` contains the new `validateOrderRow` path.
- `tests/orders/importer.test.ts` covers missing `order_id` and malformed dates.
- `npm test -- importer` passed locally.

## Assumptions

- The integration suite uses the same fixtures as the unit tests. This has not been verified.

## Next Actions

1. Run the order integration tests.
2. If they pass, run the full test suite.
3. Update the handoff if integration fixtures require schema changes.

## Implications for Next Agent

Because only focused unit tests ran, do not claim the importer is done until the integration suite passes or the remaining test gap is documented.
```

## Resume Brief Fragment

```markdown
Continue the CSV import validation task. The importer implementation exists in `src/orders/importer.ts`; focused unit tests passed, but integration tests are still pending. Preserve the decision to keep validation in the importer layer rather than moving it into the controller. Next: run integration tests, fix fixture/schema fallout if any, then run the full suite.
```

## Bad Compaction

```markdown
We worked on import stuff and it seems mostly done. Continue testing.
```

Why it fails:

- no concrete goal
- no current state
- no file paths
- no verified facts
- no risk or test gap
- vague next action
