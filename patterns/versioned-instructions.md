# Pattern — Versioned instructions

**Problem:** if instructions can change while a task is running, the task's behavior
depends on when it happened to be scheduled, and failures stop being reproducible.

**Solution:** instructions are versioned. A running task keeps the version it started
with; the next task picks up the new one.

## Invariants

- Every task records the instruction version it began under.
- An update does not reach a task already in flight.
- The next task picks up the new version.
- Rollback is possible and returns the configuration to a previous version.
- Rollback is **conditional on recurrence**, not automatic per update.

## Why pinning

Without pinning, three things break at once:

**Reproducibility.** A task that failed cannot be re-run to investigate, because the
instructions it ran under no longer exist.

**Attribution.** If behavior changed midway, you cannot tell whether an outcome came
from the task or the update.

**Safety.** A mid-task change can invalidate work already done under the old rules.
A review that passed under version N may not pass under N+1, and the task has already
built on it.

## Why rollback is conditional

An accepted update is not rolled back merely because it is an update — that would
make the loop unable to keep anything. Rollback triggers when the update's own
failure mode **reappears in later work**.

Related discipline: absence of a regression report is not evidence of improvement.
Missing evidence stays unknown. Treating "no failures observed" as "the change
worked" is how a loop accumulates changes that were never tested.

## Checks

- Can you name the instruction version a currently running task is using?
- Has an update ever reached an in-flight task?
- For each accepted update, can you state the recurrence that would trigger rollback?
- Are versions retained long enough to roll back, or are old versions discarded?

## Failure if omitted

Unreproducible failures, unattributable behavior changes, and tasks that build on
work done under superseded rules. The failure is quiet: everything appears to work,
and nothing can be investigated after the fact.
